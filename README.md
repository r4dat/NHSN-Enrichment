# NHSN-Enrichment
Enriching public health data with administrative claims.

For further work see: 
Cook-Wiens, Rutherford et al. (2016). Reduction in Early Elective Delivery in Kansas
Hospitals: Strengthening Quality Improvement Efforts with Public Health Data. In *APHA
2016.*

# Background
Surgical Site Infections (SSIs) are potential complications associated with any type of surgical procedure. Although SSIs are among the most preventable of healthcare acquired infections (HAIs) they represent a significant burden in terms of patient morbidity and mortality and additional costs to health systems and service payers. For these reasons, the prevention of SSI has received considerable attention from surgeons and infection control professionals, health care authorities, the media and the public.<sup>1</sup> 

One of the primary tracking systems for SSIs is the Center for Disease Control's National Healthcare Safety Network (NHSN). Among other features it permits risk adjustment based on facturs unique to each surgery such as surgey length, scheduled vs. emergency procedure, diabetes, and other risk factors. As with all such systems, the result is only as good as the data received by NHSN.

# Objective
Compare the diabetes risk flag in NHSN surgical procedures with ICD-9 based administrative claims data (UB-04) indicating diabetes. 

# Method
In cooperation with the state health department, claims were deterministically linked to surgical procedures with a match rate of approximately 72%. NHSN and claims based diabetes status was then compared. 

# Result
*Confusion Matrix*

|| Claims Diabetic| Claims Non-Diabetic|
|:-------------:|:-------------:|:-----:|
|NHSN Diabetic| 93% | 7% |
|NHSN Non-Diabetic | 15% | 85% |

# Specifications

Procedure codes were pulled from NHSN surgical definitions.

Claims based diabetes status was determined by ICD-9 diagnosis codes consistent with AHRQ's PSI risk-adjustment methodology. See AHRQ version 5 SAS PSI program, CMBFQI32.

Diabetes without chronic complications:
25000-25033
65800-64804

Diabetes with chronic complications:
25040-25093, 7751

1) Global Guidelines for the Prevention of Surgical Site Infection. Geneva: World Health Organization; 2016. 3, IMPORTANT ISSUES IN THE APPROACH TO SURGICAL SITE INFECTION PREVENTION. Available from: https://www.ncbi.nlm.nih.gov/books/NBK401145/