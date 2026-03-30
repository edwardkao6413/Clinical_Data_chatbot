# OSVi Biomechanics Demo Database — Data Dictionary

**Source file:** `OSVi_Biomechanics_Demo_Database.csv`
**Total rows:** 2,000 | **Total columns:** 141
**Grain:** One row per patient per assessment timepoint
**Last updated:** March 2026

> **Key abbreviations used throughout:**
> LSI = Limb Symmetry Index (injured ÷ uninjured leg × 100%); a score ≥90% is the standard return-to-sport threshold.
> BW = Bodyweight; Nm = Newton-metres; N = Newtons; N·s = Newton-seconds; W = Watts; cm = centimetres; s = seconds; m/s = metres per second.
> KF = Knee Flexion angle; HF = Hip Flexion angle.
> DL = Double Leg; SL = Single Leg; CMJ = Countermovement Jump; DJ = Drop Jump.

---

## 1. Patient Demographics & Administrative

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `Patient_ID` | String | Unique patient identifier. Format: prefix (ACL/TKR/ATH) + 5-digit number (e.g. `ACL00450`). A patient may appear in multiple rows if assessed at multiple timepoints. |
| `Age` | Integer | Patient age in years at the time of assessment. Range: 14–60. |
| `Sex` | String | Biological sex of the patient. Values: `Male`, `Female`. |
| `Sport` | String | Primary sport played by the patient. Values: `Australian Football`, `Cricket`, `Rugby`, `Basketball`, `Baseball`. |
| `Symptom` | String | Clinical diagnosis or patient category. Values: `ACLR` (ACL Reconstruction), `TKR` (Total Knee Replacement), `ATH` (Athletic / non-surgical comparison group). |
| `Injury_Limb` | String | The limb that was injured or operated on. Values: `Left`, `Right`. |
| `Post_Surgery_Progress` | Float | Months elapsed since surgery at the time of this assessment. Primary checkpoints: 3, 6, 9, 12 months. Extended follow-up: 15–30 months. Null for pre-surgical or athletic (ATH) assessments. |

---

## 2. Isokinetic Strength — Knee Extension

> Measured on a Humac isokinetic dynamometer, patient seated. Isometric tests at 60° of knee flexion; concentric and eccentric tests at 60°/second.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `ExtIsoL_` | Float | Knee extension **isometric** peak torque — **Left** leg (Nm). Maximum force produced during a static hold against resistance. |
| `ExtIsoR_` | Float | Knee extension **isometric** peak torque — **Right** leg (Nm). |
| `ExtIsoLSI_` | Float | Knee extension isometric peak torque **Limb Symmetry Index** (%). Left ÷ Right × 100 (or injured ÷ uninjured × 100). Clinical target ≥90%. |
| `ReExtIsoL_` | Float | Knee extension isometric **relative** peak torque — **Left** leg (Nm/kg). Peak torque normalised to body mass. Reference range: 3.0–4.0 Nm/kg. |
| `ReExtIsoR_` | Float | Knee extension isometric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 3.0–4.0 Nm/kg. |
| `IsoPt200L_ext_` | Float | Knee extension isometric **peak torque at 200 milliseconds** — **Left** leg (Nm). Reflects early rate of torque development, an indicator of explosive quadriceps activation. |
| `IsoPt200R_ext_` | Float | Knee extension isometric **peak torque at 200 milliseconds** — **Right** leg (Nm). |
| `LSI_Isopt200_ext_` | Float | Knee extension peak torque at 200ms **Limb Symmetry Index** (%). |
| `ExtConL_` | Float | Knee extension **concentric** peak torque — **Left** leg (Nm). Torque during active shortening of the quadriceps muscle. |
| `ExtConR_` | Float | Knee extension **concentric** peak torque — **Right** leg (Nm). |
| `ExtConLSI_` | Float | Knee extension concentric peak torque **Limb Symmetry Index** (%). |
| `ReExtConL_` | Float | Knee extension concentric **relative** peak torque — **Left** leg (Nm/kg). Reference range: 2.5–3.5 Nm/kg. |
| `ReExtConR_` | Float | Knee extension concentric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 2.5–3.5 Nm/kg. |
| `Jang_ptL_ext_` | Float | Knee extension **joint angle at peak torque** — **Left** leg (degrees). The knee flexion angle at which maximum concentric extension torque is produced. Reference range: 45–65°. |
| `Jang_ptR_ext_` | Float | Knee extension **joint angle at peak torque** — **Right** leg (degrees). Reference range: 45–65°. |
| `LSI_Jang_ext_` | Float | Knee extension joint angle at peak torque **Limb Symmetry Index** (%). Values near 100% indicate symmetrical torque curve profiles between limbs. |
| `ExtEccL_` | Float | Knee extension **eccentric** peak torque — **Left** leg (Nm). Torque produced while the quadriceps muscle is lengthening under load. |
| `ExtEccR_` | Float | Knee extension **eccentric** peak torque — **Right** leg (Nm). |
| `ExtEccLSI_` | Float | Knee extension eccentric peak torque **Limb Symmetry Index** (%). |
| `ReExtEccL_` | Float | Knee extension eccentric **relative** peak torque — **Left** leg (Nm/kg). Reference range: 3.5–4.5 Nm/kg. |
| `ReExtEccR_` | Float | Knee extension eccentric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 3.5–4.5 Nm/kg. |

