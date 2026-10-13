# Rotary Screw Air Compressor (AIR-COMP) Equipment Manual and SOP

**VINDHYA PRECISION WORKS**
**MAINTENANCE ENGINEERING DEPARTMENT**
**STANDARD OPERATING PROCEDURE & EQUIPMENT MANUAL**
**ASSET CLASS: AIR-COMP (ROTARY SCREW AIR COMPRESSOR)**
**DOCUMENT REF: VPW-SOP-AIR-042**
**REVISION: 4.2**

---

### 1.0 PURPOSE AND SCOPE

**1.1** This document defines the operating parameters, preventive maintenance schedules, fault diagnosis protocols, and spare parts provisioning for asset class AIR-COMP (Rotary Screw Air Compressors) installed at Vindhya Precision Works.

**1.2** Compliance with this manual is mandatory for all maintenance technicians, reliability engineers, and production supervisors operating within the Compressor House.

---

### 2.0 RESPONSIBLE TRADES AND HAZARDOUS ENERGY ISOLATION

**2.1 Responsible Trades**
*   Primary Trade: Mechanical.
*   Supporting Trade: Instrumentation.

**2.2 Hazardous Energy Sources**
Prior to the commencement of any maintenance, inspection, or non-routine intervention, technicians shall isolate the following energy sources in accordance with Vindhya Precision Works Lockout/Tagout (LOTO) Procedure VPW-LOTO-001:
1.  **Electrical:** 415V AC, 3-Phase, 50Hz supply via Main Incoming Feeder Breaker.
2.  **Pneumatic:** Compressed Air System via Upstream and Downstream Isolation Valves with downstream auto-venting line to zero energy state.

---

### 3.0 NORMAL OPERATING RANGES AND CONDITION MONITORING THRESHOLDS

**3.1 Operating Parameters**
Equipment operating within acceptable baseline health parameters at Vindhya Precision Works shall register within the following narrow bands:
*   **Healthy Vibration:** 1.2 to 4.0 mm/s RMS (measured at airend bearing housings, horizontal and vertical axes).
*   **Healthy Surface Temperature:** 38 °C to 66 °C (measured via IR thermography and PT100 elements on airend discharge and air-oil separator vessel).
*   **Nominal Operating Pressure:** 7.5 bar.

**3.2 Condition Monitoring Alarm and Trip Limits**
The plant condition-monitoring system (CMS) is programmed with hard limits. Any violation of these thresholds shall initiate automated logging, operator warnings, or emergency trips as specified below:

| Parameter | Baseline / Normal | Warning Setpoint | Trip Setpoint | Action on Trip |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration (RMS)** | 1.2 – 4.0 mm/s | 6.3 mm/s | 9.5 mm/s | Immediate motor coast-to-stop; lockout auto-restart |
| **Surface Temperature** | 38 °C – 66 °C | 88 °C | 102 °C | Immediate load-solenoid de-energisation and shutdown |
| **Operating Pressure** | 7.5 bar nominal | 6.2 bar (Low Pressure) | N/A | Generates SCADA warning; does not trip |
| **Motor Current** | 110 A nominal | 145 A | 165 A | Immediate breaker trip |

---

### 4.0 PREVENTIVE MAINTENANCE SCHEDULE BY RUNNING HOURS

**4.1 Base Preventive Maintenance Interval**
The base preventive maintenance interval for asset class AIR-COMP is strictly **2000 running hours** (± 50 tolerance hours). Maintenance must be executed by certified Mechanical and Instrumentation technicians.

**4.2 Schedule of Tasks**

*   **2,000 Running Hours (Level 1 - Minor Service):**
    *   Inspect and tension My belt (VPW-P-00036) to deflection specification of 4.5 mm under 35 N force.
    *   Replace Road seal (VPW-P-00001).
    *   Test Give valve (VPW-P-00034) for proper cycling and leakage.
    *   Inspect Per contactor (VPW-P-00019) and Eight contactor (VPW-P-00050) for contact pitting; measure contact resistance.
    *   Verify calibration of Time sensor (VPW-P-00106).

*   **4,000 Running Hours (Level 2 - Intermediate Service):**
    *   Execute all Level 1 tasks.
    *   Inspect Sell bearing (VPW-P-00003) condition via acoustic emission and thermal profiling.
    *   Replace Give valve (VPW-P-00034).
    *   Replace Such contactor (VPW-P-00075).

*   **8,000 Running Hours (Level 3 - Major Overhaul Service):**
    *   Execute all Level 1 and Level 2 tasks.
    *   Replace Sell bearing (VPW-P-00003).
    *   Replace Per contactor (VPW-P-00019) and Eight contactor (VPW-P-00050) regardless of visual condition.
    *   Perform complete alignment check of drive motor to airend.

---

### 5.0 FAULT-CODE TABLE AND DIAGNOSTIC PROSE

**5.1** Technicians shall use the following fault descriptions, probable root causes, and corrective actions for troubleshooting asset class AIR-COMP:

