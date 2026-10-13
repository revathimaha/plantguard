# Lockout/Tagout and Energy Isolation Standard

**VPW-EHS-SOP-401**  
**Title:** Control of Hazardous Energy (Lockout/Tagout Standard)  
**Plant:** Vindhya Precision Works – Main Facility  
**Effective Date:** 14 January 2025  
**Applies To:** All Maintenance Technicians, Machine Operators, and Engineering Contractors  

---

### 1. Purpose and Scope
1.1 This standard establishes the mandatory procedure for the lockout/tagout (LOTO) of energy sources on all machinery, presses, CNC centers, and automated assembly lines at Vindhya Precision Works.  
1.2 Compliance with this document is mandatory for all internal personnel and contracted maintenance staff.  
1.3 No maintenance task involving energy isolation may be performed on the basis of a recommendation from an automated system, predictive maintenance algorithm, or SCADA diagnostic log without a physical verification and written sign-off by a designated competent person.

### 2. Definitions and Roles
2.1 **Authorized Person:** A maintenance technician or engineer who has successfully completed Vindhya Precision Works LOTO certification course (Code: VPW-SAF-102) and holds a current Level 2 certification card.  
2.2 **Affected Employee:** An operator whose job requires them to operate or use a machine on which servicing or maintenance is being performed under LOTO.  
2.3 **Primary Lock:** A red, individually keyed padlock bearing the employee’s payroll number, issued exclusively to an Authorized Person.

### 3. The Six-Step Isolation Sequence
3.1 All Authorized Persons must execute the following six-step sequence in the exact order specified prior to commencing any unpowered intervention on production equipment:  
*   **Step 1: Notification.** Notify all affected employees in the immediate work zone of the impending shutdown and the reason for isolation, utilizing the plant intercom or direct verbal instruction.  
*   **Step 2: Machine Shutdown.** Shut down the equipment using normal stopping procedures (e.g., cycle stop button, HMI shutdown sequence). Do not use emergency stop buttons as a substitute for standard shutdown unless specified in the machine-specific appendix.  
*   **Step 3: Isolation.** Isolate all energy sources (electrical, pneumatic, hydraulic, mechanical, and thermal) by operating the designated primary disconnect switches, valves, or mechanical blocking devices located on the machine perimeter.  
*   **Step 4: Lockout and Tagout.** Affix the Authorized Person’s primary lock and standardized "Danger – Do Not Operate" tag to each energy-isolating device. The tag must be legibly filled out with the technician’s name, department code, extension, and date.  
*   **Step 5: Stored-Energy Dissipation/Restraint.** Relieve, disconnect, restrain, or otherwise render safe all stored or residual energy in accordance with Section 5 of this standard.  
*   **Step 6: Verification.** Verify isolation and zero-energy state by attempting to restart the equipment via local control panels and by executing physical test protocols defined in Section 5. Return all controls to the "Off" or "Neutral" position following verification.

### 4. Application and Removal of Locks
4.1 Only Authorized Persons holding a valid Level 2 certification are permitted to apply and remove primary locks for energy isolation.  
4.2 **Single-Key Principle:** Only the person who applied a lock may remove that lock. Keys must remain in the physical possession of the lock owner at all times during the shift.  
4.3 **Named Exception for Lock Removal:** In the event that an Authorized Person has left the plant premises without removing their primary lock at the end of a shift, the lock may be removed only under the direct authorization of the Plant Safety Manager, Mr. R. Mahajan, or in his absence, the Senior Engineering Superintendent, Ms. K. Sen.  
4.4 The authorization sequence for the exception under Clause 4.3 requires:  
*   Visual inspection of the work area by the Plant Safety Manager and Maintenance Lead to confirm all personnel are clear and guarding is reinstalled.  
*   Verification via plant attendance logs that the lock owner has exited the facility.  
*   Utilization of the Master Bolt Cutter located in the Plant Security Office, documented via Form LOTO-EX-04.

### 5. Stored-Energy Verification Procedures
5.1 **Electrical Systems:**  
*   After locking out the main circuit breaker (Step 4), use a calibrated CAT IV multitester (VPW Tool ID: MT-902, calibrated within the preceding 180 days) to test all incoming phase conductors and terminal blocks for voltage.  
*   Perform a three-point test: test a known live source, test the isolated circuit, and retest the known live source to confirm meter functionality. Zero energy is defined as a reading of $< 1.0\text{ V}$ AC/DC.  
*   Discharge internal capacitor banks using the plant-approved grounding wand (VPW Tool ID: GW-105) for a minimum dwell time of 180 seconds, or until meter verification confirms residual voltage has dropped below 50 V.

5.2 **Pneumatic Systems:**  
*   Close the main pneumatic isolation valve (ISO-PN-01) and apply the lockout hasp.  
*   Open the downstream bleed-off valve located on the manifold.  
*   Verify zero pressure by observing that panel pressure gauges drop to $0.0\text{ bar}$ within 30 seconds of valve actuation, and confirm zero air velocity at the nearest disconnect fitting using an acoustic leak detector or physical hand-sweep test past the exhaust port.

5.3 **Hydraulic Systems:**  
*   Shut down the hydraulic power unit (HPU) pump motor and lock out the feeder breaker.  
*   Close the high-pressure accumulator isolation valves.  
*   Bleed trapped hydraulic pressure by slowly opening the manual dump valves until system pressure gauges read $0.0\text{ bar}$ / $0.0\text{ PSI}$.  
*   Mechanically block any suspended heavy tooling, cylinders, or vertical slides using certified drop pins (VPW Pin ID: DP-400 through DP-412) rated for twice the maximum load.

### 6. Group Lockout Procedure
6.1 When servicing is performed by a crew, department, or multiple trades, a Group Lockout procedure must be implemented by the designated Lead Authorized Person (LAP).  
6.2 The LAP is responsible for executing Steps 1 through 5 of the isolation sequence for all energy sources affecting the work zone.  
6.3 The LAP shall place a group lockout box (lockbox) over the keys to the primary isolation points, or attach a multi-lock hasp directly to the primary isolation devices.  
6.4 Every technician participating in the maintenance task must attach their personal primary lock and identification tag to the group lockbox or multi-lock hasp before commencing work.  
6.5 Technicians may remove their individual locks from the group lockbox only when their specific task is complete and they are physically clear of the hazard zone. The LAP shall remove the final isolation locks only after all crew members have removed their locks from the group lockbox and sign-off is logged on Form LOTO-GRP-09.
