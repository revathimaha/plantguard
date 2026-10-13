# Spare Parts and Procurement Policy

**DOCUMENT ID:** VPW-SOP-MNT-404  
**EFFECTIVE DATE:** 14 January 2025  
**REVISION:** 4.1  
**SUBJECT:** SPARE PARTS INVENTORY, CRITICALITY, AND PROCUREMENT POLICY  
**APPLIES TO:** Maintenance Engineering, Stores, and Procurement Departments  

---

### 1. PURPOSE AND SCOPE
1.1 This document defines the mandatory standard operating procedures for the classification, minimum stockholding, reorder calculations, supplier tiering, purchasing authorization thresholds, and obsolescence reviews for all spare parts held at Vindhya Precision Works (VPW).  
1.2 Compliance with this policy is mandatory for all maintenance technicians, stores supervisors, and plant engineers.

---

### 2. CRITICALITY-BASED MINIMUM STOCK RULES
2.1 All inventory items stored in the VPW warehouse shall be assigned a criticality code within the enterprise resource planning (ERP) system by the Maintenance Engineering Lead.  
2.2 Stockholding rules are strictly governed by the assigned criticality tier:  
*   **2.2.1 Critical (Class A):** Parts whose sudden failure results in total plant shutdown, severe safety incidents, or environmental non-compliance.  
    *   *Minimum Stock Level:* 100% of calculated safety stock plus normal lead-time demand.  
    *   *Hard Floor:* Never less than 2 units for active assets, unless specifically exempted under Section 2.3.  
*   **2.2.2 Essential (Class B):** Parts whose failure reduces plant output by 25% or more, or disables a secondary production line.  
    *   *Minimum Stock Level:* 1 unit minimum hard floor, plus normal lead-time demand.  
*   **2.2.3 General (Class C):** Consumables, fasteners, and parts whose failure causes negligible disruption to production.  
    *   *Minimum Stock Level:* Zero minimum hard floor; reordered strictly on economic order quantity (EOQ) and reorder point triggers.  
2.3 **Named Exceptions to Minimum Stock Rules:**  
*   *Exception 2.3.1:* Long-lead custom metallurgical rollers (Part IDs RM-8801 through RM-8804) held for the primary rolling mills are restricted to a maximum inventory ceiling of 1 unit regardless of Class A status, due to thermal degradation risks in static storage.  
*   *Exception 2.3.2:* Pneumatic actuator seals (Part IDs PS-102 through PS-115) are designated as perishable items with a 12-month shelf life; their maximum stock level is capped at 4 units per item, bypassing standard Class B minimum calculations.

---

### 3. REORDER POINT (ROP) CALCULATION AND WORKED EXAMPLE
3.1 The reorder point for all inventory items shall be calculated using the standard consumption formula enforced by the ERP system:  
$$\text{ROP} = (\text{Average Daily Consumption} \times \text{Lead Time in Days}) + \text{Safety Stock}$$

3.2 **Worked Example – Hydraulic Pump Cartridge (Part ID: HP-4402):**  
*   *Asset Classification:* Class A (Critical)  
*   *Average Daily Consumption (ADC):* 0.25 units per day (calculated on a trailing 365-day issuance log)  
*   *Lead Time (LT):* 14 days (retrieved directly from the ERP inventory record for this specific part)  
*   *Safety Stock (SS):* 2 units (fixed buffer for Class A hydraulic components)  

$$\text{Calculation:} \quad \text{ROP} = (0.25 \times 14) + 2$$  
$$\text{ROP} = 3.5 + 2 = 5.5$$  

3.3 Fractional ROP results shall always be rounded up to the next whole integer. Therefore, the system shall trigger a purchase requisition when the total on-hand plus on-order stock drops to **6 units**.

---

### 4. APPROVED SUPPLIER TIERS
4.1 Procurement sources are categorized into three distinct supplier tiers. The ERP inventory record contains the designated tier for every active part number.  
*   **4.1.1 T1 (OEM or Authorised Distributor):** Original equipment manufacturer or their certified, direct regional channel partner.  
*   **4.1.2 T2 (Approved Alternate):** Secondary manufacturers or aftermarket suppliers validated through VPW Quality Assurance material testing and trial runs.  
*   **4.1.3 T3 (Local or Spot Supplier):** Uncertified local fabricators, open-market traders, or emergency spot-purchase vendors utilized for immediate plant recovery.  
4.2 **Lead Time Rule:** Lead times are not fixed by supplier tier. The exact replenishment lead time is quoted individually per part number within the ERP inventory record, ranging from a minimum of **2 days** to a maximum of **90 days**.

---

### 5. PURCHASE AUTHORISATION THRESHOLDS AND AUTOMATION RULES
5.1 Purchase orders generated for inventory replenishment or direct-issue maintenance shall adhere strictly to financial thresholds enforced by the ERP system. Supplier tier assignment determines preferred sourcing, but total monetary value governs the approval workflow.  
5.2 **Threshold Tiers:**  
*   **5.2.1 Up to 200,000 Rupees (₹200,000):** The ERP reorder system may raise and approve the purchase order automatically, provided the preferred supplier is T1 or T2, and the stock level has breached the calculated ROP.  
*   **5.2.2 Above 200,000 Rupees and up to 1,000,000 Rupees (₹200,001 – ₹1,000,000):** Requisitions must be reviewed and digitally signed off by the **Maintenance Manager**.  
*   **5.2.3 Above 1,000,000 Rupees (> ₹1,000,000):** Requisitions require the explicit digital authorization of the **Plant Head**.  
5.3 **Automation Restriction Rule:** No purchase order with a total monetary value exceeding **200,000 Rupees** may be raised, processed, or released automatically by the ERP system under any circumstances. All orders above this threshold require manual intervention and designated managerial sign-off as defined in 5.2.

---

### 6. OBSOLESCENCE REVIEW CADENCE
6.1 The Maintenance Engineering Lead, in coordination with the Stores Supervisor, shall conduct a formal obsolescence review for all inventory items on a strict **semi-annual cadence** (completed by the 15th of June and the 15th of December each calendar year).  
6.2 Any part that has recorded zero usage for 24 consecutive months, or is linked to machinery decommissioned in the plant asset register, shall be flagged as obsolete, removed from active ROP calculations, and routed to the Plant Head for formal write-off and scrap disposal authorization.
