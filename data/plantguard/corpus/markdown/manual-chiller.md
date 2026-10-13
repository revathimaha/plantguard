# Water-Cooled Process Chiller (CHILLER) Equipment Manual and SOP

# VINDHYA PRECISION WORKS
## STANDARD OPERATING PROCEDURE AND EQUIPMENT MANUAL
**Asset Class:** CHILLER (Water-Cooled Process Chiller)  
**Document ID:** SOP-MNT-CHILLER-042  
**Revision:** 4.1  
**Effective Date:** 14 January 2025  
**Owner:** Maintenance Engineering Lead  

---

### 1. SCOPE AND RESPONSIBILITY

**1.1** This document governs all preventive maintenance, corrective maintenance, condition-monitoring thresholds, and fault-resolution procedures for the Water-Cooled Process Chiller asset class (CHILLER) installed at Vindhya Precision Works.

**1.2** Primary maintenance responsibility is assigned to the **Mechanical** trade, with mandatory **Electrical** trade support for all control, power, and interlock verifications.

---

### 2. NORMAL OPERATING RANGES AND CONDITION MONITORING THRESHOLDS

**2.1** Technicians shall inspect the chiller against the operational limits detailed in Table 2.1. Any reading outside the normal healthy range but below the warning threshold requires a logged observation within the Computerized Maintenance Management System (CMMS).

**Table 2.1: CHILLER Operating Parameters and Alarm Setpoints**

| Parameter | Healthy Operating Range | Warning Setpoint | Trip / Interlock Setpoint | Action on Trip |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration (RMS)** | 1.2 to 4.0 mm/s | 5.3 mm/s RMS | 8.2 mm/s RMS | Immediate compressor coast-down; Lockout Code F-02 |
| **Surface Temperature** | 38 °C to 66 °C | 80 °C | 95 °C | Controlled shutdown via refrigerant bypass; Lockout Code F-03 |
| **Operating Pressure** | 2.8 to 3.2 bar (3.0 bar nominal) | 2.4 bar (Low Pressure) | 1.9 bar | Immediate compressor trip; Lockout Code F-01 |
| **Motor Current** | 78 A to 92 A (85 A nominal) | 98 A (105% FL) | 110 A (125% FL) | Overcurrent breaker trip; Lockout Code F-04 |
| **Chilled Water Outlet** | 6.5 °C to 7.5 °C (7.0 °C nominal) | 5.0 °C / 9.0 °C | 3.5 °C / 10.5 °C | Process interlock alarm; Chiller modulation halt |

---

### 3. PREVENTIVE MAINTENANCE SCHEDULE

**3.1** The base preventive maintenance interval for asset class CHILLER is **3000 running hours** or every 12 calendar months, whichever occurs first. 

**3.2** Running-Hour Tasks:
*   **3000 Hours (PM-1):** Inspect and clean condenser tubes; test oil separator differential pressure; replace fluid filters; verify refrigerant charge via subcooling calculation; inspect electrical terminal torque; test safety pressure switches.
*   **6000 Hours (PM-2):** Perform PM-1 tasks plus: service compressor oil pump; calibrate all temperature and pressure transducers; inspect compressor slide valve mechanism; test vibration sensor loop integrity.
*   **12000 Hours (PM-3):** Perform PM-2 tasks plus: overhaul compressor internal bearings; inspect evaporator tube bundle; replace all dynamic shaft seals and gaskets; perform non-destructive examination (NDE) of refrigerant containment pressure vessels.

---

### 4. FAULT-CODE TABLE AND CORRECTIVE ACTIONS

**4.1** When the control panel registers a fault code, technicians shall execute the diagnostic and corrective actions specified in Table 4.1.

**Table 4.1: CHILLER Fault Codes and Remediation**

