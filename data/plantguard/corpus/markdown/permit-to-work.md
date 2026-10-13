# Permit to Work and Safety-Critical Task Standard

# VINDHYA PRECISION WORKS
## ENGINEERING STANDARD: STANDARD OPERATING PROCEDURE
### DOCUMENT ID: SOP-VPW-SAF-041
### SUBJECT: PERMIT-TO-WORK (PTW) SYSTEM
### EFFECTIVE DATE: 12 OCTOBER 2026

---

### 1.0 PURPOSE AND SCOPE

**1.1** This standard defines the mandatory governance, responsibilities, thresholds, and operational constraints for the Vindhya Precision Works Permit-to-Work (PTW) system.

**1.2** This standard applies to all Vindhya Precision Works employees, contractors, and visiting personnel performing high-risk maintenance, fabrication, inspection, or modification activities within all manufacturing plants, warehouses, and utility facilities operated by Vindhya Precision Works.

---

### 2.0 DEFINITIONS AND TASK CLASSES REQUIRING A PERMIT

A formal PTW issued via the Vindhya Precision Works Maintenance Management System (MMS) is required prior to the commencement of any work falling within the following five task classes:

#### 2.1 Class 1: Hot Work
*   **Definition:** Any work involving open flames, electric arc welding, cutting, grinding, soldering, brazing, or the generation of incendiary sparks.
*   **Threshold:** Mandatory for any location within 15.0 meters of flammable material storage, combustible dust handling areas, or operational hydrocarbon and solvent lines.

#### 2.2 Class 2: Confined Space Entry
*   **Definition:** Entry into any enclosure that has limited or restricted means for entry or exit, is not designed for continuous human occupancy, and has known or potential hazards such as toxic atmospheres, oxygen deficiency, or engulfment risks.
*   **Threshold:** Mandatory for all entries into tanks, silos, vats, pits deeper than 1.2 meters, utility vaults, and large-diameter ductwork.

#### 2.3 Class 3: Work at Height
*   **Definition:** Any maintenance or construction activity where a fall from the working surface could result in personal injury.
*   **Threshold:** Mandatory for all work conducted at an elevation greater than 1.8 meters above ground or adjacent floor level without permanent physical guardrail protection meeting VPW-ENG-SPEC-102.

#### 2.4 Class 4: High-Voltage Electrical Work
*   **Definition:** Any invasive work, testing, switching, or repair on electrical infrastructure operating at voltages exceeding 1,000 Volts AC or 1,500 Volts DC.
*   **Threshold:** Mandatory for all work on substation transformers, primary switchgear, high-voltage distribution busbars, and capacitor banks.

#### 2.5 Class 5: Pressure System Breaking
*   **Definition:** The mechanical isolation, dismantling, blinding, or opening of any pipework, vessel, heat exchanger, or hydraulic accumulator containing gases or liquids under pressure.
*   **Threshold:** Mandatory for any pressure system operating at design pressures exceeding 3.5 bar gauge (barg) or carrying hazardous process fluids regardless of pressure.

---

### 3.0 NAMED ROLES AND RESPONSIBILITIES

**3.1 Permit Issuer (Authorised Signatory):**
Only personnel holding a current, plant-specific Permit Issuer Certification issued by the Vindhya Precision Works Safety Directorate may sign and issue a PTW. Current designated Permit Issuers are:
*   Manoj Sharma (Lead Reliability Engineer, Plant 1 & 2)
*   Priya Nair (Utilities Maintenance Manager)
*   Arun Patel (Senior Safety Compliance Officer)

**3.2 Permit Acceptor (Performing Authority):**
The Permit Acceptor must be the designated competent supervisor of the working crew who remains on-site for the duration of the task. Current certified Permit Acceptors include:
*   Ramesh Kumar (Mechanical Maintenance Supervisor)
*   Sunita Rao (Electrical Team Lead)
*   Deepak Joshi (Contractor Control Coordinator)

---

### 4.0 PERMIT VALIDITY PERIOD

**4.1 Standard Validity:**
The maximum validity period for any standard PTW is exactly twelve (12) consecutive hours from the time of issue, aligned with shift patterns.