---

## 3. Isokinetic Strength — Knee Flexion

> Measured on a Humac isokinetic dynamometer, patient seated. Isometric tests at 30° of knee flexion; concentric and eccentric tests at 60°/second.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `FleIsoL_` | Float | Knee flexion **isometric** peak torque — **Left** leg (Nm). Maximum hamstring force during a static hold. |
| `FleIsoR_` | Float | Knee flexion **isometric** peak torque — **Right** leg (Nm). |
| `FleIsoLSI_` | Float | Knee flexion isometric peak torque **Limb Symmetry Index** (%). |
| `ReFleIsoL_` | Float | Knee flexion isometric **relative** peak torque — **Left** leg (Nm/kg). Reference range: 1.75–2.5 Nm/kg. |
| `ReFleIsoR_` | Float | Knee flexion isometric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 1.75–2.5 Nm/kg. |
| `IsoPt200L_fle_` | Float | Knee flexion isometric **peak torque at 200 milliseconds** — **Left** leg (Nm). Reflects rate of hamstring torque development. |
| `IsoPt200R_fle_` | Float | Knee flexion isometric **peak torque at 200 milliseconds** — **Right** leg (Nm). |
| `LSI_Isopt200_fle_` | Float | Knee flexion peak torque at 200ms **Limb Symmetry Index** (%). |
| `FleConL_` | Float | Knee flexion **concentric** peak torque — **Left** leg (Nm). Hamstring torque during active shortening. |
| `FleConR_` | Float | Knee flexion **concentric** peak torque — **Right** leg (Nm). |
| `FleConLSI_` | Float | Knee flexion concentric peak torque **Limb Symmetry Index** (%). |
| `ReFleConL_` | Float | Knee flexion concentric **relative** peak torque — **Left** leg (Nm/kg). Reference range: 1.5–2.0 Nm/kg. |
| `ReFleConR_` | Float | Knee flexion concentric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 1.5–2.0 Nm/kg. |
| `Jang_ptL_fle_` | Float | Knee flexion **joint angle at peak torque** — **Left** leg (degrees). Reference range: 25–45°. |
| `Jang_ptR_fle_` | Float | Knee flexion **joint angle at peak torque** — **Right** leg (degrees). Reference range: 25–45°. |
| `LSI_Jang_fle_` | Float | Knee flexion joint angle at peak torque **Limb Symmetry Index** (%). |
| `FleEccL_` | Float | Knee flexion **eccentric** peak torque — **Left** leg (Nm). Hamstring force while lengthening under load (key injury-prevention metric). |
| `FleEccR_` | Float | Knee flexion **eccentric** peak torque — **Right** leg (Nm). |
| `FleEccLSI_` | Float | Knee flexion eccentric peak torque **Limb Symmetry Index** (%). |
| `ReFleEccL_` | Float | Knee flexion eccentric **relative** peak torque — **Left** leg (Nm/kg). Reference range: 2.0–3.0 Nm/kg. |
| `ReFleEccR_` | Float | Knee flexion eccentric **relative** peak torque — **Right** leg (Nm/kg). Reference range: 2.0–3.0 Nm/kg. |

