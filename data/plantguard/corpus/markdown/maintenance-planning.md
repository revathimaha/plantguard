# Preventive Maintenance Planning Standard

**STANDARD OPERATING PROCEDURE: VPW-MNT-SOP-412**  
**Title:** Preventive Maintenance Planning, Criticality Classification, and Scheduling Standard  
**Facility:** Vindhya Precision Works  
**Author:** Maintenance Engineering Lead  
**Effective Date:** 14 January 2025  

---

### 1. Purpose and Scope
1.1 This document establishes the mandatory standard for preventive maintenance (PM) planning, asset criticality classification, work order routing, backlog management, and prioritization across all plant assets at Vindhya Precision Works.  
1.2 Compliance with this standard is mandatory for all maintenance planners, reliability engineers, and technicians.  

### 2. Operational Shifts and Plant Calendar
2.1 Maintenance planning and execution shall align with the plant's continuous three-shift operational pattern. The shift schedule is defined as follows:
*   **Shift A:** 06:00 to 14:00 (Duration: 8 hours)
*   **Shift B:** 14:00 to 22:00 (Duration: 8 hours)
*   **Shift C:** 22:00 to 06:00 (Duration: 8 hours)

2.2 Standard preventive maintenance work windows shall be scheduled during low-load periods or planned window slots within Shifts A, B, and C as dictated by the specific asset availability matrix.

### 3. Asset Criticality Classification and Inspection Intervals
3.1 Every plant asset listed in the Vindhya Precision Works asset register shall be assigned a criticality class of **A**, **B**, or **C** based on three factors: Safety Risk, Environmental Impact, and Production Downtime Cost.  
3.2 An asset shall take the **most severe** class indicated by any single one of the three factors.  
3.3 The production downtime cost factor shall be calculated using the asset's specific hourly rate retrieved directly from the asset register.  
3.4 The Reliability Committee-approved criticality matrix is defined in Table 3.1 below:

#### Table 3.1: Criticality Matrix
| Class | Safety Risk | Environmental Impact | Production Downtime Cost (INR / hour) | Mandatory Inspection Interval |
| :--- | :--- | :--- | :--- | :--- |
| **Class A** | HIGH | CRITICAL | $\ge$ 30,000 rupees per hour | Every 7 days |
| **Class B** | MEDIUM | MAJOR | 10,000 to 29,999 rupees per hour | Every 30 days |
| **Class C** | LOW | MINOR | $<$ 10,000 rupees per hour | Every 90 days |

3.5 Assets classified as Class A shall undergo mandatory physical and functional inspection every 7 days ($\pm$ 4 hours tolerance).  
3.6 Assets classified as Class B shall undergo inspection every 30 days ($\pm$ 24 hours tolerance).  
3.7 Assets classified as Class C shall undergo inspection every 90 days ($\pm$ 72 hours tolerance).

### 4. Trade Qualification and Work Order Assignment
4.1 A maintenance work order may only be assigned to a technician who holds the verified, active trade qualification matching the asset subsystem requirement.  
4.2 Permitted trade classifications are strictly limited to:
*   Mechanical
*   Electrical
*   Instrumentation
*   Hydraulics
*   Robotics

4.3 Cross-trade task assignment is prohibited unless the assigned technician holds dual-trade certification registered with the Vindhya Precision Works human resources and engineering database.

### 5. Condition-Monitoring Alert Conversion Rule
5.1 Any condition-monitoring (CM) alert—including vibration spikes exceeding ISO 10816-3 limits, thermographic hot spots exceeding $\Delta T$ of 15°C above ambient, or oil analysis degradation flagging ISO cleanliness code exceeding 18/16/13—shall automatically generate a corrective work order within 2 hours of alert receipt in the Computerized Maintenance Management System (CMMS).  
5.2 The generated condition-monitoring work order shall inherit the criticality class of the parent asset and bypass standard planning queues.

### 6. Backlog Threshold and Escalation
6.1 The total maintenance backlog for deferred or overdue preventive and corrective work orders shall not exceed 5% of total scheduled man-hours per department over a rolling 14-day calculation window.  
6.2 If the backlog threshold exceeds 8% for two consecutive weeks, the Maintenance Planning Lead shall issue a formal escalation notice to the Plant Operations Manager within 24 hours, triggering mandatory overtime authorization and temporary suspension of non-essential Class C PM tasks.

### 7. Planning Horizon
7.1 The master maintenance planning horizon shall cover a rolling 12-week (84-day) window.  
7.2 Detailed weekly schedules must be locked and published to production supervisors no later than Thursday 16:00 for the operational week commencing Monday 06:00.

### 8. Prioritization: Predictive Alerts vs. Scheduled Tasks
8.1 When resource constraints create a conflict between execution of a predictive alert work order and a routine scheduled PM task, priority shall be allocated according to the following hierarchy:
1.  **Priority 1:** Predictive (CM) or Condition-Monitoring alerts on Class A assets.
2.  **Priority 2:** Statutory regulatory inspections and safety-critical Class A scheduled PM tasks.
3.  **Priority 3:** Predictive (CM) alerts on Class B assets.
4.  **Priority 4:** Routine scheduled PM tasks for Class A and Class B assets.
5.  **Priority 5:** Predictive (CM) alerts and routine scheduled PM tasks for Class C assets.

8.2 Routine scheduled PM tasks displaced by a Priority 1 or Priority 2 predictive alert must be rescheduled within 72 hours of the original planned execution window.

---
**Document Revision Control:**  
*   *Revision:* 03  
*   *Approved by:* Chief Reliability Officer, Vindhya Precision Works  
*   *Next Review Date:* 14 January 2026
