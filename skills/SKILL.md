---
name: osvi-biomechanics-database
description: >
  Master project skill for the OSVi Biomechanics Database and Dashboard. Provides full
  context needed to work on the database, prototype dashboard, AI chatbot, reporting,
  or the harness engineering pipeline. Read this before performing any task related to
  data analysis, code changes, dashboard improvements, or clinical reporting. Trigger
  for any task involving the OSVi population database, the Flask dashboard prototype,
  metric definitions, or clinical biomechanics data.
compatibility: >
  Python 3.10+, Flask, pandas, anthropic SDK. ANTHROPIC_API_KEY environment variable
  required for chatbot functionality. Runs on localhost:5050.
---

# OSVi Biomechanics Database — Project Skill

This document provides the full context needed to work intelligently on the OSVi Biomechanics Database project. Read this before performing any task related to the database, prototype, chatbot, or reporting.

---

## 1. Project Overview

**Organisation:** OSVi (clinical biomechanics and rehabilitation consultancy, Melbourne, Australia)

**Goal:** Build a web application that allows clinicians and physiotherapists to query a patient biomechanics population database, compare individual patients against population benchmarks, and receive AI-assisted clinical insights.

**Current stage:** Working prototype (demo) — a local Flask web application backed by a demo CSV database, with an embedded Claude-powered AI chatbot.

**Three core use cases:**
1. **Population Reporting** — Query population statistics for a filtered cohort (e.g., "Show 6-month post-op RSI data for 30-year-old ACLR basketball players")
2. **Pre-surgery Consulting** — Find patients similar to a new patient's profile to inform treatment planning
3. **Post-surgery Recovery Comparison** — Show a patient how their recovery trajectory compares to population percentiles over time

---

## 2. Folder Structure

```
OSVi_database_demo/               ← project root
│
├── prototype/                    ← the running web app
│   ├── app.py                    ← Flask server: loads CSV, API endpoints, Claude proxy
│   ├── index.html                ← single-page dashboard (4 tabs)
│   ├── requirements.txt          ← flask, anthropic, pandas
│   ├── knowledge/                ← (empty) folder for future RAG documents
│   └── variants/                 ← generated dashboard variants (from harness Trial agent)
│
├── references/                   ← background materials
│   ├── OSVi_Biomechanics_Demo_Database_DataSummary.md
│   ├── metric_labels.json        ← source of truth for metric display names
│   ├── conversation_osvi_prototype.html
│   └── 2026_MARCH_WORKING TEMPLATE_PERFORMANCE REPORT_L4_MALES_Follow-up_FINAL.docx
│
├── skills/                       ← knowledge base for AI tasks
│   ├── SKILL.md                  ← this file (master project skill)
│   ├── skills-create-doc.txt     ← field schema requirements for new SKILL.md files
│   ├── OSVi_Biomechanics_Demo_Database_DataDictionary.md
│   │
│   ├── harness/                  ← harness engineering pipeline skills
│   │   ├── 1_trial/SKILL.md      ← Trial agent: generate dashboard variants
│   │   ├── 2_role/SKILL.md       ← Role agent: define and maintain audience personas
│   │   ├── 3_tasks/SKILL.md      ← Tasks agent: execute user scenarios against variants
│   │   └── 4_evaluator/SKILL.md  ← Evaluator agent: score and rank variants
│   │
│   ├── shared/                   ← shared reference files used by multiple agents
│   │   ├── personas.md           ← audience persona definitions
│   │   ├── test_scenarios.md     ← user scenario test cases
│   │   └── scoring_rubric.md     ← evaluation criteria and scoring scales
│   │
│   ├── osvi-dashboard-guideline/ ← general OSVi dashboard design standards
│   │   └── SKILL.md
│   │
│   └── company-info/             ← OSVi organisational knowledge (from GitHub repo)
│       ├── osvi-clinical-capabilities/SKILL.md
│       ├── osvi-cordi-functions/SKILL.md
│       ├── osvi-identity/SKILL.md
│       └── osvi-people-structure/SKILL.md
│
├── tmp/
│   ├── OSVi_Biomechanics_Demo_Database.csv             ← demo database (2,000 rows × 155 cols)
│   └── OSVi_Biomechanics_Demo_Database_ORIGINAL_BACKUP.csv
│
├── harness.txt                   ← harness engineering briefing document
├── feedback.txt                  ← development feedback and pipeline notes
└── prototype.txt                 ← original project brief
```

---

## 3. The Demo Database