---

## 4. Hamstring-to-Quadriceps (H:Q) Ratios

> Derived from isokinetic strength values. Indicates the balance between hamstring and quadriceps strength, an important ACL injury risk marker.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `HQcc_L_` | Float | **Conventional H:Q ratio** (concentric hamstring ÷ concentric quadriceps) — **Left** leg. Reference range: 0.55–0.65. A low ratio suggests relative quadriceps dominance. |
| `HQcc_R_` | Float | **Conventional H:Q ratio** — **Right** leg. Reference range: 0.55–0.65. |
| `LSI_HQcc_` | Float | Conventional H:Q ratio **Limb Symmetry Index** (%). Values near 100% indicate balanced H:Q profiles between limbs. |
| `HQec_L_` | Float | **Dynamic (functional) H:Q ratio** (eccentric hamstring ÷ concentric quadriceps) — **Left** leg. Reference range: 0.75–0.85. A superior indicator of dynamic knee joint protection. |
| `HQec_R_` | Float | **Dynamic H:Q ratio** — **Right** leg. Reference range: 0.75–0.85. |
| `LSI_HQec_` | Float | Dynamic H:Q ratio **Limb Symmetry Index** (%). |

---

## 5. Ankle Plantarflexion Strength

> Measured on a VALD ForceFrame, patient seated with knee at 90° of flexion. Force in Newtons.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `PlLeft_` | Float | Ankle plantarflexion isometric **peak force** — **Left** leg (N). Calf strength assessment. |
| `PlRight_` | Float | Ankle plantarflexion isometric **peak force** — **Right** leg (N). |
| `PlLSI_` | Float | Ankle plantarflexion peak force **Limb Symmetry Index** (%). |
| `ReLeft_` | Float | Ankle plantarflexion **relative** peak force — **Left** leg (body weight multiples, BW). Reference range: 1.5–2.0 BW. |
| `ReRight_` | Float | Ankle plantarflexion **relative** peak force — **Right** leg (BW). Reference range: 1.5–2.0 BW. |

---

## 6. Hip Adduction Strength

> Measured on a VALD ForceFrame, patient supine with 45° of hip flexion.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `AdLeft_` | Float | Hip adduction isometric **peak force** — **Left** leg (N). Groin/inner thigh strength. |
| `AdRight_` | Float | Hip adduction isometric **peak force** — **Right** leg (N). |
| `AdLSI_` | Float | Hip adduction peak force **Limb Symmetry Index** (%). |
| `ReAdLeft_` | Float | Hip adduction **relative** peak force — **Left** leg (BW). Reference range: 0.45–0.55 BW. |
| `ReAdRight_` | Float | Hip adduction **relative** peak force — **Right** leg (BW). Reference range: 0.45–0.55 BW. |

---

## 7. Hip Abduction Strength

> Measured on a VALD ForceFrame, patient supine with 45° of hip flexion.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `AbLeft_` | Float | Hip abduction isometric **peak force** — **Left** leg (N). Gluteal / outer hip strength. |
| `AbRight_` | Float | Hip abduction isometric **peak force** — **Right** leg (N). |
| `AbLSI_` | Float | Hip abduction peak force **Limb Symmetry Index** (%). |
| `ReAbLeft_` | Float | Hip abduction **relative** peak force — **Left** leg (BW). Reference range: 0.40–0.50 BW. |
| `ReAbRight_` | Float | Hip abduction **relative** peak force — **Right** leg (BW). Reference range: 0.40–0.50 BW. |