| Fault Code | Named Fault Condition | Probable Cause | Corrective Action |
| :--- | :--- | :--- | :--- |
| **F-01** | Refrigerant Low Pressure Trip | Restricted liquid line, condenser fouling, or minor refrigerant charge loss. | Inspect sight glass for bubbles; check for oil traces at joints; leak-test using electronic detector; recover, evacuate, and recharge if charge is deficient by >10%. Replace part VPW-P-00022 (Per filter) if differential pressure exceeds 0.7 bar. |
| **F-02** | Compressor High Vibration | Coupling misalignment, worn internal bearings, or dynamic rotor unbalance. | Measure bearing housing vibration. If RMS velocity exceeds 8.2 mm/s, isolate unit, check alignment, and replace part VPW-P-00015 (Down coupling) and part VPW-P-00010 (We bearing). |
| **F-03** | Compressor High Surface Temperature | Inadequate cooling water flow, scaling on condenser tubes, or oil cooler starvation. | Verify condenser cooling water flow rate ($\ge 120 \text{ m}^3\text{/h}$); backflush condenser tubes; inspect oil injection solenoid valve part VPW-P-00043 (Cause valve) for correct actuation. |
| **F-04** | Motor Overcurrent Trip | Phase imbalance, high ambient plant temperature, or internal mechanical binding. | Measure line-to-line resistance and voltage balance; check starter contactor condition; verify motor winding thermistor resistance ($\le 2.7\text{ k}\Omega$ at normal operating temp). |
| **F-05** | Slide Valve Positioning Error | Hydraulic actuator failure, internal linkage binding, or feedback sensor drift. | Inspect hydraulic control manifold; verify actuator pressure (nominal 18 bar); replace part VPW-P-00012 (Live valve) if solenoid spool is stuck; recalibrate feedback transducer part VPW-P-00027 (Program sensor). |
| **F-06** | Sensor Loop Open / Out of Range | Damaged signal cable, water ingress into terminal box, or transducer failure. | Verify terminal strip continuity; check 24VDC loop power supply; if sensor reads outside physical limits, replace part VPW-P-00014 (End sensor) and inspect connector sealing gland. |

---

### 5. CONSUMABLE AND SPARE PARTS LIST

**5.1** Technicians shall only use the exact inventory part numbers listed in Table 5.1 for maintenance and repair of asset class CHILLER. No substitutions are permitted.

**Table 5.1: Approved CHILLER Spare Parts Inventory**

| Part Number | Description | Standard Replacement Interval |
| :--- | :--- | :--- |
| **VPW-P-00010** | We bearing | 12,000 running hours (PM-3) |
| **VPW-P-00012** | Live valve | As required by fault F-05 |
| **VPW-P-00014** | End sensor | As required by fault F-06 |
| **VPW-P-00015** | Down coupling | 12,000 running hours or upon high vibration |
| **VPW-P-00022** | Per filter | 3,000 running hours (Every PM-1) |
| **VPW-P-00027** | Program sensor | 6,000 running hours (Every PM-2) |
| **VPW-P-00041** | Difficult seal | 12,000 running hours (Every PM-3) |
| **VPW-P-00043** | Cause valve | As required by fault F-03 |

---

### 6. TORQUE SPECIFICATIONS

**6.1** Technicians shall apply the torque values specified in Table 6.1 during reassembly. Calibrated torque wrenches are mandatory for all bolting operations.

**Table 6.1: Fastener Torque Limits**

| Fastener Location | Thread Size | Target Torque | Lubrication Status |
| :--- | :--- | :--- | :--- |
| Compressor Terminal Lug Nuts | M10 | 28 Nm | Clean, dry threads |
| Refrigerant Flange Bolting (High Pressure) | M12 | 65 Nm | Anti-seize compound applied |
| Oil Line Compression Fittings | 3/4-16 UNF | 45 Nm | Light mineral oil on threads |
| Coupling Clamping Bolts | M8 | 32 Nm | Clean, dry threads |
| Bearing Housing Retaining Bolts | M10 | 40 Nm | Thread-locking fluid (Medium strength) |

---

### 7. SAFETY-CRITICAL CORRECTIVE ACTIONS AND LOCKOUT / PERMIT REQUIREMENTS

**7.1 Hazardous Energy Sources:** Prior to initiating any corrective maintenance on asset class CHILLER, technicians must isolate the following two primary hazardous energy sources:
1.  **Electrical Energy:** 415V AC 3-Phase supply via main feeder breaker in Motor Control Center (MCC) Panel CH-04.
2.  **Refrigerant Pressure:** High-pressure liquid and vapor R-134a/R-513A containment within the compressor, condenser, and evaporator vessels.

**7.2 Safety-Critical Corrective Actions:** The following corrective actions are designated as safety-critical and **strictly require** an approved Plant Lockout/Tagout (LOTO) and a formal Confined Space / Hot Work / Pressure Vessel Opening Permit signed by the shift safety officer before work begins:
*   **Action A:** Replacement or internal servicing of part VPW-P-00010 (We bearing) or compressor disassembly.
*   **Action B:** Opening of any refrigerant-containing circuit, line, or vessel requiring evacuation, refrigerant recovery, and replacement of part VPW-P-00022 (Per filter) or part VPW-P-00041 (Difficult seal).
*   **Action C:** Maintenance, removal, or replacement of high-pressure hydraulic or solenoid control valves, specifically part VPW-P-00012 (Live valve) or part VPW-P-00043 (Cause valve).
*   **Action D:** Electrical busbar inspection, drive-inverter replacement, or main power terminal re-termination inside the compressor terminal enclosure.

**7.3** No technician shall bypass safety interlocks, pressure relief valves, or vibration trip loops without written authorization from the Maintenance Engineering Lead and the execution of a temporary operating procedure document.
