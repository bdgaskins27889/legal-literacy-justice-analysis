# Project Proposal: The Scales of Justice

**Author**: Barbara D. Gaskins

**Course**: DSC 680: Applied Data Science

**Date**: February 16, 2026

---

## 1. Introduction and Project Proposal

This project, titled "The Scales of Justice: An Analysis of Representation and Sentencing Outcomes in U.S. Federal Courts," proposes a comprehensive data science analysis to investigate the impact of legal representation on sentencing outcomes within the U.S. federal court system. The core objective is to build and evaluate a series of statistical models to determine whether the type of legal counsel a defendant receives (e.g., private attorney vs. public defender) is a significant predictor of sentence severity, while controlling for other relevant factors such as race, age, and criminal history.

The project will leverage a large, publicly available dataset from the U.S. Sentencing Commission (USSC) to ensure replicability and transparency. The analysis will culminate in a detailed white paper, a presentation, and a fully documented code repository, demonstrating a complete, end-to-end data science workflow. This portfolio piece will showcase advanced skills in data processing, statistical modeling, fairness analysis, and communication, making it a suitable capstone project for a Master of Science in Data Science program.

---

## 2. Data Source

The primary data source for this project is the **U.S. Sentencing Commission (USSC) Individual Offender Datafiles**. Specifically, this project will utilize the Fiscal Year 2024 dataset.

| Attribute | Description |
| --- | --- |
| **Source** | U.S. Sentencing Commission (USSC) |
| **Dataset** | Individual Offender Datafiles, FY 2024 |
| **Accessibility** | Publicly available for download from the USSC website [1] |
| **Size** | Approximately 61,679 individual cases (rows) and over 27,000 variables (columns) |
| **Scope** | Contains detailed case-level information on all offenders sentenced under the federal sentencing guidelines. |
| **Key Variables** | Demographics (race, age, gender), criminal history, offense type, sentencing guidelines calculations, type of legal representation, and detailed sentencing outcomes (prison term, probation, fines). |

This dataset was chosen for its authority, comprehensiveness, and public accessibility, which are critical for credible and reproducible research. The large number of variables provides a rich foundation for a multi-faceted analysis.

---

## 3. Research Questions

This project seeks to answer the following primary and secondary research questions:

### Primary Research Question

1. **To what extent does the type of legal representation (private attorney vs. court-appointed counsel) influence the likelihood and severity of a prison sentence in U.S. federal courts, after controlling for defendant demographics and offense characteristics?**

### Secondary Research Questions

1. Are there significant disparities in sentencing outcomes based on a defendant's race? If so, does the type of legal representation mediate or moderate these disparities?

1. Which factors are the most significant predictors of receiving a prison sentence versus a non-custodial sentence (e.g., probation)?

1. Can a machine learning model be developed to predict sentencing outcomes, and does this model exhibit algorithmic bias against any particular racial or demographic group?

1. Among different statistical models (e.g., Logistic Regression, Multilevel Model), which provides the fairest and most accurate predictions of sentencing outcomes?

---

## 4. Ethical Implications

This research involves sensitive data and addresses a topic with significant societal implications. The following ethical considerations will be paramount throughout the project:

1. **Algorithmic Bias and Fairness**: The models developed in this project could, if misused, perpetuate or even amplify existing biases in the criminal justice system. A core component of this project is to rigorously audit the models for fairness using metrics like disparate impact and equalized odds. The goal is not just to build a predictive model, but to critically assess its fairness and report transparently on any biases found.

1. **Data Privacy and Anonymity**: Although the USSC dataset is public, it contains information about real individuals. The data is anonymized, and this project will maintain that anonymity strictly. No attempt will be made to re-identify individuals. All published results will be aggregated and will not contain any personally identifiable information.

1. **Interpretation and Misrepresentation**: The findings of this study could be misinterpreted or used to support prejudiced conclusions. The final report will include a detailed discussion of the limitations of the analysis and will caution against oversimplified interpretations. For example, a correlation between race and sentencing does not imply a causal relationship and must be contextualized with the systemic factors at play.

1. **Stigmatization**: The analysis will inevitably highlight disparities among different demographic groups. It is crucial to frame these findings not as a reflection on the groups themselves, but as evidence of systemic issues within the justice system. The language used in all reports and presentations will be chosen carefully to avoid stigmatizing any community.

1. **Accountability and Transparency**: The entire project, including all code, data sources, and analytical methods, will be made publicly available to ensure full transparency and allow for independent verification. This commitment to reproducibility is a core ethical principle of this project.

By proactively addressing these ethical issues, this project aims to be an example of responsible and socially conscious data science.

---

## References

[1]: https://www.ussc.gov/research/datafiles/commission-datafiles "United States Sentencing Commission. (2025). Individual Offender Datafiles, FY 1999-2024. Retrieved from"

