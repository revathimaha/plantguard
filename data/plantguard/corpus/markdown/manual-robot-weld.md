# Six-Axis Welding Robot (ROBOT-WELD) Equipment Manual and SOP

# VINDHYA PRECISION WORKS
## EQUIPMENT MANUAL AND STANDARD OPERATING PROCEDURE
### ASSET CLASS: ROBOT-WELD (SIX-AXIS WELDING ROBOT)
**Document ID:** VPW-SOP-RW-014  
**Revision:** 4.2  
**Effective Date:** 14 January 2025  
**Owner:** Engineering Lead, Maintenance Department  

---

### 1.0 PURPOSE AND SCOPE
This document establishes the operational parameters, preventive maintenance schedules, fault response protocols, consumable replacement parts, and safety-critical isolation procedures for the Six-Axis Welding Robot asset class (**ROBOT-WELD**) at Vindhya Precision Works. Compliance with this procedure is mandatory for all maintenance technicians, robotics specialists, and electrical contractors.

### 2.0 RESPONSIBLE TRADES AND HAZARDOUS ENERGY ISOLATION
*   **Primary Responsible Trade:** Robotics
*   **Supporting Trade:** Electrical
*   **Hazardous Energy Sources Requiring Isolation:** 
    1. Electrical (400V AC 3-phase supply and 24V DC control power)
    2. Pneumatic (6.5 bar compressed air supply to tip dresser and purge solenoids)

### 3.0 NORMAL OPERATING RANGES AND CONDITION-MONITORING THRESHOLDS
The continuous condition-monitoring system installed on asset class **ROBOT-WELD** shall enforce the following numerical limits. Healthy equipment within this plant operates at 1.2 to 4.0 mm/s RMS vibration and 38°C to 66°C surface temperature.

*   **Vibration Parameters:**
    *   Normal Operating Range: 1.2 to 4.0 mm/s RMS
    *   Warning Setpoint: 4.6 mm/s RMS (Trigger level 1: Log event, notify Robotics trade within 4 operating hours)
    *   Trip Setpoint: 7.3 mm/s RMS (Trigger level 2: Immediate automatic safety stop and lockout of servo drives)
*   **Surface Temperature Parameters:**
    *   Normal Operating Range: 38°C to 66°C (Measured at Axis 3 gear housing and weld torch mounting flange)
    *   Warning Setpoint: 74°C (Trigger level 1: Log event, schedule thermal inspection within 24 operating hours)
    *   Trip Setpoint: 88°C (Trigger level 2: Immediate automatic thermal interlock trip)
*   **Process Pressure Parameters:**
    *   There is no monitored process pressure on this asset class (**ROBOT-WELD**). Pneumatic line pressure is regulated locally but is not integrated into the automated condition-monitoring trip matrix.
*   **Electrical Current Parameters:**
    *   Normal Operating Range: 8.5 A to 24.0 A per axis under standard payload (6 kg gun weight)
    *   Warning Setpoint: 28.5 A sustained for > 3.0 seconds
    *   Trip Setpoint: 34.0 A instantaneous overcurrent trip across any servo amplifier

---

### 4.0 PREVENTIVE MAINTENANCE SCHEDULE
The base preventive maintenance interval for asset class **ROBOT-WELD** is **1250 running hours**. Maintenance must be executed within a tolerance window of ± 25 running hours.

*   **1250 Running Hours (PM Level 1):**
    *   Inspect and clean **Health filter** (Part No. VPW-P-00060). Replace if differential pressure exceeds 0.25 bar.
    *   Inspect **Ground belt** (Part No. VPW-P-00017) for fraying, grounding continuity, and secure terminal torque.
    *   Inspect **Energy belt** (Part No. VPW-P-00078) for exterior wear, abrasion, and pinch points.
    *   Verify sensor calibration on **Group sensor** (Part No. VPW-P-00074).
*   **2500 Running Hours (PM Level 2 - Includes Level 1 tasks):**
    *   Inspect mechanical linkages: **Show coupling** (Part No. VPW-P-00000), **Against coupling** (Part No. VPW-P-00018), and **Lawyer coupling** (Part No. VPW-P-00059) for backlash, micro-fretting, and set-screw migration.
    *   Inspect and test electrical switching components, specifically the **Two contactor** (Part No. VPW-P-00089) bank for contact pitting, weld-stick, and coil resistance.
*   **5000 Running Hours (PM Level 3 - Includes Levels 1 & 2 tasks):**
    *   Complete overhaul of axis gearboxes, replacement of internal coupling assemblies, and re-termination of all moving flexible cable harnesses.

---

### 5.0 FAULT-CODE TABLE
The condition-monitoring and robot controller display the following fault conditions, accompanied by their probable causes and mandated corrective actions:

1.  **Fault Code RW-E01 (Drive Overcurrent Axis 3):**
    *   *Probable Cause:* Mechanical binding in harmonic drive, foreign object obstruction, or failing **Show coupling** (Part No. VPW-P-00000).
    *   *Corrective Action:* Execute full electrical lockout. Inspect gear train manually for binding. Replace **Show coupling** if tooth wear or slippage is detected.
