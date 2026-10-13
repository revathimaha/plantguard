# 400-Tonne Hydraulic Press (HYD-PRESS) Equipment Manual and SOP

# VINDHYA PRECISION WORKS
## MAINTENANCE ENGINEERING DIVISION
### STANDARD OPERATING PROCEDURE: ASSET CLASS HYD-PRESS
**Document ID:** SOP-HYD-400T-04  
**Applies To:** 400-Tonne Hydraulic Press (Assets HYD-01 through HYD-06)  
**Effective Date:** 14 January 2025  

---

## 1. PURPOSE AND SCOPE
This document defines the mandatory operating limits, condition-monitoring thresholds, preventive maintenance schedules, fault isolation procedures, torque specifications, and consumable part numbers for the 400-Tonne Hydraulic Press (Asset Class HYD-PRESS). Compliance with this procedure is mandatory for all maintenance and operations personnel at Vindhya Precision Works.

---

## 2. NORMAL OPERATING RANGES AND MONITORING THRESHOLDS

### 2.1 Parameter Specifications
The 400-Tonne Hydraulic Press shall operate strictly within the parameters defined in Table 2.1. The condition-monitoring system (CMS) is programmed with these exact numeric limits.

**Table 2.1: Operating Ranges and Alarm Setpoints for HYD-PRESS**
| Parameter | Healthy Operating Range | Warning Setpoint | Trip / Interlock Setpoint | Corrective Action Trigger |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration (RMS)** | 1.2 – 4.0 mm/s | 5.6 mm/s RMS | 8.5 mm/s RMS | Immediate shutdown at trip |
| **Surface Temperature** | 38 °C – 66 °C | 78 °C | 92 °C | Inspect cooling circuit at warning |
| **Operating Pressure** | 205.0 – 215.0 bar | 185.0 bar (Low Pressure) | 175.0 bar (Low-Low Press) | Halt cycle at low-pressure alarm |
| **Motor Current (Full Load)**| 115 A – 142 A | 158 A | 172 A | Check proportional valve load |

### 2.2 Hazardous Energy Isolation
Prior to performing any mechanical or hydraulic intervention, technicians shall execute complete isolation of the following hazardous energy sources in accordance with Vindhya Precision Works Lockout/Tagout (LOTO) Procedure EHS-LOTO-01:
1. **Hydraulic Energy:** Isolate main pump circuit breaker, close manual isolation valve V-01, and bleed accumulator pressure to < 0.5 bar via drain valve DV-01.
2. **Electrical Energy:** Open and lock out main 415V supply isolator Q1 at Motor Control Centre MCC-HYD-02.
3. **Gravity:** Lower the 400-tonne main slide to the mechanical dead-stops and engage the hydraulic drop-pin safety locks (Pins LP-01 and LP-02).

---

## 3. PREVENTIVE MAINTENANCE SCHEDULE

### 3.1 Maintenance Responsibility
* **Responsible Trade:** Hydraulics
* **Supporting Trade:** Mechanical
* **Base Preventive Maintenance Interval:** Exactly 750 running hours ($\pm 12$ hours tolerance).

### 3.2 Running-Hour Task Matrix
* **750 Hours (PM-1):** 
  * Inspect proportional valves for spool stiction.
  * Grease main slide bronze guideways with VPW-approved synthetic grease (15 strokes per nipple).
  * Check electrical terminations at contactor VPW-P-00042.
  * Clean return-line filter housing.
* **1,500 Hours (PM-2):** 
  * Perform PM-1 tasks.
  * Replace return-line and pressure-line filtration elements.
  * Inspect drive belt tension; replace Economy belt VPW-P-00037 if deflection exceeds 8 mm under 3.5 kg load.
  * Calibrate pressure transducers against reference gauge.
* **4,500 Hours (PM-3):** 
  * Perform PM-2 tasks.
  * Overhaul main cylinder dynamic seals using Deep seal VPW-P-00002 and Inside seal VPW-P-00005.
  * Inspect and replace secondary sealing elements (Almost seal VPW-P-00032).
  * Inspect Camera bearing VPW-P-00013 and Account bearing VPW-P-00024 for radial play exceeding 0.05 mm; replace if necessary.
  * Verify alignment of Left sensor VPW-P-00009.

---

## 4. FAULT-CODE TABLE AND TROUBLESHOOTING

