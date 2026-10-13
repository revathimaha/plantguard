# Continuous Curing Oven (IND-OVEN) Equipment Manual and SOP

# VINDHYA PRECISION WORKS
## EQUIPMENT MANUAL AND MAINTENANCE STANDARD OPERATING PROCEDURE
### ASSET CLASS: Continuous Curing Oven (IND-OVEN)
**Document ID:** SOP-IND-OVEN-014  
**Revision:** 4.2  
**Effective Date:** 14 January 2025  
**Owner:** Maintenance Engineering Lead  

---

## 1. GENERAL DESCRIPTION AND APPLICABILITY

**1.1** This document governs all operation, routine maintenance, condition monitoring, and corrective intervention for asset class **IND-OVEN** (Continuous Curing Oven) installed across Vindhya Precision Works facilities.  
**1.2** Primary maintenance responsibility is assigned to the **Electrical** trade, with **Instrumentation** providing mandatory support for control loops, pyrometric profiling, and safety interlock verification.  
**1.3** Healthy equipment operating within baseline parameters shall exhibit vibration levels between $1.2\text{ mm/s}$ and $4.0\text{ mm/s}$ RMS, and external surface temperatures between $38\,^{\circ}\text{C}$ and $66\,^{\circ}\text{C}$.  
**1.4** This asset class operates at atmospheric pressure; therefore, **no monitored process pressure** limits, alarms, or trips apply to IND-OVEN.  

---

## 2. HAZARDOUS ENERGY CONTROL AND ISOLATION

**2.1** Prior to undertaking any corrective maintenance, mechanical adjustment, or internal inspection, technicians shall execute a complete energy isolation in accordance with Vindhya Precision Works Safety Standard VPW-LOTO-01.  
**2.2** The hazardous energy sources associated explicitly with asset class IND-OVEN are:
1. **Electrical:** 415V AC 3-phase supply via Main Isolator Circuit Breaker MCC-B14, and 24V DC control power.
2. **Thermal:** Internal heating elements and refractory lining retaining residual heat exceeding $250\,^{\circ}\text{C}$.  

**2.3** Thermal energy dissipation requires a mandatory cool-down period until internal ambient temperature drops below $40\,^{\circ}\text{C}$ before technicians may enter the curing chamber.  

---

## 3. OPERATING RANGES, THRESHOLDS, AND ALARM SETPOINTS

**3.1** The condition-monitoring system shall continuously poll asset class IND-OVEN against the following hard limits. Exceeding warning thresholds triggers a restricted alert to the control room; exceeding trip thresholds initiates an immediate, automated category-1 safety shutdown.

| Parameter Monitored | Healthy Baseline | Warning Setpoint | Trip Setpoint | Action on Trip |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration (Drive End / Blower)** | $1.2 - 4.0\text{ mm/s}$ RMS | $4.8\text{ mm/s}$ RMS | $7.5\text{ mm/s}$ RMS | Immediate 415V trip, coast to stop |
| **Surface Temperature (Casing)** | $38 - 66\,^{\circ}\text{C}$ | $90\,^{\circ}\text{C}$ | $105\,^{\circ}\text{C}$ | Interlock element power cut, run exhaust fan |
| **Current (Drive Motor)** | $28.0 - 35.0\text{ A}$ | $39.5\text{ A}$ | $44.0\text{ A}$ | Overload relay trip, alarm annunciated |
| **Process Pressure** | *None* | *None* | *None* | *Not applicable to IND-OVEN* |

**3.2** Any vibration reading remaining between $4.8\text{ mm/s}$ and $7.49\text{ mm/s}$ RMS for more than 120 continuous seconds shall escalate automatically to a maintenance work order generation.  

---

## 4. PREVENTIVE MAINTENANCE SCHEDULE

**4.1** The base preventive maintenance (PM) interval for asset class IND-OVEN is exactly **1500 running hours** ($\pm 25$ hours tolerance).  
**4.2** Maintenance tasks shall be executed according to the following running-hour hierarchy:

* **1500 Running Hours (PM-1):**
  - Inspect and test electrical termination tightness inside the main control cabinet (torque to specification per Section 7).
  - Lubricate conveyor drive bearings using high-temperature synthetic grease (maximum 15 strokes per fitting).
  - Inspect condition of **VPW-P-00038 (Family belt)** and **VPW-P-00039 (Relationship belt)** for fraying, tension loss, or cracking; adjust alignment.
  - Verify calibration of thermocouple arrays against secondary standard.
  - Clean blower intake mesh and inspect **VPW-P-00058 (Reason seal)** for gas leakage or thermal hardening.

* **3000 Running Hours (PM-2):**
  - Execute all PM-1 tasks.
  - Inspect and test power contactors **VPW-P-00048 (Part contactor)** and **VPW-P-00052 (Material contactor)** for contact pitting, arc erosion, and coil resistance.
  - Inspect pneumatic/hydraulic actuation paths, replacing **VPW-P-00004 (Forget valve)** and **VPW-P-00069 (Race valve)** O-rings and seals.
  - Check structural integrity of internal belt support rollers and replace **VPW-P-00073 (Should bearing)** if radial play exceeds $0.15\text{ mm}$.

* **6000 Running Hours (PM-3):**
  - Execute all PM-1 and PM-2 tasks.
  - Complete overhaul of the hot-air recirculation blower assembly.
  - Full recalibration of all safety loops, emergency stop pushbuttons, and over-temperature limit thermostats.

---

## 5. FAULT-CODE TABLE AND CORRECTIVE ACTIONS

**5.1** The control system logs specific fault codes for IND-OVEN irregularities. Technicians shall consult the following diagnostic matrix for probable causes and mandatory corrective actions:

