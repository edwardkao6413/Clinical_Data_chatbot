"""
OSVi Biomechanics Database — Demo Prototype
============================================
A lightweight Flask server that:
  1. Loads the demo CSV into memory (pandas DataFrame)
  2. Serves an interactive HTML dashboard
  3. Proxies chat requests to the Claude API so the chatbot can answer
     any question about the patient population data

Usage
-----
  pip install -r requirements.txt
  set ANTHROPIC_API_KEY=sk-ant-...        # Windows
  export ANTHROPIC_API_KEY=sk-ant-...     # Mac / Linux
  python app.py

Then open http://localhost:5050 in your browser.
"""

import os, json, textwrap, pathlib
from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CSV_PATH = pathlib.Path(__file__).resolve().parent.parent / "tmp" / "OSVi_Biomechanics_Demo_Database.csv"
PORT = 5050
MODEL = "claude-sonnet-4-20250514"

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print(f"Loading CSV from {CSV_PATH} ...")
df = pd.read_csv(CSV_PATH)
print(f"  → {len(df)} rows × {len(df.columns)} columns loaded.")

# Pre-compute some useful metadata
DEMOGRAPHICS = {
    "sports": sorted(df["Sport"].dropna().unique().tolist()),
    "symptoms": sorted(df["Symptom"].dropna().unique().tolist()),
    "sexes": sorted(df["Sex"].dropna().unique().tolist()),
    "injury_limbs": sorted(df["Injury_Limb"].dropna().unique().tolist()),
    "post_surgery_months": sorted(df["Post_Surgery_Progress"].dropna().unique().astype(int).tolist()),
    "age_min": int(df["Age"].min()),
    "age_max": int(df["Age"].max()),
    "total_patients": int(df["Patient_ID"].nunique()),
    "total_records": len(df),
}

# Build a compact data-dictionary string for the system prompt
COLUMN_GROUPS = {
    "Demographics": ["Patient_ID", "Age", "Sex", "Sport", "Symptom", "Injury_Limb", "Post_Surgery_Progress"],
    "Knee Extension Strength (Iso/Con/Ecc, L/R/LSI)": [c for c in df.columns if c.startswith("Ext") or c.startswith("ReExt") or c.startswith("IsoPt200") and "ext" in c.lower() or c.startswith("Jang_pt") and "ext" in c.lower()],
    "Knee Flexion Strength": [c for c in df.columns if "Fle" in c or ("fle" in c.lower() and ("IsoPt200" in c or "Jang" in c))],
    "H:Q Ratios": [c for c in df.columns if "HQ" in c],
    "Ankle Plantarflexion": [c for c in df.columns if c.startswith("Pl") or c.startswith("Re") and c not in ["ReExtIsoL_","ReExtIsoR_","ReExtConL_","ReExtConR_","ReExtEccL_","ReExtEccR_","ReFleIsoL_","ReFleIsoR_","ReFleConL_","ReFleConR_","ReFleEccL_","ReFleEccR_","ReAdLeft_","ReAdRight_","ReAbLeft_","ReAbRight_"]],
    "Hip Ad/Abduction": [c for c in df.columns if c.startswith("Ad") or c.startswith("Ab") or c.startswith("ReAd") or c.startswith("ReAb")],
    "DL CMJ": [c for c in df.columns if "DL" in c and "cmj" in c.lower() or c == "jhDL_"],
    "DL Drop Jump": [c for c in df.columns if "DL" in c and "dj" in c.lower() or c == "rsidj_DL_" or c == "asi_DL_dj_"],
    "DL 10-5": [c for c in df.columns if "105" in c and "DL" in c],
    "SL CMJ": [c for c in df.columns if "SL" in c and ("cmj" in c.lower() or c.startswith("jhSL_L") or c.startswith("jhSL_R") or c.startswith("LSI_jhSL") or "ciP" in c or ("ci_" in c and "SL" in c))],
    "SL Drop Jump": [c for c in df.columns if "SL" in c and "dj" in c.lower()],
    "SL 10-5": [c for c in df.columns if "105" in c and "SL" in c],
    "Triple Hop": [c for c in df.columns if "triforhop" in c],
    "SL Squat Power": [c for c in df.columns if "sq_cpp" in c],
}

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder="static")

