# Key Variables Selection for Legal Literacy Analysis

## Data Source
**US Sentencing Commission Individual Datafile - Fiscal Year 2024**
- Total cases: 61,679
- Total variables: 27,265
- Codebook: USSC_Public_Release_Codebook_FY99_FY24.pdf

## Research Framework
Based on the conceptual framework provided, we will operationalize **legal literacy proxies** and **access to representation** as mechanisms explaining disparities in criminal case outcomes.

## Variable Categories and Selection

### 1. **Demographics** (Control Variables)
- **NEWRACE**: Race/ethnicity (recoded variable)
- **MONSEX**: Gender
- **AGE**: Age at sentencing
- **CITIZEN**: Citizenship status
- **DISTRICT**: Judicial district

### 2. **Offense Characteristics** (Control Variables)
- **OFFTYPE2**: Primary offense type
- **NOCOUNTS**: Number of counts of conviction
- **MWGT1**: Drug weight (for drug offenses)
- **GLMIN**: Guideline minimum sentence (months)
- **GLMAX**: Guideline maximum sentence (months)

### 3. **Criminal History** (Legal Literacy Proxy)
- **CRIMHIST**: Criminal History Category (I-VI)
- **TOTPRISN**: Total prior prison sentences
- **TOTPROB**: Total prior probation sentences
- **PRISOR**: Prior incarceration indicator
- **PRIORARR**: Number of prior arrests

*Rationale: Prior system exposure indicates familiarity with legal processes*

### 4. **Representation Type** (Primary Independent Variable)
- **TYPEMONY**: Type of attorney/counsel
  - Public defender
  - Private attorney
  - Court-appointed (CJA panel)
  - Pro se (self-represented)
  
*Rationale: Direct measure of access to legal expertise*

### 5. **Procedural Engagement** (Legal Literacy Proxies)
- **TRIAL**: Trial indicator (vs. plea)
- **PLEADISP**: Plea disposition type
- **ACCGDLN**: Acceptance of responsibility
- **TOTMOTN**: Total number of motions filed
- **SAFE5C1**: Safety valve provision (indicates legal knowledge/advocacy)
- **DEPART**: Departure from guidelines (indicates effective advocacy)

*Rationale: These indicate system navigation skills and quality of representation*

### 6. **Pretrial Status** (Legal Literacy Proxy)
- **MONCIRC**: Monitoring circumstances (pretrial detention status)
- **PRESENT**: Presentence status
- **XCRHISSR**: Criminal history computation

*Rationale: Pretrial detention limits ability to prepare defense*

### 7. **Sentencing Outcomes** (Dependent Variables)
- **SENTTOT**: Total sentence length (months)
- **PRISDUM**: Prison sentence indicator
- **PRISON**: Prison sentence length (months)
- **PROBDUM**: Probation indicator
- **PROBATION**: Probation length (months)
- **FINE**: Fine amount
- **SENTIMP**: Sentence imposed relative to guideline range
  - Within range
  - Below range (government sponsored)
  - Below range (other)
  - Above range

### 8. **Judicial Discretion** (Contextual Variable)
- **DISTRICT**: Judicial district (for multilevel modeling)
- **CIRCDIST**: Circuit
- **REASON1-REASON3**: Reasons for departure/variance

## Hypotheses to Test

**H1**: Defendants with lower legal literacy proxies (fewer motions, no prior system exposure, pretrial detention) experience harsher outcomes, controlling for offense severity and criminal history.

**H2**: Representation type mediates the relationship between race and sentencing outcomes.

**H3**: Early procedural disadvantages (detention, acceptance of responsibility, plea vs. trial) compound into harsher final outcomes.

**H4**: Judicial discretion (departures/variances) amplifies—not neutralizes—legal literacy gaps.

## Analytical Approach

1. **Descriptive Statistics**: Distribution of key variables by race and representation type
2. **Bivariate Analysis**: Correlation between legal literacy proxies and outcomes
3. **Logistic Regression**: Prison vs. no prison (binary outcome)
4. **Linear Regression**: Sentence length (continuous outcome)
5. **Multilevel Models**: Account for district/judge clustering effects
6. **Mediation Analysis**: Race → Representation → Outcome pathway
7. **Fairness Metrics**: Disparate impact, equalized odds across racial groups

## Data Extraction Strategy

Given the large dataset (27,265 variables), we will:
1. Extract only the ~50-60 essential variables listed above
2. Create a working dataset with complete case analysis
3. Document all variable transformations and recoding
4. Save processed data for reproducibility
