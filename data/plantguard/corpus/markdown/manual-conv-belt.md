# Main Line Belt Conveyor (CONV-BELT) Equipment Manual and SOP

# VINDHYA PRECISION WORKS
## EQUIPMENT MANUAL AND MAINTENANCE STANDARD OPERATING PROCEDURE
### ASSET CLASS: CONV-BELT — MAIN LINE BELT CONVEYOR
**Document ID:** VPW-SOP-CONV-BELT-042  
**Revision:** 4.2  
**Effective Date:** 14 October 2024  
**Applies To:** Plant Maintenance Department, Building 4 Heavy Assembly Line  

---

## 1. PURPOSE AND SCOPE

This document defines the technical specifications, operating ranges, preventive maintenance schedules, fault-clearing procedures, and spare parts catalog for the Main Line Belt Conveyor, asset class **CONV-BELT**. 

Adherence to this Standard Operating Procedure (SOP) is mandatory for all maintenance technicians, reliability engineers, and operations personnel at Vindhya Precision Works. 

---

## 2. RESPONSIBLE TRADES AND HAZARDOUS ENERGY ISOLATION

### 2.1 Primary Trade
* **Mechanical Technician:** Responsible for all mechanical inspections, alignments, roller replacements, belt tensioning, and gearbox servicing.

### 2.2 Supporting Trade
* **Electrical Technician:** Required to assist during lockout/tagout, drive motor checks, sensor recalibrations, and electrical control troubleshooting.

### 2.3 Hazardous Energy Sources
Prior to commencing any maintenance activity outside of standard visual inspection, technicians must isolate the following energy sources in accordance with Vindhya Precision Works Lockout/Tagout (LOTO) Procedure VPW-LOTO-01:
1. **Electrical:** 415V AC 3-Phase supply via Motor Control Center (MCC) Panel B4-MCC-07, Feeder Breaker 12.
2. **Mechanical:** Stored rotational energy of the head pulley and gravity take-up weight assembly; mechanical brake engagement required.

---

## 3. NORMAL OPERATING RANGES AND CONDITION-MONITORING THRESHOLDS

The condition-monitoring system (CMS) monitors asset class CONV-BELT continuously. Healthy equipment operating within baseline parameters exhibits a vibration velocity of **1.2 to 4.0 mm/s RMS** and a surface temperature of **38 to 66 °C**.

The specific numeric operating limits, alarm setpoints, and trip thresholds for asset class CONV-BELT are defined in Table 1.

### Table 1: Operating Limits and Alarm Setpoints (CONV-BELT)

| Parameter | Normal Healthy Range | Warning Setpoint | Trip Setpoint | Action on Trip |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration (Velocity RMS)** | 1.2 – 4.0 mm/s | 7.1 mm/s RMS | 11.0 mm/s RMS | Immediate drive interlock shutdown |
| **Surface Temperature (Bearings/Drive)** | 38 – 66 °C | 70 °C | 84 °C | Immediate drive interlock shutdown |
| **Motor Current (FLA 45A nominal)** | 32.0 – 42.0 A | 46.5 A (105% FLA) | 49.5 A (110% FLA for >5s) | Overload relay trip and lockout |
| **Process Pressure** | N/A | N/A | N/A | *No monitored process pressure on this asset class.* |

---

## 4. PREVENTIVE MAINTENANCE SCHEDULE

The base preventive maintenance (PM) interval for asset class CONV-BELT is **1000 running hours** (± 48 operational hours). Maintenance tasks are categorized by cumulative running hours in Table 2.

### Table 2: Preventive Maintenance Running-Hour Schedule

| Interval | Task ID | Maintenance Task Description | Trade |
| :--- | :--- | :--- | :--- |
| **1,000 Hours** | PM-1K-01 | Inspect belt tracking, alignment, and edge wear. Check skirt rubber clearance. | Mechanical |
| **1,000 Hours** | PM-1K-02 | Grease head and tail pulley plummer block bearings (Lithium Complex NLGI 2, 40g per point). | Mechanical |
| **1,000 Hours** | PM-1K-03 | Inspect drive coupling alignment and fastener torque. | Mechanical |
| **1,000 Hours** | PM-1K-04 | Clean optical and inductive proximity sensors. Verify signal response. | Electrical |
| **3,000 Hours** | PM-3K-01 | Check gearbox oil level, condition, and breathers. Take oil sample for laboratory analysis. | Mechanical |
| **3,000 Hours** | PM-3K-02 | Perform thermal imaging scan of motor windings, contactors, and bearing housings. | Electrical |
| **6,000 Hours** | PM-6K-01 | Complete overhaul and wear check of impact idlers and return rollers. Replace failed units. | Mechanical |
| **6,000 Hours** | PM-6K-02 | Megger test drive motor windings (minimum acceptable insulation resistance: 100 MΩ at 500V DC). | Electrical |
| **12,000 Hours** | PM-12K-01 | Flush and replace gearbox synthetic lubricant (ISO VG 220 gear oil). | Mechanical |
| **12,000 Hours** | PM-12K-02 | Inspect main drive contactor contacts and replace if pitting exceeds 1.5 mm depth. | Electrical |

---

## 5. FAULT-CODE AND TROUBLESHOOTING TABLE

When the control system flags an operational fault, technicians shall reference Table 3 for root-cause diagnosis and corrective action.

### Table 3: Fault-Code Descriptions, Causes, and Corrective Actions