---

## 8. Double Leg Countermovement Jump (DL CMJ)

> Performed on VALD ForceDecks, hands on hips, best of three trials. Measures bilateral jumping power and limb loading symmetry.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `jhDL_` | Float | Double leg CMJ **jump height** (cm). The height the centre of mass rises above the starting position. Reference range: 31–35 cm. |
| `EcDel_DLCMJ_L_` | Float | DL CMJ **eccentric deceleration impulse** — **Left** leg (N·s). Force-time area during the braking/lowering phase of the jump. Reflects the ability to control descent asymmetrically. |
| `EcDel_DLCMJ_R_` | Float | DL CMJ **eccentric deceleration impulse** — **Right** leg (N·s). |
| `LSI_EcDel_DLCMJ_` | Float | DL CMJ eccentric deceleration impulse **Limb Symmetry Index** (%). |
| `ci_left_DL_` | Float | DL CMJ **concentric impulse** — **Left** leg (N·s). Force-time area during the propulsion/push-off phase. |
| `ci_right_DL_` | Float | DL CMJ **concentric impulse** — **Right** leg (N·s). |
| `LSI_ci_DL_` | Float | DL CMJ concentric impulse **Limb Symmetry Index** (%). |
| `pf_left_DL_` | Float | DL CMJ **relative peak landing force** — **Left** leg (N/BW). Peak force at ground contact upon landing, normalised to body weight. |
| `pf_right_DL_` | Float | DL CMJ **relative peak landing force** — **Right** leg (N/BW). |
| `LSI_pf_DL_` | Float | DL CMJ relative peak landing force **Limb Symmetry Index** (%). |

---

## 9. Double Leg Drop Jump (DL DJ)

> Performed on VALD ForceDecks. Patient drops from a box and immediately jumps maximally. Tests reactive and plyometric ability under bilateral loading.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `rsidj_DL_` | Float | DL drop jump **Reactive Strength Index** (m/s). Jump height ÷ ground contact time. The gold-standard measure of plyometric efficiency. Reference range: 1.1–1.4 m/s. |
| `jhDL_dj_` | Float | DL drop jump **jump height** (cm). |
| `ct_DL_dj_` | Float | DL drop jump **ground contact time** (s). Duration of foot contact with the force plate between landing and take-off. |
| `asi_DL_dj_` | Float | DL drop jump **active stiffness index** (N). A measure of lower limb stiffness during ground contact; higher values indicate stiffer, more spring-like mechanics. |
| `dof_DL_L_` | Float | DL drop jump **drive-off force** — **Left** leg (N). Peak force produced during the propulsive push-off phase. |
| `dof_DL_R_` | Float | DL drop jump **drive-off force** — **Right** leg (N). |
| `LSI_dof_DL_` | Float | DL drop jump drive-off force **Limb Symmetry Index** (%). |
| `pk_left_DLdj_` | Float | DL drop jump **relative peak landing force** — **Left** leg (N/BW). Peak impact force on landing, normalised to body weight. |
| `pk_right_DLdj_` | Float | DL drop jump **relative peak landing force** — **Right** leg (N/BW). |
| `LSI_pk_DLDJ_` | Float | DL drop jump relative peak landing force **Limb Symmetry Index** (%). |

---

## 10. Double Leg 10-5 Repeated Hops (DL 10-5)

> A bilateral repeated-hop protocol: 10 consecutive hops with a 5-second rest cycle. Assesses repeated plyometric endurance and ankle stiffness.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `105rsi_DL_` | Float | DL 10-5 repeated hops **Reactive Strength Index** (m/s). Average jump height ÷ average ground contact time across all repetitions. Reference range: 0.75–1.0 m/s. |
| `105jh_DL_` | Float | DL 10-5 repeated hops **average jump height** (cm). |
| `105ct_DL_` | Float | DL 10-5 repeated hops **average ground contact time** (s). |

