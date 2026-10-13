# Vertical CNC Machining Centre (CNC-MILL) Equipment Manual and SOP

# STANDARD OPERATING PROCEDURE AND MAINTENANCE MANUAL
**Asset Class:** CNC-MILL (Vertical CNC Machining Centre)  
**Document ID:** SOP-VPW-CNC-042  
**Revision:** 04  
**Effective Date:** 15 October 2024  
**Plant Location:** Vindhya Precision Works, Plant Unit 3, Machining Bay B  

---

## 1. PURPOSE AND APPLICABILITY

1.1 This document defines the mandatory operating envelopes, preventive maintenance schedules, fault diagnosis protocols, torque values, and spare parts management for asset class CNC-MILL within Vindhya Precision Works.  
1.2 Compliance with this document is mandatory for all Maintenance Engineering, Toolroom, and Production Operations personnel.  
1.3 Responsible Trade: Mechanical is primary, with Electrical assigned in direct support for all electrical interlock, drive, and control cabinet interventions.

---

## 2. HAZARDOUS ENERGY ISOLATION

2.1 Prior to performing any corrective maintenance, tool change of non-standard configuration, or preventive maintenance requiring physical enclosure entry, technicians shall execute complete Lockout/Tagout (LOTO) procedures in accordance with Vindhya Precision Works safety standard EHS-LOTO-01.  
2.2 Hazardous energy sources identified for asset class CNC-MILL:
*   **Electrical:** 415V AC, 3-phase supply via main rotary isolator switch QF1, located on the rear of the machine control cabinet. Control voltage (24V DC) must be verified dead at terminal block X10.
*   **Pneumatic:** 6.0 bar compressed air supply via main air service unit shut-off valve V-AIR-01, equipped with an exhaust port padlock loop.

---

## 3. NORMAL OPERATING RANGES AND CONDITION MONITORING THRESHOLDS

3.1 Healthy units within asset class CNC-MILL shall operate strictly within the baseline parameters defined in Table 3.1.

**Table 3.1: Operating Envelopes and Alarm Setpoints for Asset Class CNC-MILL**

| Parameter | Baseline Healthy Range | Warning Setpoint | Trip / Interlock Setpoint | Monitored Status |
| :--- | :--- | :--- | :--- | :--- |
| **Spindle Vibration (RMS)** | 1.2 to 4.0 mm/s | 4.5 mm/s RMS | 7.1 mm/s RMS | Continuous (CMS Channel 1) |
| **Spindle/Housing Surface Temp** | 38 °C to 66 °C | 72 °C | 86 °C | Continuous (CMS Channel 2) |
| **Hydraulic/Pneumatic Pressure** | Not Applicable | Not Applicable | Not Applicable | No monitored process pressure on this asset class |
| **Spindle Motor Current (Normal Load)** | 14.0 A to 38.5 A | 45.0 A (10s delay) | 52.0 A (Immediate Trip) | Polled via PLC Register R-402 |

3.2 **Vibration Warning (4.5 mm/s RMS):** Generates an amber advisory on the shop floor SCADA terminal. The machine may complete the active part program, but subsequent cycles are inhibited until a mechanical inspection is logged.  
3.3 **Vibration Trip (7.1 mm/s RMS):** Initiates an immediate hardware emergency stop, cutting servo and spindle power within 120 milliseconds.  
3.4 **Surface Temperature Warning (72 °C):** Triggers a coolant flow verification flag on the operator HMI.  
3.5 **Surface Temperature Trip (86 °C):** Initiates a controlled feed-hold, spindle deceleration, and cycle abort.

---

## 4. PREVENTIVE MAINTENANCE SCHEDULE

4.1 The base preventive maintenance interval for asset class CNC-MILL is **500 running hours** (measured via PLC hour-meter register HR-01).  
4.2 Technicians shall execute tasks in accordance with the running-hour milestone matrix detailed in Table 4.1.

**Table 4.1: Preventive Maintenance Milestone Matrix**

| Interval | Task Description | Responsible Trade | Estimated Hours |
| :--- | :--- | :--- | :--- |
| **Every 500 Hours** | Replace Training filter (Part ID VPW-P-00076). Inspect Way lube reservoir levels. Check spindle taper runout. Clean cabinet ventilation grills. | Mechanical | 2.5 |
| **Every 1,000 Hours** | Replace Hour filter (Part ID VPW-P-00008). Inspect and grease axis ball screws (X, Y, Z axes) with Mobilith SHC 220. Verify axis backlash using laser interferometer. | Mechanical | 4.0 |
| **Every 2,000 Hours** | Full overhaul of pneumatic distribution blocks. Replace Drug valve (Part ID VPW-P-00021). Inspect Report coupling (Part ID VPW-P-00067) for rotational play. | Mechanical & Electrical | 8.0 |
| **Every 4,000 Hours** | Replace Investment bearing (Part ID VPW-P-00054) assemblies on primary axes. Calibrate Still sensor (Part ID VPW-P-00051) and Dark sensor (Part ID VPW-P-00079) against NIST-traceable standards. Overhaul Remain seal (Part ID VPW-P-00006) on spindle head. | Mechanical & Electrical | 16.0 |