# Serve dashboard
@app.route("/")
def index():
    return send_from_directory(pathlib.Path(__file__).parent, "index.html")

# ---------------------------------------------------------------------------
# API: demographics metadata
# ---------------------------------------------------------------------------
@app.route("/api/demographics")
def api_demographics():
    return jsonify(DEMOGRAPHICS)

# ---------------------------------------------------------------------------
# API: filter & aggregate data
# ---------------------------------------------------------------------------
@app.route("/api/query", methods=["POST"])
def api_query():
    """
    Accepts JSON filters and returns filtered summary statistics.
    Body: { age_min, age_max, sex, sport, symptom, injury_limb, months, metrics }
    """
    body = request.json or {}
    filtered = df.copy()

    if body.get("age_min"):
        filtered = filtered[filtered["Age"] >= int(body["age_min"])]
    if body.get("age_max"):
        filtered = filtered[filtered["Age"] <= int(body["age_max"])]
    if body.get("sex"):
        filtered = filtered[filtered["Sex"] == body["sex"]]
    if body.get("sport"):
        filtered = filtered[filtered["Sport"] == body["sport"]]
    if body.get("symptom"):
        filtered = filtered[filtered["Symptom"] == body["symptom"]]
    if body.get("injury_limb"):
        filtered = filtered[filtered["Injury_Limb"] == body["injury_limb"]]
    if body.get("months"):
        filtered = filtered[filtered["Post_Surgery_Progress"] == int(body["months"])]

    metrics = body.get("metrics", ["jhSL_L_", "jhSL_R_", "LSI_jhSL_"])

    # Build summary
    summary = {}
    for m in metrics:
        if m in filtered.columns:
            col = filtered[m].dropna()
            summary[m] = {
                "n": int(len(col)),
                "mean": round(float(col.mean()), 2) if len(col) else None,
                "std": round(float(col.std()), 2) if len(col) else None,
                "min": round(float(col.min()), 2) if len(col) else None,
                "p25": round(float(col.quantile(0.25)), 2) if len(col) else None,
                "median": round(float(col.median()), 2) if len(col) else None,
                "p75": round(float(col.quantile(0.75)), 2) if len(col) else None,
                "max": round(float(col.max()), 2) if len(col) else None,
                "values": col.tolist(),  # for histogram
            }
    return jsonify({"n_records": len(filtered), "summary": summary})

# ---------------------------------------------------------------------------
# API: find similar patients
# ---------------------------------------------------------------------------
@app.route("/api/similar", methods=["POST"])
def api_similar():
    """
    Find patients similar to a given profile.
    Body: { age, sex, sport, symptom, injury_limb, months, top_n }
    """
    body = request.json or {}
    target_age = int(body.get("age", 30))
    top_n = int(body.get("top_n", 10))

    filtered = df.copy()
    if body.get("sex"):
        filtered = filtered[filtered["Sex"] == body["sex"]]
    if body.get("sport"):
        filtered = filtered[filtered["Sport"] == body["sport"]]
    if body.get("symptom"):
        filtered = filtered[filtered["Symptom"] == body["symptom"]]
    if body.get("injury_limb"):
        filtered = filtered[filtered["Injury_Limb"] == body["injury_limb"]]
    if body.get("months"):
        filtered = filtered[filtered["Post_Surgery_Progress"] == int(body["months"])]

    # Score by age similarity
    filtered = filtered.copy()
    filtered["_age_diff"] = (filtered["Age"] - target_age).abs()
    filtered = filtered.sort_values("_age_diff").head(top_n)

    # Select key columns for display
    display_cols = ["Patient_ID", "Age", "Sex", "Sport", "Symptom", "Injury_Limb",
                    "Post_Surgery_Progress",
                    "ExtIsoLSI_", "ExtConLSI_", "FleIsoLSI_", "FleConLSI_",
                    "LSI_jhSL_", "LSI_rsidj_SL_", "LSI_triforhop_",
                    "HQcc_L_", "HQcc_R_"]
    display_cols = [c for c in display_cols if c in filtered.columns]
    result = filtered[display_cols].to_dict(orient="records")

    return jsonify({"n_matched": len(filtered), "patients": result})