1.  **Fault Code F-101: High Air Discharge Temperature**
    *   *Probable Cause:* Low compressor lubricant level, fouled air-oil cooler matrix, or failing Time sensor (VPW-P-00106) providing false readings.
    *   *Corrective Action:* Check oil level in separator vessel and top up if required. Clean external cooler fins using compressed air. If temperature persists above 88 °C, check calibration of Time sensor (VPW-P-00106) and replace if output drifts by >2%.

2.  **Fault Code F-102: Excessive Vibration Warning (6.3 mm/s RMS)**
    *   *Probable Cause:* Loose My belt (VPW-P-00036) causing pulley resonance, or initial degradation of Sell bearing (VPW-P-00003).
    *   *Corrective Action:* Isolate electrical energy, inspect My belt (VPW-P-00036) tension and alignment, and re-torque mounting bolts. If vibration remains elevated, inspect Sell bearing (VPW-P-00003) for spalling.

3.  **Fault Code F-103: Low Operating Pressure (< 6.2 bar)**
    *   *Probable Cause:* Stuck or sluggish Give valve (VPW-P-00034) failing to close fully during loading cycle, or severe downstream compressed air system leakage.
    *   *Corrective Action:* Isolate pneumatic energy, inspect Give valve (VPW-P-00034) for internal debris or diaphragm rupture. Clean or replace Give valve (VPW-P-00034). Conduct ultrasonic leak detection on header network.

4.  **Fault Code F-104: Main Motor Overcurrent Trip (165 A)**
    *   *Probable Cause:* Airend rotor binding due to Sell bearing (VPW-P-00003) failure, or phase imbalance across Per contactor (VPW-P-00019).
    *   *Corrective Action:* Perform manual shaft rotation check of airend (unpowered). Check contact surfaces of Per contactor (VPW-P-00019) for welding or high resistance. Replace Sell bearing (VPW-P-00003) if mechanical binding is identified.

5.  **Fault Code F-105: Control Circuit Failure / Starter Drop-Out**
    *   *Probable Cause:* Burnout or mechanical binding in Eight contactor (VPW-P-00050) or auxiliary coil failure in Such contactor (VPW-P-00075).
    *   *Corrective Action:* Isolate electrical energy. Measure coil resistance of Eight contactor (VPW-P-00050) and Such contactor (VPW-P-00075). Replace faulty contactor units.

6.  **Fault Code F-106: Oil Leakage at Shaft Interface**
    *   *Probable Cause:* Degradation and weeping of Road seal (VPW-P-00001) due to thermal cycling beyond design life.
    *   *Corrective Action:* Isolate electrical and pneumatic energy sources. Disassemble drive coupling, extract worn Road seal (VPW-P-00001), inspect shaft sleeve for scoring, and install new Road seal (VPW-P-00001) using dedicated installation arbor.

---

### 6.0 CONSUMABLE AND SPARE PARTS LIST

**6.1** Technicians shall only use inventory items matching the exact part numbers and descriptions recorded in the Vindhya Precision Works enterprise asset management system for asset class AIR-COMP. No substitutions are permitted.

*   `VPW-P-00001` — Road seal
*   `VPW-P-00003` — Sell bearing
*   `VPW-P-00019` — Per contactor
*   `VPW-P-00034` — Give valve
*   `VPW-P-00036` — My belt
*   `VPW-P-00050` — Eight contactor
*   `VPW-P-00075` — Such contactor
*   `VPW-P-00106` — Time sensor

---

### 7.0 TORQUE SPECIFICATIONS

**7.1** Maintenance personnel shall apply calibrated torque wrenches to all fasteners associated with asset class AIR-COMP in accordance with the following schedule:
*   Airend Discharge Flange Bolts (M12 Gr 8.8): 85 Nm (± 4 Nm)
*   Motor Foot Mounting Bolts (M16 Gr 8.8): 195 Nm (± 10 Nm)
*   Air-Oil Separator Cover Nuts (M10 Gr 8.8): 50 Nm (± 2 Nm)
*   Electrical Power Terminals (Contactors VPW-P-00019, VPW-P-00050, VPW-P-00075): 14 Nm (± 1 Nm)

---

### 8.0 SAFETY-CRITICAL CORRECTIVE ACTIONS AND PERMIT REQUIREMENTS

**8.1** The following corrective actions are designated as **Safety-Critical**. They cannot be performed without an approved Work Permit (Permit to Work - PTW) and complete execution of Plant Lockout/Tagout (LOTO) protocols as detailed in section 2.0:
1.  Replacement or internal overhaul of the Sell bearing (`VPW-P-00003`).
2.  Replacement or servicing of the Road seal (`VPW-P-00001`) involving shaft disassembly.
3.  Any intervention on electrical contactors (`VPW-P-00019`, `VPW-P-00050`, `VPW-P-00075`) or internal wiring.
4.  Opening, inspection, or resealing of the air-oil separator pressure vessel or associated Give valve (`VPW-P-00034`) pipework.
5.  Tensioning or replacement of My belt (`VPW-P-00036`) involving guard removal and proximity to rotating transmission shafts.

**Document End.**