---

## 5. FAULT-CODE DIAGNOSTICS AND CORRECTIVE ACTIONS

5.1 When the CNC control unit or CMS registers a fault, technicians shall reference Table 5.1 for diagnosis and mandatory remediation.

**Table 5.1: Fault-Code Prose Description and Corrective Action Matrix**

| Fault Condition / Code | Description | Probable Cause | Corrective Action |
| :--- | :--- | :--- | :--- |
| **ERR-CNC-101** | Spindle Over-Temperature Trip | Coolant pump cavitation or heat exchanger fouling. | Verify fluid flow; clean heat exchanger fins; inspect Still sensor (Part ID VPW-P-00051) wiring integrity. |
| **ERR-CNC-102** | Excessive Vibration Interlock | Spindle bearing micro-spalling or tool unbalance. | Stop machine; inspect toolholder balance; check Investment bearing (Part ID VPW-P-00054) condition via CMS history. |
| **ERR-CNC-103** | Lube Pressure Fault | Lubrication distributor blockage or pump failure. | Inspect Way lube lines; replace Training filter (Part ID VPW-P-00076); verify pump cycle timer in PLC. |
| **ERR-CNC-104** | Axis Servo Drive Overload | Mechanical binding on ball screw or way covers. | Isolate electrical power; manually check axis drag; inspect Report coupling (Part ID VPW-P-00067) alignment. |
| **ERR-CNC-105** | Pneumatic Clamping Failure | Insufficient clamping pressure or seal degradation. | Check incoming air supply (min 6.0 bar); replace Remain seal (Part ID VPW-P-00006) on drawbar cylinder. |
| **ERR-CNC-106** | Coolant Flow Interlock | Fluid starvation or heavy chip accumulation in sump. | Clean chip conveyor; replace Hour filter (Part ID VPW-P-00008); purge air pockets from fluid lines using Drug valve (Part ID VPW-P-00021). |

---

## 6. TORQUE SPECIFICATIONS

6.1 All fasteners utilized during maintenance of asset class CNC-MILL shall be tightened using calibrated torque wrenches in accordance with Table 6.1.

**Table 6.1: Fastener Torque Requirements**

| Fastener Application | Thread Size | Strength Class | Tightening Torque ($\pm 5\%$) |
| :--- | :--- | :--- | :--- |
| Spindle Cartridge Clamping Bolts | M12 | 12.9 | 85.0 Nm |
| Axis Ball Screw Bearing Locknuts | M20x1.5 | 10.9 | 150.0 Nm |
| Tool Changer Arm Mounting Bolts | M10 | 8.8 | 46.0 Nm |
| Way Cover Retaining Screws | M8 | 8.8 | 25.0 Nm |
| Motor Coupling Clamp Screws | M6 | 12.9 | 14.5 Nm |

---

## 7. CONSUMABLE AND SPARE PARTS INVENTORY

7.1 Technicians shall exclusively use the following plant-inventory-controlled part numbers when servicing asset class CNC-MILL. No substitutions are permitted without written engineering authorization from the Maintenance Engineering Lead.

*   **VPW-P-00006** – Remain seal (Spindle drawbar assembly)
*   **VPW-P-00008** – Hour filter (Primary coolant filtration unit)
*   **VPW-P-00021** – Drug valve (Pneumatic purge and fluid line control valve)
*   **VPW-P-00051** – Still sensor (Thermal monitoring probe, spindle housing)
*   **VPW-P-00054** – Investment bearing (Primary axis support bearing set)
*   **VPW-P-00067** – Report coupling (Servo-to-ball screw torque transmission coupling)
*   **VPW-P-00076** – Training filter (Way lube metering unit inline filter)
*   **VPW-P-00079** – Dark sensor (Optical zero-position reference sensor)

---

## 8. SAFETY-CRITICAL CORRECTIVE ACTIONS

8.1 The following corrective actions are designated as **Safety-Critical**. They require mandatory execution of Lockout/Tagout (LOTO) per Section 2 and the issuance of a confined-space or hot-work permit (as applicable) before work commences:
1. Replacement or mechanical adjustment of Investment bearing (Part ID VPW-P-00054) assemblies.
2. Servicing, alignment, or replacement of Report coupling (Part ID VPW-P-00067) under dynamic load conditions.
3. Overhaul or resealing of the spindle cartridge involving Remain seal (Part ID VPW-P-00006).
4. Any direct intervention within the main 415V electrical control enclosure involving the servo drives or main breaker QF1.