---

## 11. Single Leg Countermovement Jump (SL CMJ)

> Performed on VALD ForceDecks, one leg at a time. Tests unilateral vertical power and reveals side-to-side asymmetries in jump mechanics.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `jhSL_L_` | Float | SL CMJ **jump height** — **Left** leg (cm). Reference range: 13–16 cm. |
| `jhSL_R_` | Float | SL CMJ **jump height** — **Right** leg (cm). Reference range: 13–16 cm. |
| `LSI_jhSL_` | Float | SL CMJ jump height **Limb Symmetry Index** (%). |
| `EcBra_SLCMJL_` | Float | SL CMJ **eccentric braking impulse** — **Left** leg (N·s). The impulse produced during the initial braking/deceleration phase of the jump. Reflects the ability to load and control the limb during descent. |
| `EcBra_SLCMJR_` | Float | SL CMJ **eccentric braking impulse** — **Right** leg (N·s). |
| `LSI_EcBra_SLCMJ_` | Float | SL CMJ eccentric braking impulse **Limb Symmetry Index** (%). |
| `EcDel_SLCMJL_` | Float | SL CMJ **eccentric deceleration impulse** — **Left** leg (N·s). Impulse during the full downward phase before propulsion. |
| `EcDel_SLCMJR_` | Float | SL CMJ **eccentric deceleration impulse** — **Right** leg (N·s). |
| `LSI_EcDel_SLCMJ_` | Float | SL CMJ eccentric deceleration impulse **Limb Symmetry Index** (%). |
| `ci_left_SL_` | Float | SL CMJ **total concentric impulse** — **Left** leg (N·s). Total force-time area during the push-off phase. |
| `ci_right_SL_` | Float | SL CMJ **total concentric impulse** — **Right** leg (N·s). |
| `LSI_ci_SL_` | Float | SL CMJ total concentric impulse **Limb Symmetry Index** (%). |
| `ciP1_left_SL_` | Float | SL CMJ **concentric impulse — early phase** — **Left** leg (N·s). Force-time area in the first portion of the propulsion phase, reflecting initial explosive drive. |
| `ciP1_right_SL_` | Float | SL CMJ **concentric impulse — early phase** — **Right** leg (N·s). |
| `LSI_ciP1_SL_` | Float | SL CMJ concentric impulse early phase **Limb Symmetry Index** (%). |
| `ciP2_left_SL_` | Float | SL CMJ **concentric impulse — late phase** — **Left** leg (N·s). Force-time area in the final portion of the propulsion phase, reflecting terminal push-off capacity. |
| `ciP2_right_SL_` | Float | SL CMJ **concentric impulse — late phase** — **Right** leg (N·s). |
| `LSI_ciP2_SL_` | Float | SL CMJ concentric impulse late phase **Limb Symmetry Index** (%). |

---

## 12. Single Leg Drop Jump (SL DJ)