**File:** `tmp/OSVi_Biomechanics_Demo_Database.csv`
**Rows:** 2,000 | **Columns:** 155 (141 original + 14 from Registration) | **Unique patients:** 1,911
**Backup of original:** `tmp/OSVi_Biomechanics_Demo_Database_ORIGINAL_BACKUP.csv`

### Patient grain
One row = one assessment session for one patient. Longitudinal patients may have up to 4 rows (one per timepoint).

### Demographics columns (original)
| Column | Values |
|---|---|
| `Patient_ID` | ACL#####, TKR#####, ATH##### |
| `Age` | 14–60 years |
| `Sex` | Male (58.6%), Female (41.4%) |
| `Sport` | Australian Football, Cricket, Rugby, Basketball, Baseball |
| `Symptom` | ACLR (85.4%), TKR (10.2%), ATH (4.5%) |
| `Injury_Limb` | Left, Right |
| `Post_Surgery_Progress` | 3, 6, 9, 12, 15–30 months (null for ATH/pre-op) |

### Registration columns (integrated April 2026 from `ACLR_Rego_PROMS_Returnees_Master_2025.xlsx`)
Sourced from the Registration sheet (888 rows, 826 with ACL IDs). Matched to CSV by Patient_ID; unmatched rows randomly assigned from the observed value distribution.

| Column | Description | Example Values |
|---|---|---|
| `Height_cm` | Patient height in cm | 158–194 |
| `Weight_kg` | Patient weight in kg | 50–120 |
| `Competition_Level` | Sport participation tier | Recreational, Developmental, Competitive, Semi-Professional, Professional, National, Non-Athletic |
| `Dom_Jump_Leg` | Dominant jumping leg | Left, Right, Ambidextrous, Not Sure |
| `Dom_Kick_Leg` | Dominant kicking leg | Left, Right, Ambidextrous, Not Sure |
| `Injury_Mechanism` | How the ACL injury occurred | Contact, Non-contact, Other |
| `Surgical_Procedure` | Type of surgery performed | ACLR, ACLR (Non-LEAT), ACLR + LEAT, ACLR + Meniscus Repair |
| `Graft_Type` | ACL graft material used | Ipsilateral Hamstring, Contralateral Hamstring, Patellar Tendon (BTB), Quadriceps Tendon |
| `Surgeon` | Operating surgeon name | Timothy Whitehead, Cameron Norsworthy, Rohan Price, etc. |
| `Previous_ACLR` | History of prior ACL injury/surgery | Yes, No |
| `Other_LL_Injuries` | Other lower limb injury history | Yes, No, Not Sure |
| `Rehab_Freq_per_Week` | Rehab sessions per week (last 3 months) | 1 to 2, 2 to 3, 3 to 4, 4+ |
| `Rehab_Supervised` | Whether rehab was supervised | Yes, No, Partially |
| `Family_ACL_History` | Family history of ACL injury | Yes, No, Not Sure |

### Test categories (15 groups, 134 numeric columns)
1. Isokinetic Knee Extension Strength (Iso, Con, Ecc — absolute + relative + LSI)
2. Isokinetic Knee Flexion Strength (same structure)
3. Hamstring-to-Quadriceps Ratios (conventional + dynamic, L/R/LSI)
4. Ankle Plantarflexion Strength
5. Hip Adduction Strength
6. Hip Abduction Strength
7. Double Leg Countermovement Jump (DL CMJ)
8. Double Leg Drop Jump (DL DJ)
9. Double Leg 10-5 Repeated Hops
10. Single Leg Countermovement Jump (SL CMJ)
11. Single Leg Drop Jump (SL DJ)
12. Single Leg 10-5 Repeated Hops
13. Triple Forward Hop
14. Single Leg Squat — Concentric Peak Power

**For full column definitions, units, and clinical reference ranges, see:** `skills/OSVi_Biomechanics_Demo_Database_DataDictionary.md`

---

## 4. Critical Clinical Rules

These must be applied consistently in any analysis, chatbot response, or report:

### LSI (Limb Symmetry Index)
- **Formula:** Injured limb ÷ Uninjured limb × 100%
- **Return-to-sport threshold:** ≥ 90% (applies to all LSI columns)
- **Colour coding used in the prototype:**
  - Green: ≥ 90%
  - Amber: 80–89%
  - Red: < 80%

