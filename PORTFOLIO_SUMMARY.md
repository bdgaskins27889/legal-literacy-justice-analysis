# Master's Portfolio Project: Complete Summary

**Student**: Barbara D. Gaskins

**Program**: Master of Science in Data Science

**Completion Date**: March 2026

**Project Title**: The Scales of Justice: An Analysis of Representation and Sentencing Outcomes in U.S. Federal Courts

---

## Project Overview

This portfolio project represents a comprehensive, graduate-level data science analysis examining the relationship between legal representation, defendant demographics, and sentencing outcomes in the U.S. federal court system. The project goes beyond simple prediction to rigorously evaluate and mitigate algorithmic bias, demonstrating a commitment to ethical AI and responsible data science.

---

## Key Accomplishments

### 1. Real-World Data Analysis
- Analyzed **60,026 federal sentencing cases** from the U.S. Sentencing Commission (FY 2024)
- Publicly available dataset ensuring full reproducibility
- Comprehensive data preprocessing and feature engineering

### 2. Advanced Statistical Modeling
- **Logistic Regression**: Baseline classification model
- **Multilevel Model**: Advanced model with district-level fixed effects (103 features)
- **Mediation Analysis**: Testing causal pathways (race → representation → outcomes)

### 3. Rigorous Fairness Evaluation
- Calculated disparate impact and equalized odds metrics across racial groups
- Identified that baseline model **fails the 80% rule** for disparate impact
- Demonstrated that Multilevel Model **passes the 80% rule** with 35% reduction in bias

### 4. Statistical Significance Testing
- **Bootstrap Analysis** (1,000 iterations): Confirmed non-overlapping confidence intervals
- **Permutation Test** (1,000 permutations): P-value < 0.001
- **McNemar's Test**: Confirmed models make significantly different predictions
- **Effect Size Calculation**: Quantified magnitude of improvement

### 5. Comprehensive Documentation
- **Research Report**: Full academic-style analysis with methodology and results
- **Model Comparison Document**: Detailed evidence-based comparison with statistical proof
- **Executive Summary**: Presentation-ready poster content
- **Policy Brief**: Non-technical recommendations for stakeholders
- **Reproduction Guide**: Complete instructions for replicating all results

---

## Technical Skills Demonstrated

| Category | Skills |
|:---------|:-------|
| **Programming** | Python (pandas, numpy, scikit-learn, statsmodels, fairlearn, matplotlib, seaborn) |
| **Statistical Methods** | Logistic regression, multilevel modeling, mediation analysis, bootstrap resampling, permutation testing |
| **Machine Learning** | Classification, model evaluation, hyperparameter tuning, cross-validation |
| **Fairness & Ethics** | Disparate impact analysis, equalized odds, demographic parity, algorithmic bias auditing |
| **Data Wrangling** | Large-scale data processing, missing value handling, feature engineering, stratified sampling |
| **Visualization** | Publication-quality charts (300 DPI), comparative visualizations, statistical graphics |
| **Communication** | Academic writing, technical documentation, policy briefs, executive summaries |
| **Reproducibility** | Version control, documented workflows, standalone reproduction scripts |

---

## Project Structure

```
legal_literacy_justice_project/
├── data/
│   ├── ussc_fy2024_model_ready.csv (2.8 MB, 52,456 cases)
│   └── README.md
├── scripts/
│   ├── 05_exploratory_analysis.py
│   ├── 06_statistical_models.py
│   ├── 07_fairness_analysis.py
│   ├── 08_advanced_models.py
│   ├── 09_comparative_fairness.py
│   ├── 10_reproduce_multilevel_fairness.py (STANDALONE)
│   ├── 11_statistical_significance_testing.py
│   └── README_REPRODUCTION.md
├── outputs/
│   ├── fairness/ (11 files: metrics, visualizations)
│   ├── models/ (6 files: coefficients, predictions, ROC curves)
│   ├── reproduction/ (6 files: complete reproduction outputs)
│   └── statistical_tests/ (6 files: bootstrap, permutation, confidence intervals)
├── docs/
│   ├── research_report.md
│   ├── fairness_report.md
│   ├── comparative_fairness_report.md
│   ├── detailed_model_comparison.md
│   ├── executive_summary_poster.md
│   ├── policy_brief.md
│   └── ussc_codebook.pdf
├── README.md
├── requirements.txt
└── DELIVERABLES.md
```

