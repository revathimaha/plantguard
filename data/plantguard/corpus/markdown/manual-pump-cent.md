# Centrifugal Process Pump (PUMP-CENT) Equipment Manual and SOP

**VINDHYA PRECISION WORKS**
**STANDARD OPERATING PROCEDURE & EQUIPMENT MANUAL**
**Document ID:** VPW-SOP-ENG-PUMP-CENT-042
**Asset Class:** PUMP-CENT (Centrifugal Process Pump)
**Effective Date:** 14 January 2026
**Maintenance Discipline:** Mechanical (Primary), Instrumentation (Support)

---

### 1.0 ASSET OVERVIEW AND SCOPE

1.1 This document defines the operating limits, preventive maintenance schedules, fault diagnosis protocols, torque specifications, and safety-critical isolation procedures for all Centrifugal Process Pumps (Asset Class: PUMP-CENT) installed across Vindhya Precision Works.

1.2 The parameters, limits, and part numbers contained in this manual are specific to asset class PUMP-CENT and shall not be applied to positive displacement pumps, screw compressors, or auxiliary blowers.

---

### 2.0 NORMAL OPERATING RANGES AND CONDITION MONITORING SETPOINTS

2.1 Healthy units within asset class PUMP-CENT operate within the baseline parameters defined in Table 2.1.

**Table 2.1: Baseline Operating Ranges and Alarm Setpoints**
| Parameter | Healthy Operating Range | Warning Setpoint | Trip Setpoint |
| :--- | :--- | :--- | :--- |
| **Vibration (RMS Velocity)** | $1.2\text{--}4.0\text{ mm/s}$ | $5.0\text{ mm/s}$ | $8.0\text{ mm/s}$ |
| **Surface Temperature** | $38\text{--}66\ ^\circ\text{C}$ | $75\ ^\circ\text{C}$ | $90\ ^\circ\text{C}$ |
| **Operating Pressure** | $4.2\text{ bar}$ (nominal) | $3.4\text{ bar}$ (Low-Pressure Alarm) | N/A |
| **Motor Current** | $28.0\text{--}34.5\text{ Amps}$ | $38.0\text{ Amps}$ | $42.0\text{ Amps}$ |

2.2 Any reading exceeding the Warning Setpoint shall be logged by the condition-monitoring system and reported to the Mechanical Maintenance Lead within two (2) operating shifts.

2.3 Any reading reaching the Trip Setpoint shall automatically de-energize the pump motor via the Plant Distributed Control System (DCS) within 500 milliseconds and trigger a high-priority technician dispatch.

---

### 3.0 PREVENTIVE MAINTENANCE (PM) SCHEDULE

3.1 The base preventive maintenance interval for asset class PUMP-CENT is exactly **4000 running hours**, or every 180 calendar days, whichever occurs first.

3.2 **PM-1 (Every 1000 Running Hours):** Inspect mechanical seal flush lines for obstruction; record motor current and bearing housing vibration signatures manually; verify lubrication levels in the bearing housings.

3.3 **PM-2 (Every 4000 Running Hours - Minor Overhaul):** Execute full machinery shutdown, apply mandatory lock-out/tag-out (LOTO), replace VPW-P-00007 (Rate filter) and VPW-P-00023 (Discussion filter), inspect impeller clearance, and test trip interlocks.

3.4 **PM-3 (Every 12000 Running Hours - Major Overhaul):** Complete disassembly of pump wet-end; replace rotating assembly bearings using VPW-P-00020 (Once bearing) and VPW-P-00031 (Western bearing); replace shaft sealing elements using VPW-P-00026 (Second seal) and VPW-P-00030 (Author seal); recalibrate instrumentation via VPW-P-00011 (Nation sensor).

---

### 4.0 FAULT CODES AND DIAGNOSTIC PROSE

4.1 **Fault Code FC-PC-101 (High Vibration):** Probable causes include pump-motor shaft misalignment exceeding 0.05 mm, cavitation due to inlet starvation, or bearing raceway spalling. Corrective action: Check laser alignment of coupling; verify suction pressure is $\ge 3.4\text{ bar}$; if vibration persists above $8.0\text{ mm/s}$ trip threshold after alignment, replace bearings VPW-P-00020 and VPW-P-00031.

4.2 **Fault Code FC-PC-102 (High Surface Temperature):** Probable causes include dry running, degraded bearing grease, or external friction from the mechanical seal faces. Corrective action: Stop pump immediately if temperature reaches $90\ ^\circ\text{C}$; inspect seal flush line fitted with VPW-P-00023 (Discussion filter) for blockages; clean or replace filter element; repack bearing cavities with high-temperature synthetic grease.