**Table 4.1: HYD-PRESS Fault Conditions, Causes, and Corrective Actions**
| Fault ID | Condition Description | Probable Cause | Corrective Action |
| :--- | :--- | :--- | :--- |
| **F-HYD-01** | Main Pump Cavitation Noise | Restricted suction strainer or degraded oil viscosity at start-up. | Clean suction strainer; verify hydraulic oil temperature is above 25 °C before starting pump. |
| **F-HYD-02** | Slide Creep at Top Dead Center | Internal bypass across main piston seals (Deep seal VPW-P-00002 / Inside seal VPW-P-00005). | Isolate energy sources, perform LOTO, and replace cylinder seal kits. |
| **F-HYD-03** | Press Fails to Build Tonnage | Proportional relief valve sticking or pilot pressure failure below 28.0 bar. | Clean pilot stage valve spool; verify proportional amplifier card output current (target 400-800 mA). |
| **F-HYD-04** | Excessive Vibration Alarm (5.6 mm/s) | Misalignment of pump-motor coupling or loose mounting bolts on base plate. | Check coupling alignment with laser tool (tolerance $< 0.05$ mm); torque motor foot bolts to 210 Nm. |
| **F-HYD-05** | High Surface Temperature (78 °C) | Heat exchanger fouling or insufficient cooling water flow ($< 45$ L/min). | Backwash shell-and-tube heat exchanger; verify cooling water inlet temperature does not exceed 25 °C. |
| **F-HYD-06** | Contactor Chatter / Failure | Low control voltage or pitted main contacts on Notice contactor VPW-P-00042. | Measure control circuit voltage (must be 110V AC $\pm 5\%$). If voltage is stable, replace contactor VPW-P-00042. |

---

## 5. CONSUMABLE AND SPARE PARTS LIST
Technicians shall only use inventory items matching the exact part numbers listed in Table 5.1. Substitution of unlisted parts is strictly prohibited.

**Table 5.1: Approved Spare Parts and Consumables Inventory**
| Part Number | Description | Application |
| :--- | :--- | :--- |
| **VPW-P-00002** | Deep seal | Main hydraulic cylinder primary dynamic sealing element |
| **VPW-P-00005** | Inside seal | Main hydraulic cylinder secondary wiper and rod seal |
| **VPW-P-00009** | Left sensor | Slide position linear encoder / proximity sensor assembly |
| **VPW-P-00013** | Camera bearing | Optical alignment guide bearing on upper crown assembly |
| **VPW-P-00024** | Account bearing | Main toggle pivot thrust bearing assembly |
| **VPW-P-00032** | Almost seal | Auxiliary manifold block static O-ring kit |
| **VPW-P-00037** | Economy belt | Main hydraulic pump auxiliary auxiliary drive belt |
| **VPW-P-00042** | Notice contactor | Main motor control panel primary power switching contactor |

---

## 6. TORQUE SPECIFICATIONS
All threaded fasteners associated with the HYD-PRESS asset class shall be torqued to the values specified in Table 6.1 using a calibrated torque wrench. Threads shall be lightly coated with anti-seize compound unless specified otherwise.

**Table 6.1: Fastener Torque Matrix**
| Fastener Location | Thread Size | Target Torque | Remarks |
| :--- | :--- | :--- | :--- |
| Main Cylinder Flange Bolts | M30 (Grade 12.9) | 1,450 Nm | Star pattern tightening in 3 stages (500 Nm, 1000 Nm, 1450 Nm) |
| Pump-Motor Mounting Foot | M16 (Grade 8.8) | 210 Nm | Cross-pattern torque |
| Hydraulic Manifold Tie-Bolts | M12 (Grade 10.9) | 85 Nm | Sequential torque pass |
| Base Frame Anchor Bolts | M24 (Grade 8.8) | 650 Nm | Verify with hydraulic tensioner every 4,500 hours |

---

## 7. SAFETY-CRITICAL CORRECTIVE ACTIONS

### 7.1 Mandatory LOTO and Permit Requirements
The following corrective actions involve high-energy release risks or heavy lifting overhead. Technicians shall not commence work without executing a formal **Confined Space / Mechanical LOTO Permit** countersigned by the Area Safety Engineer:
1. **Replacement of Main Cylinder Seals (Deep seal VPW-P-00002 and Inside seal VPW-P-00005):** Requires mechanical pinning of the 400-tonne slide, absolute pressure zeroing of accumulators, and overhead crane lifting authorization.
2. **Replacement of Account bearing VPW-P-00024:** Requires hydraulic cylinder shoring and structural load-transfer rigging to prevent accidental slide collapse.
3. **Replacement of Notice contactor VPW-P-00042:** Requires electrical LOTO at MCC-HYD-02 with mandatory voltage verification using a CAT IV multimeter confirming 0.0V across all terminals prior to terminal touching.
4. **Intervention on High-Pressure Hydraulic Lines (> 185 bar):** Requires full depressurization, zero-energy verification via gauge PT-01, and thermal cool-down until surface oil temperature drops below 40 °C.