---

## Key Findings

### Finding 1: Representation Type Matters
Defendants with private attorneys have significantly different outcomes compared to those with public defenders or court-appointed counsel, even after controlling for criminal history and case characteristics.

### Finding 2: Baseline Models Can Be Unfair
A standard logistic regression model, while achieving 76% accuracy, exhibits significant racial bias with a Demographic Parity Ratio of **0.706 (FAIL)**.

### Finding 3: Context-Aware Models Are Fairer
The Multilevel Model, which accounts for district-level variations, achieves a Demographic Parity Ratio of **0.816 (PASS)** and reduces error rate disparities by up to 42%.

### Finding 4: Improvements Are Statistically Significant
Bootstrap analysis and permutation testing confirm that the fairness improvements are not due to chance (p < 0.001).

---

## Deliverables

### For Academic Review
1. **Research Report** (research_report.md): Complete analysis with introduction, methodology, results, and discussion
2. **Fairness Analysis Report** (fairness_report.md): Detailed fairness metrics and interpretation
3. **Model Comparison Document** (detailed_model_comparison.md): Statistical evidence for model selection

### For Presentations
4. **Executive Summary Poster** (executive_summary_poster.md): One-page visual summary
5. **Presentation Slides** (presentation_slides.md): Slide deck content

### For Policy Impact
6. **Policy Brief** (policy_brief.md): Non-technical recommendations for stakeholders

### For Reproducibility
7. **Standalone Reproduction Script** (10_reproduce_multilevel_fairness.py): Complete, documented script
8. **Reproduction Guide** (README_REPRODUCTION.md): Step-by-step instructions
9. **GitHub Repository**: All code, data, and documentation

### For Validation
10. **Statistical Testing Results**: Bootstrap, permutation, and McNemar's test outputs
11. **Visualizations**: 20+ publication-quality figures (300 DPI)

---

## Impact & Significance

This project makes three key contributions:

1.  **Methodological**: Demonstrates how to conduct a rigorous fairness audit of predictive models, including statistical significance testing of fairness improvements.

2.  **Practical**: Provides a replicable template for building fairer models in the criminal justice domain, with clear policy recommendations.

3.  **Educational**: Serves as a comprehensive example of graduate-level data science work that balances technical rigor with ethical responsibility.

---

## Next Steps for Deployment

While this is a portfolio project, the methodology and findings have real-world applicability:

1. **Publish Findings**: Submit to conferences (e.g., ACM FAT*, AIES) or journals focused on AI ethics
2. **Share with Stakeholders**: Distribute policy brief to criminal justice reform organizations
3. **Expand Analysis**: Replicate across state-level court systems or other federal datasets
4. **Build Dashboard**: Create interactive tool for exploring fairness metrics

---

## Contact Information

**Barbara D. Gaskins**
- Email: bdgaskins27889@gmail.com
- Phone: 252.495.3173
- LinkedIn: [Barbara D. Gaskins](https://www.linkedin.com/in/barbara-d-gaskins)

---

## Acknowledgments

- **Data Source**: U.S. Sentencing Commission, Individual Offender Datafiles (FY 2024)
- **Tools**: Python, scikit-learn, fairlearn, statsmodels, matplotlib, seaborn
- **Methodology**: Inspired by fairness-aware machine learning research and criminal justice reform literature

---

**This project demonstrates that it is possible—and necessary—to build AI systems that are both accurate and fair.**
