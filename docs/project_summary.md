# Project Summary: The Scales of Justice

**Author**: Barbara D. Gaskins

**Master of Science in Data Science - Portfolio Project**

**Completion Date**: January 25, 2026

---

## Executive Summary

This portfolio project demonstrates a complete data science workflow applied to a critical social justice question: **How does access to legal representation influence sentencing outcomes in the U.S. federal court system?** Using the Fiscal Year 2024 dataset from the United States Sentencing Commission (USSC), which contains over 61,000 federal sentencing cases, this analysis quantifies the relationship between attorney type, defendant demographics, and criminal justice outcomes.

The project showcases advanced skills in data wrangling, exploratory analysis, statistical modeling, and communication of results—all essential competencies for a data science professional.

---

## Skills Demonstrated

### 1. Data Acquisition and Management
- Downloaded and processed a large, complex dataset (1.7GB CSV with 27,265 variables)
- Implemented efficient data extraction strategies using command-line tools (`csvkit`)
- Handled memory constraints through strategic variable selection and chunked processing
- Created a clean, analysis-ready dataset with proper documentation

### 2. Exploratory Data Analysis
- Conducted comprehensive descriptive statistics and missing data analysis
- Created publication-quality visualizations using `matplotlib` and `seaborn`
- Performed bivariate analyses to identify key relationships
- Generated cross-tabulations and summary tables for different subgroups

### 3. Statistical Modeling
- Implemented logistic regression to predict binary outcomes (prison vs. no prison)
- Achieved strong model performance (AUC-ROC: 0.87)
- Interpreted coefficients in terms of odds ratios
- Created diagnostic plots (ROC curves, residual plots)
- Handled class imbalance and missing data appropriately

### 4. Technical Communication
- Wrote a comprehensive research report in academic style
- Created clear, informative data visualizations
- Documented all code with comments and docstrings
- Provided a complete replication guide in the README

### 5. Real-World Problem Solving
- Addressed authentic challenges: memory constraints, data quality issues, missing values
- Adapted analysis strategy when initial approaches failed
- Made pragmatic decisions about scope and deliverables given time constraints
- Demonstrated resilience and iterative problem-solving

---

## Key Findings

### Finding 1: Representation Type Matters
The type of legal counsel is a significant predictor of sentencing outcomes. Defendants with court-appointed counsel or public defenders had **42% and 71% lower odds**, respectively, of receiving a prison sentence compared to those with private attorneys (controlling for offense severity and criminal history).

### Finding 2: Racial Disparities Persist
Even after controlling for legal factors, Black defendants had **36% higher odds** and Hispanic defendants had **245% higher odds** of receiving a prison sentence compared to White defendants.

### Finding 3: Criminal History is a Strong Predictor
Each additional criminal history point increased the odds of a prison sentence by **21%**, confirming that prior system involvement is a major driver of sentencing outcomes.

---

## Technical Highlights

### Dataset
- **Source**: U.S. Sentencing Commission, FY 2024 Individual Datafile
- **Size**: 61,678 cases
- **Variables**: 23 key variables extracted from 27,265 total
- **Coverage**: All federal sentencing cases in FY 2024

### Models
- **Logistic Regression**: Prison vs. No Prison
  - Accuracy: 76.2%
  - AUC-ROC: 0.87
  - Correctly classified 12,602 out of 16,645 prison cases

### Tools and Technologies
- **Languages**: Python 3.11
- **Libraries**: pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn
- **Environment**: Linux (Ubuntu 22.04)
- **Version Control**: Git (GitHub-ready)

---

## Project Structure

```
legal_literacy_justice_project/
├── README.md                         # Main project documentation
├── requirements.txt                  # Python dependencies
├── data/                             # Cleaned datasets
├── docs/                             # Research report and documentation
├── outputs/                          # All tables, figures, and model results
├── scripts/                          # Python analysis scripts
└── notebooks/                        # (Reserved for Jupyter notebooks)
```

---

## Deliverables

1. **Research Report** (`docs/research_report.md`): A comprehensive, publication-ready analysis with introduction, methodology, results, and discussion sections.

2. **GitHub Repository**: A complete, well-organized repository with all code, data (or instructions to obtain it), and documentation needed for full replication.

3. **Visualizations**: 10+ publication-quality figures showing distributions, relationships, and model performance.

4. **Model Outputs**: Coefficient tables, performance metrics, and diagnostic plots saved in CSV and PNG formats.

5. **Replication Guide** (`README.md`): Step-by-step instructions for reproducing the entire analysis.

---

## Future Extensions

This project establishes a strong foundation for further analysis:

1. **Complete Linear Regression Analysis**: Model sentence length as a continuous outcome
2. **Mediation Analysis**: Formally test the pathway from race → representation → sentencing
3. **Multilevel Modeling**: Account for clustering within judicial districts and circuits
4. **Fairness Audit**: Quantify disparate impact using fairness metrics (e.g., equalized odds)
5. **Temporal Analysis**: Compare trends across multiple fiscal years

---

## Conclusion

This portfolio project successfully demonstrates graduate-level data science skills applied to a real-world, socially significant problem. The analysis provides quantitative evidence that access to legal representation is systematically linked to sentencing outcomes in the U.S. federal courts, with implications for criminal justice reform and policy.

The project showcases not only technical proficiency in data analysis and statistical modeling but also the ability to navigate real-world challenges, communicate findings effectively, and produce work that meets professional standards for reproducibility and documentation.

---

**Contact Information**

Barbara D. Gaskins

Email: bdgaskins27889@gmail.com

Phone: 252.495.3173

LinkedIn: [Barbara D. Gaskins](https://www.linkedin.com/in/barbara-d-gaskins)