2.  **Fault Code RW-E02 (High Vibration Warning):**
    *   *Probable Cause:* Loose base anchor bolts, unbalance in the welding gun assembly, or degraded **Against coupling** (Part No. VPW-P-00018).
    *   *Corrective Action:* Check baseplate torque to 180 Nm. Inspect and replace **Against coupling** if radial play exceeds 0.15 mm.
3.  **Fault Code RW-E03 (Thermal Trip Axis 2):**
    *   *Probable Cause:* Over-duty cycle operation, degraded ambient ventilation, or internal bearing failure causing surface temperature to breach 88°C.
    *   *Corrective Action:* Isolate electrical supply. Allow robot to cool below 40°C. Inspect Axis 2 motor winding insulation resistance; replace motor assembly if resistance reads $< 100\text{ M}\Omega$.
4.  **Fault Code RW-E04 (Ground Fault / Continuity Failure):**
    *   *Probable Cause:* Severed, oxidized, or loose **Ground belt** (Part No. VPW-P-00017) connecting the robot base to the rotating wrist casting.
    *   *Corrective Action:* Isolate electrical supply. Remove damaged **Ground belt** and install a new unit (Part No. VPW-P-00017), torquing mounting hardware to 22 Nm. Verify resistance $< 0.1\ \Omega$.
5.  **Fault Code RW-E05 (Control Power Contactor Dropout Failure):**
    *   *Probable Cause:* Internal mechanical binding, coil burnout, or burned contacts within the **Two contactor** (Part No. VPW-P-00089) assembly.
    *   *Corrective Action:* Perform electrical lockout. Replace the **Two contactor** (Part No. VPW-P-00089) module. Verify auxiliary contact feedback signals before clearing fault.
6.  **Fault Code RW-E06 (Pneumatic Pressure Low / Purge Failure):**
    *   *Probable Cause:* Blocked or saturated **Health filter** (Part No. VPW-P-00060) restricting airflow to the torch cleaning station and weld head purge channels.
    *   *Corrective Action:* Depressurize pneumatic circuit. Remove and replace **Health filter** (Part No. VPW-P-00060). Test line pressure downstream to ensure stable 6.0 bar delivery.

---

### 6.0 CONSUMABLE AND SPARE PARTS LIST
Technicians shall use only the exact part numbers and descriptions recorded in the plant's inventory system for asset class **ROBOT-WELD**. No substitutions are permitted.

*   **VPW-P-00000** – Show coupling
*   **VPW-P-00017** – Ground belt
*   **VPW-P-00018** – Against coupling
*   **VPW-P-00059** – Lawyer coupling
*   **VPW-P-00060** – Health filter
*   **VPW-P-00074** – Group sensor
*   **VPW-P-00078** – Energy belt
*   **VPW-P-00089** – Two contactor

---

### 7.0 TORQUE SPECIFICATIONS
Maintenance personnel must adhere to the following torque values during assembly, preventive maintenance, and component replacement:

*   Base Mounting Bolts (M16 Grade 10.9): **180 Nm**
*   Axis Servo Motor Mounting Fasteners (M8 Grade 8.8): **28 Nm**
*   Coupling Clamp Bolts (**Show coupling**, **Against coupling**, **Lawyer coupling**): **14 Nm**
*   Ground Terminal Fasteners (**Ground belt** VPW-P-00017): **22 Nm**
*   Electrical Power Terminal Lugs (**Two contactor** VPW-P-00089): **4.5 Nm**
*   Pneumatic Push-to-Connect Fitting Ports: **Hand tight plus 1 full turn**

---

### 8.0 SAFETY-CRITICAL CORRECTIVE ACTIONS (LOCKOUT / PERMIT REQUIREMENTS)
Any corrective action involving mechanical disassembly of robot axes, electrical replacement of switching devices, or entry into the robot safety cell envelope is classified as safety-critical. 

**Mandatory Prerequisites:**
1.  Issuance of a formal **Plant Hot Work and Mechanical Maintenance Permit**.
2.  Execution of a physical **Lockout/Tagout (LOTO)** procedure isolating:
    *   Electrical Energy: Main 400V breaker locked out with personal padlock and danger tag.
    *   Pneumatic Energy: Main air service valve closed, padlocked, and downstream line bled to 0.0 bar via the dump valve.
3.  Verification of zero energy state at the robot controller test points prior to hand tool contact.

**Explicit List of Safety-Critical Corrective Actions Requiring LOTO + Permit:**
*   Replacement or mechanical adjustment of **Show coupling** (Part No. VPW-P-00000).
*   Replacement, tensioning, or alignment of **Energy belt** (Part No. VPW-P-00078).
*   Replacement of the **Two contactor** (Part No. VPW-P-00089) power switching assembly.
*   Disconnection, replacement, or re-termination of the **Ground belt** (Part No. VPW-P-00017).
*   Any intervention requiring physical entry inside the perimeter safety light-curtain zone of asset class **ROBOT-WELD**.