1. **Fault Code IND-FLT-01 (Vibration Warning / Trip):**
   * *Probable Cause:* Mechanical unbalance in the recirculation fan, loose motor mounting bolts, or failure of **VPW-P-00073 (Should bearing)**.
   * *Corrective Action:* Isolate electrical supply. Inspect blower impeller for material build-up or blade erosion. Measure bearing radial play; replace **VPW-P-00073 (Should bearing)** if worn. Retorque all motor base bolts.

2. **Fault Code IND-FLT-02 (Surface Temperature High):**
   * *Probable Cause:* Degradation of internal thermal insulation blanket or failure of **VPW-P-00058 (Reason seal)** allowing hot-gas bypass.
   * *Corrective Action:* Allow oven to cool below $40\,^{\circ}\text{C}$. Perform thermographic survey of casing exterior. Replace compromised sections of **VPW-P-00058 (Reason seal)** and re-pack internal insulation.

3. **Fault Code IND-FLT-03 (Drive Motor Overcurrent):**
   * *Probable Cause:* Binding in the conveyor transport mechanism, excessive belt tension on **VPW-P-00038 (Family belt)** or **VPW-P-00039 (Relationship belt)**, or seized transmission components.
   * *Corrective Action:* Lock out electrical energy. Manually rotate conveyor drive train to check for mechanical binding. Inspect and readjust belt tracking and tension. Check motor winding resistance.

4. **Fault Code IND-FLT-04 (Contactor Failure to Close / Chatter):**
   * *Probable Cause:* Low control circuit voltage, degraded contact surfaces on **VPW-P-00048 (Part contactor)** or **VPW-P-00052 (Material contactor)**, or dust ingress in the magnetic coil housing.
   * *Corrective Action:* Verify 24V DC control rail stability. Isolate power, open contactor housing, inspect silver-cadmium oxide contacts, and replace **VPW-P-00048** or **VPW-P-00052** if pitting exceeds $1.0\text{ mm}$ depth.

5. **Fault Code IND-FLT-05 (Pneumatic Actuation Failure):**
   * *Probable Cause:* Internal spool leakage or contamination in **VPW-P-00004 (Forget valve)** or **VPW-P-00069 (Race valve)**.
   * *Corrective Action:* Isolate compressed air supply and bleed downstream pressure. Remove valve assemblies, flush with anhydrous solvent, inspect internal spools, and replace faulty valve units using exact plant inventory part numbers.

6. **Fault Code IND-FLT-06 (Heating Element Control Loop Fault):**
   * *Probable Cause:* Solid-state relay failure, open-circuit heating element, or thermocouple drift.
   * *Corrective Action:* Isolate 415V electrical supply. Measure element resistance across all three phases. Verify thermocouple millivolt output against temperature bath. Replace defective element banks or control modules.

---

## 6. CONSUMABLE AND SPARE PARTS LIST

**6.1** Technicians shall only use genuine plant-inventories spare parts listed below for asset class IND-OVEN. Substitution of unlisted parts is strictly prohibited and invalidates safety certification.

| Part Number | Plant Inventory Description | Standard Repl. Qty |
| :--- | :--- | :--- |
| **VPW-P-00004** | Forget valve | 1 per assembly |
| **VPW-P-00038** | Family belt | 2 per drive train |
| **VPW-P-00039** | Relationship belt | 1 per drive train |
| **VPW-P-00048** | Part contactor | 3 per main panel |
| **VPW-P-00052** | Material contactor | 2 per main panel |
| **VPW-P-00058** | Reason seal | 1 set per casing perimeter |
| **VPW-P-00069** | Race valve | 2 per pneumatic manifold |
| **VPW-P-00073** | Should bearing | 4 per conveyor shaft |

---

## 7. TORQUE SPECIFICATIONS

**7.1** Fasteners on asset class IND-OVEN shall be tightened using a calibrated torque wrench to the following limits:
* M6 Electrical Terminal Screws: $2.5\text{ Nm}$ ($\pm 0.2\text{ Nm}$)
* M8 Busbar Connections: $14.0\text{ Nm}$ ($\pm 1.0\text{ Nm}$)
* M10 Motor Base and Flange Bolts: $45.0\text{ Nm}$ ($\pm 3.0\text{ Nm}$)
* M12 Bearing Housing Retention Bolts: $78.0\text{ Nm}$ ($\pm 5.0\text{ Nm}$)

---

## 8. SAFETY-CRITICAL CORRECTIVE ACTIONS AND PERMIT REQUIREMENTS

**8.1** The following corrective actions are designated as **safety-critical** due to the severe risk of electrical shock, arc flash, or uncontrolled thermal release:
1. Replacement or internal maintenance of power contactors **VPW-P-00048 (Part contactor)** and **VPW-P-00052 (Material contactor)**.
2. Servicing, replacement, or rewiring of heating element banks and internal thermal insulation seals (**VPW-P-00058**).
3. Disassembly, alignment, or replacement of conveyor drive belts (**VPW-P-00038**, **VPW-P-00039**) and bearing assemblies (**VPW-P-00073**).
4. Intervention on pneumatic control valves **VPW-P-00004 (Forget valve)** and **VPW-P-00069 (Race valve)** when connected to pressurized headers.

**8.2** Execution of any safety-critical corrective action listed in Clause 8.1 requires:
* An approved **Lockout/Tagout (LOTO)** application isolating Electrical (415V/24V) and Thermal energy sources.
* A mandatory **Hot Work Permit** if any welding, grinding, or thermal cutting is performed within $3.0\text{ meters}$ of the curing oven casing.
* A signed **Confined Space Entry Permit** prior to any technician entering the internal curing chamber.

---
*End of Document — SOP-IND-OVEN-014*