# ---------------------------------------------------------------------------
# API: recovery trajectory
# ---------------------------------------------------------------------------
@app.route("/api/recovery", methods=["POST"])
def api_recovery():
    """
    Return population percentiles across post-surgery timepoints for given filters.
    Body: { sex, sport, symptom, metrics }
    """
    body = request.json or {}
    filtered = df.copy()
    filtered = filtered.dropna(subset=["Post_Surgery_Progress"])

    if body.get("sex"):
        filtered = filtered[filtered["Sex"] == body["sex"]]
    if body.get("sport"):
        filtered = filtered[filtered["Sport"] == body["sport"]]
    if body.get("symptom"):
        filtered = filtered[filtered["Symptom"] == body["symptom"]]

    metrics = body.get("metrics", ["ExtIsoLSI_", "LSI_jhSL_", "LSI_triforhop_"])
    months = sorted(filtered["Post_Surgery_Progress"].unique().astype(int).tolist())

    trajectories = {}
    for m in metrics:
        if m not in filtered.columns:
            continue
        traj = []
        for mo in months:
            sub = filtered[filtered["Post_Surgery_Progress"] == mo][m].dropna()
            if len(sub) == 0:
                continue
            traj.append({
                "month": int(mo),
                "n": int(len(sub)),
                "p25": round(float(sub.quantile(0.25)), 2),
                "median": round(float(sub.median()), 2),
                "p75": round(float(sub.quantile(0.75)), 2),
            })
        trajectories[m] = traj

    return jsonify({"months": months, "trajectories": trajectories})

