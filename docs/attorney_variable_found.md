# Attorney/Counsel Variable Found

## Variable Name: DEFCONSL

**Description**: Indicates the type of defense counsel used in the instant offense.

**Codes**:
- 1 = Privately Retained Counsel
- 2 = Court Appointed Counsel
- 3 = Federal Public Defender
- 4 = Defendant Represented Self
- 5 = Waived Rights to Counsel
- 77 = Other Arrangements for Counsel
- . = Missing, Indeterminable, or Inapplicable

**Note**: This information is often not delineated in the PSR (Pre-Sentence Report), so it may be missing in some cases.

**Related Variable**: DEFCONTX - Text field describing the type of defense counsel when DEFCONSL is coded as "Other" (Code 77). Available FY1999-FY2003.

## Importance for Legal Literacy Analysis

This is a **critical variable** for the research framework. It directly measures **access to representation**, which is one of the primary mechanisms hypothesized to explain outcome disparities.

### Operationalization:
- **High Access**: Privately Retained Counsel (Code 1)
- **Moderate Access**: Court Appointed Counsel (Code 2), Federal Public Defender (Code 3)
- **Low Access**: Defendant Represented Self (Code 4), Waived Rights to Counsel (Code 5)

### Expected Relationships:
1. Privately retained counsel → Better outcomes (shorter sentences, more departures)
2. Pro se defendants → Worse outcomes (longer sentences, fewer departures)
3. This variable may mediate the relationship between race and sentencing outcomes

### Analysis Strategy:
1. Descriptive: Distribution of counsel type by race
2. Bivariate: Counsel type × Sentencing outcomes
3. Mediation: Race → Counsel Type → Sentencing Outcomes
4. Interaction: Counsel Type × Criminal History → Outcomes
