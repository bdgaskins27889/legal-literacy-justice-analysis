# Codebook Index Findings - Key Variables

## Source
USSC Public Release Codebook FY99-FY24 (Appendix C: Index by Subject)

## Variable Categories Found in Index

### Criminal History Variables (Page C-5)
- **CRIMHIST** (p. 31) - Criminal History Category
- **CRIMLIV** (p. 31) - Criminal Livelihood
- **CRIMLIVAP** (p. 31) - Criminal Livelihood Applied
- **CRIMPTS** (p. 31) - Criminal History Points
- **CRPTS** (p. 31) - Criminal Points
- **REL2PTS** (p. 62) - Release Points
- **POINT1, POINT2, POINT3** (p. 60) - Criminal history points
- **SENTPT** (p. 62) - Sentence Points

### Demographic Variables (Page C-6)
- **AGE** (p. 16) - Age at sentencing
- **AGECAT** (p. 17) - Age Category
- **CITIZEN** (p. 30) - Citizenship status
- **DISTRICT** (p. 34) - Judicial district
- **MONSEX** (p. 52) - Gender/Sex
- **MONRACE** (p. 52) - Race (monitoring variable)
- **NEWRACE** (p. 53) - Race (recoded)
- **NEWEDUC** (p. 53) - Education level (recoded)
- **EDUCATN** (p. 37) - Education
- **HISPOR IG** (p. 42) - Hispanic origin
- **MARRIED** (p. 49) - Marital status

### Court Proceedings Variables (Page C-6)
- **ACPTDLN** (p. 11) - Acceptance of responsibility
- **ACPTCOMM** (p. 11) - Acceptance of responsibility comments
- **PRESENT** (p. 60) - Presentence status
- **QUARTER** (p. 61) - Quarter of sentencing
- **SENTDATE** (p. 68) - Sentencing date
- **SENTVN** (p. 68) - Sentence version
- **SENTYR** (p. 70) - Sentencing year

### Departure and Variance Variables (Page C-6, C-7)
- **NOREAS** (p. 53) - No reason for departure
- **REASON1-REASONX** (p. 61) - Reasons for departure
- **DEPART** (p. 33) - Departure indicator
- **DEPART_A, DEPART_P, DEPART_S** (p. 33) - Departure types
- **BOOKER2, BOOKER3, BOOKER4** (p. 24-25) - Post-Booker departures
- **BOOKERCD** (p. 25) - Booker code
- **BOOKERT** (p. 25) - Booker type

### Guideline Range Variables (Page C-7, C-8)
- **GLMAX** (p. 41) - Guideline maximum
- **GLMIN** (p. 41) - Guideline minimum
- **XFOLSOR** (p. 86) - Final offense level
- **XMAXSOR** (p. 86) - Maximum sentence
- **XMINSOR** (p. 86) - Minimum sentence

### Sentencing Outcome Variables
- **SENTTOT** - Total sentence (not in index excerpt, but standard variable)
- **PRISDUM** - Prison dummy (not in index excerpt)
- **PROBDUM** - Probation dummy (not in index excerpt)

### Loss Variables (Page C-8)
- **LOSS1-LOSSX** (p. 48) - Loss amounts
- **LOSSCH** (p. 48) - Loss schedule
- **LOSSPROB** (p. 48) - Loss probation

### Mandatory Minimum Variables (Page C-8)
- **FAILMIN** (p. 37) - Failed mandatory minimum
- **FIREMIN1, FIREMIN2** (p. 39) - Firearm mandatory minimums

## Notes for Data Extraction

**IMPORTANT**: The codebook has an index organized by subject (Appendix C). Key page numbers:
- Criminal History: p. 31
- Demographics: p. 16-17, 30, 42, 49, 52-53
- Court Proceedings: p. 11, 60-61, 68, 70
- Departures: p. 24-25, 33, 53, 61
- Guidelines: p. 41, 86
- Offense Types: Need to check main codebook body

**Missing from Index**: 
- TYPEMONY (type of attorney) - need to search main codebook
- TRIAL indicator - need to search main codebook
- PLEADISP (plea disposition) - need to search main codebook
- MONCIRC (monitoring circumstances) - need to search main codebook
- NOCOUNTS (number of counts) - need to search main codebook
- OFFTYPE2 (offense type) - need to search main codebook

## Next Steps
1. Extract exact variable definitions from codebook pages listed above
2. Search for missing variables (attorney type, trial, plea, etc.)
3. Create final variable selection list with codes and descriptions
4. Build data extraction script to load only selected variables