### Key clinical reference ranges
| Metric | Reference Range | Column(s) |
|---|---|---|
| DL Drop Jump RSI | 1.1–1.4 m/s | `rsidj_DL_` |
| SL Drop Jump RSI | 0.50–0.75 m/s | `rsidj_left_SL_`, `rsidj_right_SL_` |
| DL 10-5 RSI | 0.75–1.0 m/s | `105rsi_DL_` |
| SL 10-5 RSI | 0.40–0.50 m/s | `105rsiL_SL_`, `105rsiR_SL_` |
| DL CMJ jump height | 31–35 cm | `jhDL_` |
| SL CMJ jump height | 13–16 cm | `jhSL_L_`, `jhSL_R_` |
| Conventional H:Q ratio | 0.55–0.65 | `HQcc_L_`, `HQcc_R_` |
| Dynamic H:Q ratio | 0.75–0.85 | `HQec_L_`, `HQec_R_` |
| Ext isometric rel. torque | 3.0–4.0 Nm/kg | `ReExtIsoL_`, `ReExtIsoR_` |
| Ext concentric rel. torque | 2.5–3.5 Nm/kg | `ReExtConL_`, `ReExtConR_` |
| Fle isometric rel. torque | 1.75–2.5 Nm/kg | `ReFleIsoL_`, `ReFleIsoR_` |
| Ankle plantarflex rel. force | 1.5–2.0 BW | `ReLeft_`, `ReRight_` |
| Hip adduction rel. force | 0.45–0.55 BW | `ReAdLeft_`, `ReAdRight_` |
| Hip abduction rel. force | 0.40–0.50 BW | `ReAbLeft_`, `ReAbRight_` |

### Data completeness
- All 141 columns are 100% complete except `Post_Surgery_Progress` (4.5% null — expected for pre-surgical and ATH cohort)
- When n < 5 in a filtered cohort, always flag this as insufficient sample size

### LSI behaviour nuance
- Most LSI columns: mean ≈ 83%, SD ≈ 10% (reflects partially recovered population)
- **Exception — these LSIs have mean ≈ 100%** because they represent ratio/angle metrics that are inherently symmetric: `LSI_Jang_ext_`, `LSI_Jang_fle_`, `LSI_HQcc_`, `LSI_HQec_`, `LSI_ctSL_dj_`, `LSI_105ct_SL_`

---

## 5. Prototype Architecture

**How to run:**
```
cd prototype/
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "sk-ant-..."    # PowerShell
python app.py
# Open http://localhost:5050
```

### Backend — `app.py` endpoints
| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves `index.html` dashboard |
| `/api/demographics` | GET | Returns filter options + total record/patient counts |
| `/api/query` | POST | Filters data + returns summary statistics + histogram values |
| `/api/similar` | POST | Finds closest patients by category matching + age proximity |
| `/api/recovery` | POST | Returns population percentiles (P25/P50/P75) by post-surgery month |
| `/api/chat` | POST | Proxies user message + data context to Claude API |
| `/api/patient/<id>` | GET | Returns all rows for a specific patient ID |
| `/api/columns` | GET | Returns all column names grouped by category |

### Current similarity algorithm (basic)
1. Hard-filter on any selected values across all 18 filter fields (multi-select, exact match)
2. Rank remaining patients by absolute age difference from target
3. Return top N closest (default 15)

### Similar Patients — available filters (all multi-select)
**Demographics:** Sex, Sport, Condition (Symptom), Injury Limb, Post-Surgery Months, Competition Level
**Injury & Surgery:** Dominant Jump Leg, Dominant Kick Leg, Injury Mechanism, Surgical Procedure, Graft Type, Surgeon
**History & Rehab:** Previous ACLR, Other LL Injuries, Rehab Freq/Week, Rehab Supervised, Family ACL History

### Current red-flag logic (basic)
Only LSI columns are colour-coded: ≥90% green, 80–89% amber, <80% red. Non-LSI absolute metrics are not yet flagged.

### AI chatbot
- **Model:** claude-sonnet-4-20250514
- **Context injected:** full filtered data summary stats, demographic breakdown by current filter state
- **System prompt:** clinical biomechanics analyst persona with LSI rules and metric definitions
- **No conversation memory** between messages (each request is stateless)
- **API key:** must be set as `ANTHROPIC_API_KEY` environment variable — not stored in code

---

## 6. Harness Engineering Pipeline

OSVi uses a harness engineering approach to iteratively improve the dashboard. The pipeline
has four stages, each managed by a dedicated agent skill:

| Stage | Agent | Skill Location | Purpose |
|---|---|---|---|
| 1. Trial | osvi-harness-trial | `skills/harness/1_trial/SKILL.md` | Generate 2-3 distinct dashboard variants per run |
| 2. Role | osvi-harness-role | `skills/harness/2_role/SKILL.md` | Define and maintain audience personas |
| 3. Tasks | osvi-harness-tasks | `skills/harness/3_tasks/SKILL.md` | Execute user scenarios against each variant |
| 4. Evaluator | osvi-harness-evaluator | `skills/harness/4_evaluator/SKILL.md` | Score variants using a rubric and rank them |