# ---------------------------------------------------------------------------
# API: Chat with Claude
# ---------------------------------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Send a user message to Claude with data context.
    Body: { message, filters (optional) }
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not set. Please set it as an environment variable."}), 400

    body = request.json or {}
    user_msg = body.get("message", "")
    filters = body.get("filters", {})

    # Build filtered data context
    filtered = df.copy()
    if filters.get("sex"):
        filtered = filtered[filtered["Sex"] == filters["sex"]]
    if filters.get("sport"):
        filtered = filtered[filtered["Sport"] == filters["sport"]]
    if filters.get("symptom"):
        filtered = filtered[filtered["Symptom"] == filters["symptom"]]
    if filters.get("age_min"):
        filtered = filtered[filtered["Age"] >= int(filters["age_min"])]
    if filters.get("age_max"):
        filtered = filtered[filtered["Age"] <= int(filters["age_max"])]
    if filters.get("months"):
        filtered = filtered[filtered["Post_Surgery_Progress"] == int(filters["months"])]

    # Create a concise data summary for context
    data_context = f"""DATABASE SUMMARY (filtered: {len(filtered)} records from {len(df)} total):

Demographics of filtered set:
- Age: {filtered['Age'].describe().to_dict()}
- Sex: {filtered['Sex'].value_counts().to_dict()}
- Sport: {filtered['Sport'].value_counts().to_dict()}
- Symptom: {filtered['Symptom'].value_counts().to_dict()}
- Post-surgery months: {filtered['Post_Surgery_Progress'].value_counts().sort_index().to_dict()}

Key LSI metrics (filtered):
- Ext Isometric LSI: mean={filtered['ExtIsoLSI_'].mean():.1f}%, median={filtered['ExtIsoLSI_'].median():.1f}%
- Ext Concentric LSI: mean={filtered['ExtConLSI_'].mean():.1f}%, median={filtered['ExtConLSI_'].median():.1f}%
- Fle Isometric LSI: mean={filtered['FleIsoLSI_'].mean():.1f}%, median={filtered['FleIsoLSI_'].median():.1f}%
- SL Jump Height LSI: mean={filtered['LSI_jhSL_'].mean():.1f}%, median={filtered['LSI_jhSL_'].median():.1f}%
- SL Drop Jump RSI LSI: mean={filtered['LSI_rsidj_SL_'].mean():.1f}%, median={filtered['LSI_rsidj_SL_'].median():.1f}%
- Triple Hop LSI: mean={filtered['LSI_triforhop_'].mean():.1f}%, median={filtered['LSI_triforhop_'].median():.1f}%

All available columns: {', '.join(df.columns.tolist())}
"""

    # If the user asks about specific metrics, include more detail
    # Find the top 5 most relevant numeric columns and add descriptive stats
    relevant_cols = [c for c in filtered.select_dtypes(include="number").columns
                     if any(kw in user_msg.lower() for kw in [c.lower().replace("_",""), c.lower()[:5]])]
    if relevant_cols:
        data_context += "\nDetailed stats for potentially relevant metrics:\n"
        for c in relevant_cols[:8]:
            desc = filtered[c].describe()
            data_context += f"  {c}: n={desc['count']:.0f}, mean={desc['mean']:.2f}, std={desc['std']:.2f}, min={desc['min']:.2f}, p25={desc['25%']:.2f}, median={desc['50%']:.2f}, p75={desc['75%']:.2f}, max={desc['max']:.2f}\n"

    system_prompt = textwrap.dedent(f"""\
    You are OSVi Assistant, a clinical biomechanics data analyst embedded in the OSVi patient database system.
    You help clinicians and physiotherapists query and understand patient population data for rehabilitation assessment.

    CONTEXT:
    - The database contains {len(df)} assessment records from {df['Patient_ID'].nunique()} unique patients
    - Conditions: ACLR (ACL Reconstruction), TKR (Total Knee Replacement), ATH (Athletic/non-surgical)
    - Sports: Australian Football, Cricket, Rugby, Basketball, Baseball
    - Post-surgery timepoints: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30 months
    - LSI (Limb Symmetry Index) = injured limb ÷ uninjured limb × 100%. Return-to-sport threshold: ≥90%
    - Tests include: isokinetic strength (extension/flexion, isometric/concentric/eccentric), H:Q ratios,
      ankle plantarflexion, hip ad/abduction, DL/SL CMJ, DL/SL drop jump, DL/SL 10-5 hops, triple hop, SL squat

    CURRENT DATA:
    {data_context}

    GUIDELINES:
    - Be concise and clinically relevant
    - Always cite sample sizes when reporting statistics
    - Use the ≥90% LSI threshold as the clinical benchmark for return-to-sport decisions
    - When comparing a patient to the population, clearly state percentile rankings
    - If data is insufficient (n < 5), flag this as a limitation
    - Format numbers to 1 decimal place
    - You can suggest which metrics to look at if the clinician's question is broad
    - Never fabricate data — only report what's in the database
    """)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}],
        )
        reply = response.content[0].text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------------------
# API: get raw data for a specific patient
# ---------------------------------------------------------------------------
@app.route("/api/patient/<patient_id>")
def api_patient(patient_id):
    rows = df[df["Patient_ID"] == patient_id]
    if rows.empty:
        return jsonify({"error": f"Patient {patient_id} not found"}), 404
    return jsonify(rows.to_dict(orient="records"))

# ---------------------------------------------------------------------------
# API: list all columns
# ---------------------------------------------------------------------------
@app.route("/api/columns")
def api_columns():
    return jsonify({"columns": df.columns.tolist(), "groups": {k: v for k, v in COLUMN_GROUPS.items()}})

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  OSVi Database Prototype")
    print(f"  Open http://localhost:{PORT} in your browser")
    print(f"{'='*60}\n")
    app.run(host="0.0.0.0", port=PORT, debug=True)