| Fault ID | Description (Prose) | Probable Cause | Corrective Action |
| :--- | :--- | :--- | :--- |
| **F-CB-01** | Drive Contactor Failure to Engage | Internal coil burnout or mechanical binding in starter assembly. | Isolate power; inspect and replace the **Attack contactor** (Part **VPW-P-00016**). |
| **F-CB-02** | Bearing Lubrication / Seal Integrity Failure | Grease contamination ingress past worn shaft barriers. | Isolate power; replace degraded barrier component using **Avoid seal** (Part **VPW-P-00025**). |
| **F-CB-03** | Speed/Motion Monitoring Loss | Optical/magnetic pulse train interruption from tracking unit. | Clean lens; if unit is non-responsive, replace with **Artist sensor** (Part **VPW-P-00028**). |
| **F-CB-04** | Pulley Shaft End-Cap Leakage | Lubricant seepage past secondary housing exclusion barriers. | Depressurize and overhaul housing; install new **Drop seal** (Part **VPW-P-00029**). |
| **F-CB-05** | Longitudinal Carcass Delamination or Tear | Mechanical snagging of conveyed product against structural stringers. | Isolate asset; cut out damaged section and splice in a replacement **Avoid belt** (Part **VPW-P-00035**). |
| **F-CB-06** | Auxiliary Control Circuit Dropout | Chatter and failure of secondary auxiliary switching interface. | Verify control voltage; replace faulty auxiliary relay using **Mention contactor** (Part **VPW-P-00040**). |
| **F-CB-07** | Misalignment Edge-Switch Trip | Lateral belt drift exceeding allowable track envelope limits. | Adjust tracking idlers; check sensor alignment and replace faulty unit with **Several sensor** (Part **VPW-P-00044**). |
| **F-CB-08** | Return Roller Bearing Seizure | Internal ball-race corrosion or particulate blinding. | Lock out conveyor; extract seized assembly and fit a replacement **Own seal** (Part **VPW-P-00047**) inclusive of roller cartridge. |

---

## 6. APPROVED SPARE PARTS LIST

Technicians must strictly use plant-inventory-controlled part numbers listed in Table 4 for all replacement work on asset class CONV-BELT. No substitutions are permitted without written sign-off from the Plant Reliability Manager.

### Table 4: Approved Spare Parts Inventory

| Part Number | Plant Inventory Description | Asset Application |
| :--- | :--- | :--- |
| **VPW-P-00016** | Attack contactor | Main motor starter primary power switching |
| **VPW-P-00025** | Avoid seal | Primary shaft bearing contamination barrier |
| **VPW-P-00028** | Artist sensor | Shaft rotational speed and zero-speed monitoring |
| **VPW-P-00029** | Drop seal | Secondary housing lubrication retention barrier |
| **VPW-P-00035** | Avoid belt | Main conveyor carcass replacement section |
| **VPW-P-00040** | Mention contactor | Auxiliary control circuit switching relay |
| **VPW-P-00044** | Several sensor | Edge-tracking and belt-sway proximity detector |
| **VPW-P-00047** | Own seal | Return roller and idler bearing protection assembly |

---

## 7. TORQUE SPECIFICATIONS

To prevent structural failure or fastener fatigue during maintenance assembly, all technicians must apply calibrated torque wrenches to the fastener classes detailed in Table 5.

### Table 5: Fastener Torque Guidelines

| Fastener Location / Size | Thread Class | Target Torque (Nm) | Tolerance |
| :--- | :--- | :--- | :--- |
| Drive Motor Mounting Bolts (M16) | Grade 8.8 | 185 Nm | ± 5 Nm |
| Pillow Block Bearing Holding Down Bolts (M20) | Grade 8.8 | 360 Nm | ± 10 Nm |
| Head Pulley Locking Assembly Screws (M12) | Grade 10.9 | 115 Nm | ± 3 Nm |
| Conveyor Stringer Structural Splice Bolts (M12) | Grade 8.8 | 85 Nm | ± 2 Nm |
| Gearbox Torque Arm Anchor Bolts (M24) | Grade 10.9 | 650 Nm | ± 15 Nm |

---

## 8. SAFETY-CRITICAL CORRECTIVE ACTIONS AND PERMIT REQUIREMENTS

The following corrective actions involve high-risk energy states or structural load manipulations. They are explicitly designated as **Safety-Critical**. 

Before initiating any of the tasks listed below, technicians must execute a formal Lockout/Tagout (LOTO) per Procedure VPW-LOTO-01 **AND** obtain an active **Permit to Work (PTW)** issued by the Shift Safety Officer:

1. **Replacement of Main Drive Contactor (Fault F-CB-01 / Part VPW-P-00016):** Involves live-side 415V exposure risk within the MCC enclosure. LOTO of MCC Feeder Breaker 12 and High-Voltage PTW mandatory.
2. **Conveyor Belt Splice and Replacement Operations (Fault F-CB-05 / Part VPW-P-00035):** Involves release and re-tensioning of the gravity take-up weight stack (stored potential energy) and heavy manual handling. Mechanical LOTO, gravity drop-stop pin installation, and Hot Work / Lifting PTW mandatory.
3. **Head Pulley and Bearing Assembly Overhaul (Fault F-CB-02 / Part VPW-P-00025):** Involves overhead rigging, lifting of heavy rotating assemblies (>250 kg), and decoupling of heavy-duty gearboxes. Rigging Plan, Craning Permit, and Mechanical LOTO mandatory.

---
*End of Document — Vindhya Precision Works Internal Policy*