> Performed on VALD ForceDecks, one leg at a time. The most demanding plyometric assessment; reveals unilateral reactive strength and landing mechanics deficits.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `rsidj_left_SL_` | Float | SL drop jump **Reactive Strength Index** — **Left** leg (m/s). Reference range: 0.50–0.75 m/s. |
| `rsidj_right_SL_` | Float | SL drop jump **Reactive Strength Index** — **Right** leg (m/s). Reference range: 0.50–0.75 m/s. |
| `LSI_rsidj_SL_` | Float | SL drop jump RSI **Limb Symmetry Index** (%). |
| `jhSL_djL_` | Float | SL drop jump **jump height** — **Left** leg (cm). |
| `jhSL_djR_` | Float | SL drop jump **jump height** — **Right** leg (cm). |
| `LSI_jhSL_dj_` | Float | SL drop jump jump height **Limb Symmetry Index** (%). |
| `ct_SL_djL_` | Float | SL drop jump **ground contact time** — **Left** leg (s). Reference range: 0.22–0.27 s. Shorter contact times indicate more reactive, stiff ankle mechanics. |
| `ct_SL_djR_` | Float | SL drop jump **ground contact time** — **Right** leg (s). Reference range: 0.22–0.27 s. |
| `LSI_ctSL_dj_` | Float | SL drop jump ground contact time **Limb Symmetry Index** (%). |
| `act_SL_djL_` | Float | SL drop jump **active stiffness index** — **Left** leg (N). Unilateral lower limb stiffness during the reactive ground contact phase. |
| `act_SL_djR_` | Float | SL drop jump **active stiffness index** — **Right** leg (N). |
| `LSI_act_SL_dj_` | Float | SL drop jump active stiffness index **Limb Symmetry Index** (%). |
| `dof_SL_L_` | Float | SL drop jump **drive-off force** — **Left** leg (N). Peak propulsive force during the push-off phase. |
| `dof_SL_R_` | Float | SL drop jump **drive-off force** — **Right** leg (N). |
| `LSI_dof_SL_` | Float | SL drop jump drive-off force **Limb Symmetry Index** (%). |

---

## 13. Single Leg 10-5 Repeated Hops (SL 10-5)

> A unilateral repeated-hop protocol performed separately on each leg. Reference range for RSI: 0.40–0.50 m/s.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `105rsiL_SL_` | Float | SL 10-5 repeated hops **Reactive Strength Index** — **Left** leg (m/s). Reference range: 0.40–0.50 m/s. |
| `105rsiR_SL_` | Float | SL 10-5 repeated hops **Reactive Strength Index** — **Right** leg (m/s). Reference range: 0.40–0.50 m/s. |
| `LSI_105rsi_SL_` | Float | SL 10-5 RSI **Limb Symmetry Index** (%). |
| `105jhL_SL_` | Float | SL 10-5 repeated hops **average jump height** — **Left** leg (cm). |
| `105jhR_SL_` | Float | SL 10-5 repeated hops **average jump height** — **Right** leg (cm). |
| `LSI_105jh_SL_` | Float | SL 10-5 jump height **Limb Symmetry Index** (%). |
| `105ctL_SL_` | Float | SL 10-5 repeated hops **average ground contact time** — **Left** leg (s). |
| `105ctR_SL_` | Float | SL 10-5 repeated hops **average ground contact time** — **Right** leg (s). |
| `LSI_105ct_SL_` | Float | SL 10-5 ground contact time **Limb Symmetry Index** (%). |

---

## 14. Triple Forward Hop

> A horizontal hop test performed on each leg separately. Patient performs three consecutive forward hops and the total distance is recorded. Tests horizontal power and landing mechanics.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `triforhop_L_` | Float | Triple forward hop **total distance** — **Left** leg (cm). Sum of three consecutive single-leg forward hops. |
| `triforhop_R_` | Float | Triple forward hop **total distance** — **Right** leg (cm). |
| `LSI_triforhop_` | Float | Triple forward hop distance **Limb Symmetry Index** (%). |

---

## 15. Single Leg Squat — Concentric Peak Power

> Performed on VALD ForceDecks. Measures explosive lower limb power during a unilateral squat movement.

| Column Name | Data Type | Plain English Description |
|---|---|---|
| `sq_cppL_` | Float | Single leg squat **concentric peak power** — **Left** leg (Watts). The maximum power output during the propulsive upward phase of the squat. |
| `sq_cppR_` | Float | Single leg squat **concentric peak power** — **Right** leg (Watts). |
| `LSI_sqcpp_` | Float | Single leg squat concentric peak power **Limb Symmetry Index** (%). |

---

*Data dictionary compiled from the OSVi Biomechanics & Performance Lab reporting template and column naming conventions. For clinical reference values and testing protocols, refer to the OSVi Performance Report template.*