**4.2 Extension Protocol:**
A permit may be extended for a single additional period not exceeding four (4) hours, provided:
*   The physical plant conditions remain unchanged.
*   The Permit Issuer re-inspects the worksite.
*   Both the Issuer and Acceptor sign the extension block on the physical permit document prior to the expiration of the initial 12-hour window.

**4.3 Multi-Day Tasks:**
For multi-day tasks, a fresh PTW must be generated, reviewed, and issued for each calendar day or shift rotation. Under no circumstances shall a permit carry over across shift handovers without formal re-validation by incoming shift leadership.

---

### 5.0 GAS-TESTING REQUIREMENTS AND RE-TEST INTERVALS

**5.1 Initial Pre-Entry Testing:**
Prior to the issuance of any permit involving Confined Space Entry (Class 2) or Hot Work (Class 1) within hazardous zones, an initial atmospheric gas test must be performed by a certified gas tester using a calibrated 4-gas monitor (Oxygen, Lower Explosive Limit [LEL], Carbon Monoxide, Hydrogen Sulfide).

**5.2 Acceptance Thresholds:**
Work shall not commence unless baseline atmospheric readings meet the following strict criteria:
*   Oxygen ($\text{O}_2$): 19.5% to 23.5% by volume.
*   Lower Explosive Limit (LEL): 0.0% LEL.
*   Carbon Monoxide ($\text{CO}$): Less than 25 ppm.
*   Hydrogen Sulfide ($\text{H}_2\text{S}$): Less than 5 ppm.

**5.3 Re-Test Intervals:**
*   **Confined Space (Class 2):** Mandatory continuous atmospheric monitoring with datalogging, supplemented by manual verification re-testing every two (2) hours by the Permit Acceptor.
*   **Hot Work (Class 1):** Mandatory atmospheric re-testing every four (4) hours, or immediately following any work stoppage exceeding thirty (30) minutes.

---

### 6.0 AUTOMATIC PERMIT VOID CONDITIONS

A PTW becomes immediately null and void, requiring total cessation of work and re-application, upon the occurrence of any of the following events:

**6.1 Plant Emergency:**
Sounding of the plant-wide or unit-specific emergency evacuation alarm.

**6.2 Gas Threshold Breach:**
Any gas detector reading exceeding the limits defined in Section 5.2 during continuous or periodic monitoring.

**6.3 Scope Deviation:**
Any modification to the job scope, equipment identification, or methodology not explicitly captured within the original permit text.

**6.4 Equipment Failure:**
Failure, uncalibrated drift, or removal of mandatory safety interlocks, local ventilation extraction fans, or personal protective safety equipment assigned to the task.

**6.5 Loss of Supervision:**
Absence of the designated Permit Acceptor from the immediate worksite for a continuous period exceeding fifteen (15) minutes without formal handover to a secondary certified Acceptor.

**6.6 Incident Occurrence:**
Occurrence of a near-miss, dropped object incident, or minor injury within the designated permit safety perimeter.

---

### 7.0 AUTOMATED ADVISORY SYSTEM RESTRICTIONS

**7.1 Automated Advisory Constraint:**
Where Vindhya Precision Works utilizes automated artificial intelligence or rule-based advisory engines within the MMS for maintenance scheduling and hazard evaluation, the automated system is strictly prohibited from issuing recommendations in the following four categories without prior, explicit, manual authorization and countersignature by the Plant Safety Director (Dr. K. R. Venkat):

1.  **Isolation Bypass Authorization:** Recommendations to bypass, override, or temporarily de-rate safety instrumented systems (SIS), fire suppression interlocks, or pressure safety valves (PSVs) to facilitate maintenance execution.
2.  **Confined Space Re-Classification:** Recommendations to reclassify a designated Class 2 confined space as a "non-permit required" space based solely on algorithmic historical sensor trends without physical inspector verification.
3.  **Simultaneous Operation (SIMOPS) Override:** Recommendations to permit conflicting high-risk work classes (e.g., simultaneous Hot Work and Solvent Flushing) within overlapping safety exclusion zones.
4.  **Exemption from Mandatory Cool-Down Periods:** Recommendations to shorten, waive, or bypass the mandatory 60-minute post-hot-work fire watch monitoring period specified in VPW-SAF-041-A.

---
### REVISION HISTORY
*   **Rev 01 (12 Oct 2026):** Initial release approved by Dr. K. R. Venkat, Director of Safety and Operational Integrity.