4.3 **Fault Code FC-PC-103 (Low Operating Pressure):** Probable causes include worn impeller wear rings, air entrainment in the suction header, or a partially closed suction isolation valve (VPW-P-00033). Corrective action: Verify valve position on VPW-P-00033; bleed air from casing vent port; inspect internal hydraulic clearances; replace worn wear rings if differential head drops below $3.1\text{ bar}$ at rated speed.

4.4 **Fault Code FC-PC-104 (Motor Overcurrent):** Probable causes include process fluid specific gravity exceeding design limits ($\text{SG} > 1.15$), mechanical rub between the impeller and casing, or motor winding phase imbalance. Corrective action: Measure phase-to-phase electrical resistance; inspect pump wet-end for foreign debris; verify process fluid density via laboratory sampling.

4.5 **Fault Code FC-PC-105 (Seal Leakage / Flush Failure):** Probable causes include particulate scoring of seal faces or restriction in the internal flush circuit. Corrective action: Isolate hydraulic energy; remove and inspect mechanical seal assembly; replace secondary seal components VPW-P-00026 and VPW-P-00030; inspect and replace inline particulate filter VPW-P-00007.

4.6 **Fault Code FC-PC-106 (Instrumentation Drift / Fault):** Probable causes include electronic calibration drift, signal loop degradation, or sensor tip fouling. Corrective action: Instrument technician to cross-check local gauge readings against DCS input; recalibrate or replace faulty sensor element VPW-P-00011 (Nation sensor) in accordance with calibration SOP VPW-SOP-INS-019.

---

### 5.0 CONSUMABLE AND SPARE PARTS LIST

5.1 Maintenance technicians shall strictly use the plant inventory part numbers listed in Table 5.1 for all maintenance and overhaul activities on asset class PUMP-CENT. No substitutions are permitted without prior written authorization from the Engineering Manager.

**Table 5.1: Inventory Spare Parts and Consumables**
| Inventory Part Number | Part Description |
| :--- | :--- |
| **VPW-P-00007** | Rate filter |
| **VPW-P-00011** | Nation sensor |
| **VPW-P-00020** | Once bearing |
| **VPW-P-00023** | Discussion filter |
| **VPW-P-00026** | Second seal |
| **VPW-P-00030** | Author seal |
| **VPW-P-00031** | Western bearing |
| **VPW-P-00033** | Trade valve |

---

### 6.0 TORQUE SPECIFICATIONS

6.1 All mechanical fasteners associated with asset class PUMP-CENT shall be tightened using calibrated torque wrenches in a star-pattern sequence to the specific limits set forth in Table 6.1.

**Table 6.1: Fastener Torque Limits**
| Fastener Location | Thread Size | Target Torque ($\text{Nm}$) |
| :--- | :--- | :--- |
| Casing Bolt / Studs | M16 | $115\text{ Nm} \pm 5\%$ |
| Bearing Housing Cap Screws | M10 | $45\text{ Nm} \pm 5\%$ |
| Coupling Hub Clamp Bolts | M12 | $78\text{ Nm} \pm 5\%$ |
| Seal Gland Nuts | M8 | $22\text{ Nm} \pm 5\%$ |
| Baseplate Anchor Bolts | M20 | $180\text{ Nm} \pm 10\%$ |

---

### 7.0 HAZARDOUS ENERGY ISOLATION AND SAFETY-CRITICAL CORRECTIVE ACTIONS

7.1 **Hazardous Energy Sources:** Prior to initiating any invasive maintenance, disassembly, or corrective work on asset class PUMP-CENT, technicians must isolate two (2) primary hazardous energy sources:
1. **Electrical Energy:** 415V AC 3-phase supply via motor control center (MCC) breaker rack-out and padlocked tag-out.
2. **Hydraulic Energy:** Process fluid pressure via positive closure of suction and discharge isolation valves (including Trade valve VPW-P-00033), followed by atmospheric venting and draining of the pump casing.

7.2 **Safety-Critical Corrective Actions:** The following corrective actions are classified as safety-critical. They strictly mandate the execution of a formal Lockout/Tagout (LOTO) procedure under an active Permit to Work (PTW) issued by the Shift Safety Officer:
* Replacement or adjustment of mechanical seals (involving components VPW-P-00026 and VPW-P-00030) on pumps handling hazardous or corrosive process media.
* Disconnection of primary electrical power leads at the motor terminal box.
* Replacement of rotating element bearings (VPW-P-00020 and VPW-P-00031) requiring overhead crane lifting or heavy rigging.
* Opening of the pump casing or associated piping spool pieces where residual chemical or thermal energy may be trapped behind closed valves.

7.3 Non-invasive tasks—such as replacing exterior instrumentation filters (VPW-P-00007, VPW-P-00023), reading vibration signatures, or inspecting non-pressure-retaining safety guards—may be performed under a standard plant maintenance clearance without a formal PTW, provided running machinery is not contacted.