**Pipeline flow:**
```
Role (personas) ──────────────────────────────────┐
                                                   ↓
Trial (generate variants) → Tasks (test) → Evaluator (score & rank)
                                                   ↓
                                          Best version selected
```

**Operational Execution Rules:**
1. **No Score Reporting:** When running the harness engineering pipeline, do not generate or output a detailed score report to the user. Simply select the highest-scoring variant and apply it to update the dashboard.
2. **Iterative Feedback:** After the dashboard is updated, the user will provide high-level, general feedback (not overly specific) which will be used by the pipeline to inform the next round of changes.

**Key reference files for the harness:**
- `harness.txt` — full briefing document (project context, personas, scenarios, rubric)
- `skills/shared/personas.md` — audience persona definitions
- `skills/shared/test_scenarios.md` — user scenario test cases (15 cases)
- `skills/shared/scoring_rubric.md` — evaluation criteria (7 factors, 1-3 scale)

**Dashboard design standards** are documented in `skills/osvi-dashboard-guideline/SKILL.md`.
This guideline applies to all OSVi dashboards, not just this prototype.

**Company context** (organisational identity, team structure, clinical capabilities, CORDi platform)
is stored in `skills/company-info/` — sourced from the osvi-cloud/osvi-claude-skills GitHub repository.

---

## 7. Known Limitations & Planned Improvements

| Area | Current state | Planned improvement |
|---|---|---|
| Similarity scoring | Age distance only after exact category matching | Weighted multi-factor score across demographics + biomechanical profile |
| Red flags | LSI threshold only | Add absolute metric thresholds (H:Q, RSI, relative torque) |
| AI context | Summary stats only | RAG — load documents from `prototype/knowledge/` folder at startup |
| Chatbot memory | Stateless per message | Pass full conversation history in each API call |
| AI tools | Free-text interpretation | Claude function calling for structured, validated queries |
| System prompt | Generic clinical description | Enrich with OSVi-specific protocols, decision trees, few-shot examples |

---

## 8. Key Abbreviations

| Abbreviation | Meaning |
|---|---|
| ACLR | Anterior Cruciate Ligament Reconstruction |
| TKR | Total Knee Replacement |
| ATH | Athletic (non-surgical comparison group) |
| LSI | Limb Symmetry Index |
| RTS | Return to Sport |
| DL / SL | Double Leg / Single Leg |
| CMJ | Countermovement Jump |
| DJ | Drop Jump |
| RSI | Reactive Strength Index |
| Nm | Newton-metres (torque) |
| N | Newtons (force) |
| N·s | Newton-seconds (impulse) |
| BW | Body Weight (normalisation) |
| W | Watts (power) |
| Iso / Con / Ecc | Isometric / Concentric / Eccentric |
| H:Q | Hamstring-to-Quadriceps ratio |
| P25 / P50 / P75 | 25th / 50th (median) / 75th percentile |

---

## 9. Working with the Project — Guidelines for AI Assistance

- **Always read this file first** before performing any task involving data analysis, code changes, reporting, or chatbot improvements.
- **For column definitions**, refer to `skills/OSVi_Biomechanics_Demo_Database_DataDictionary.md`.
- **For population statistics**, refer to `references/OSVi_Biomechanics_Demo_Database_DataSummary.md`.
- **For the clinical report format**, refer to the Word template in `references/`.
- When editing `app.py` or `index.html`, preserve the existing API contract — all endpoint paths and response schemas must remain backward compatible.
- When adding knowledge documents to `prototype/knowledge/`, prefer `.md` or `.txt` format for easy loading. PDFs require extraction first.
- Never hardcode the Anthropic API key into any source file.
- When reporting statistics, always include sample size (n) and flag n < 5 as insufficient.

---

## 10. Dashboard Editing — Noticed Things

> This section logs observations and standing rules that have come up during development. Update this section whenever something notable is discovered while editing the dashboard.

- **Keep SKILL.md in sync:** Once any change is made to `index.html` (dashboard UI/logic) or `app.py` (backend/API), review this SKILL.md and update it if the change affects architecture, API endpoints, clinical logic, red-flag thresholds, similarity scoring, or known limitations. Do not leave SKILL.md stale after a dashboard update.

- **Updating osvi-dashboard-guideline:** Not every change needs to be updated to osvi-dashboard-guideline. If the changes are more structural and whole picture stuff, then make the updates.

- **Tag picker UI (Similar Patients):** All `<select multiple>` dropdowns in the Similar Patients section have been replaced with a custom click-to-toggle tag picker component. Tags use `.tag-picker` (container) and `.tag-item` (individual pill) classes. Click once to select (blue), click again to deselect. No Ctrl key required. JS helpers: `buildTagPicker(containerId, values)` builds the picker, `getTagPicker(containerId)` returns the array of selected values.

- **`.sim-form` vs `.patient-form`:** The Similar Patients filter grids use a dedicated `.sim-form` class (scoped under `#panel-similar`) with `align-items: start`. This is intentionally different from other tabs that use `.patient-form` with `align-items: end` (needed for Recovery Trajectory button alignment). Do not merge these classes.

- **Age range filter:** The Similar Patients section uses `age_min` / `age_max` inputs (numeric, free text) instead of a dropdown. The similarity algorithm computes a midpoint and ranks by absolute age difference. When both fields are empty, the full age range (14–60) is used.

- **`Previous_ACLR` normalisation:** Raw Registration values were normalised to `Yes`, `No`, `Other` only. Any free-text entry that was not exactly "Yes" or "No" was mapped to "Other" (33 rows affected). Apply similar normalisation if other free-text columns develop messy values.

---

## 11. Metric Naming Convention

### Source of truth
All metric display names are defined in **`references/metric_labels.json`**.
- **Key** = the exact column/variable code used in the CSV and dashboard JS (`METRIC_LABELS` object in `index.html`).
- **Value** = the full clinical name shown to users, following the naming pattern from the OSVi Performance Report template (`references/2026_MARCH_WORKING TEMPLATE_PERFORMANCE REPORT_L4_MALES_Follow-up_FINAL.docx`).

### Naming pattern (derived from the template)
Follow this pattern exactly when adding new metrics:

| Component | Rule | Examples |
|---|---|---|
| **Contraction type first** | Isometric / Concentric / Eccentric | `Isometric Knee Extension` |
| **Movement second** | Anatomical name | `Knee Extension`, `Hip Abduction` |
| **Qualifier third** | Relative / Peak Torque at 200ms / Joint Angle / etc. | `Relative Isometric Knee Extension` |
| **Side suffix** | `— Left`, `— Right`, `— LSI (%)` | `Isometric Knee Extension — Left (Nm)` |
| **Units in brackets** | Always include unit | `(Nm)`, `(Nm/kg)`, `(N)`, `(BW)`, `(cm)`, `(m/s)`, `(N·s)`, `(W)`, `(s)`, `(°)` |
| **Double vs Single Leg** | `Double Leg` / `Single Leg` prefix for force plate tasks | `Double Leg CMJ Jump Height (cm)` |
| **Task abbreviations** | CMJ, DJ, RSI, CPP — match the template's exact abbreviations | `Single Leg Drop Jump RSI — LSI (%)` |

### Rules
1. **Only ever add** entries to `metric_labels.json` — never delete or rename existing keys (the key is a CSV column name; renaming breaks data loading).
2. When Edward notifies that the report template (`references/*.docx`) has been updated with new metrics, you must:
   a. Read the updated template using `pandoc` to extract new column codes and their context.
   b. Add the new entries to `references/metric_labels.json` following the naming pattern above.
   c. Add the new keys to `METRIC_LABELS` in `prototype/index.html` with the same value strings.
   d. Update this SKILL.md if the new metrics introduce a new section or category.
3. Section-header keys (e.g. `"STRENGTH — KNEE EXTENSION"`) are decorative separators in the JSON — they are **not** valid metric codes and must never be added to the dashboard `METRIC_LABELS`.
4. The dashboard `METRIC_LABELS` object in `index.html` only needs to contain metrics that are actually selectable in the UI (LSI metrics + key absolute metrics). Raw left/right absolute columns (e.g. `ExtIsoL_`, `ReExtIsoL_`) are in the JSON for completeness but do not need to be in the dashboard selector unless a new feature requires them.

### File locations
- Naming source of truth: `references/metric_labels.json`
- Dashboard metric selector: `METRIC_LABELS` const in `prototype/index.html` (~line 424)
- Report template: `references/2026_MARCH_WORKING TEMPLATE_PERFORMANCE REPORT_L4_MALES_Follow-up_FINAL.docx`

---

*Last updated: April 2026 (harness engineering pipeline, dashboard guideline, company-info skills, updated folder structure) | Project: OSVi Clinical Population Data Query System*
