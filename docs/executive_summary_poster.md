# The Scales of Justice: A Fairness-Aware Analysis of Sentencing Outcomes

**Barbara D. Gaskins** | Master of Science in Data Science | January 25, 2026

---

## Research Question

How does legal representation, in conjunction with defendant demographics, influence sentencing outcomes in U.S. federal courts, and can we build a predictive model that is not only accurate but also fair?

---

## Data & Methods

-   **Data**: 60,026 federal sentencing cases from the U.S. Sentencing Commission (FY 2024).
-   **Models Compared**:
    1.  **Logistic Regression**: Baseline model with individual-level features.
    2.  **Multilevel Model**: Advanced model including district-level fixed effects to account for systemic variations.
-   **Fairness Evaluation**: Assessed disparate impact and error rate disparities across racial groups using the `fairlearn` library.
-   **Statistical Testing**: Used bootstrap analysis and permutation tests to validate fairness improvements.

---

## Key Findings

1.  **Representation Matters**: The type of legal counsel is a significant predictor of whether a defendant receives a prison sentence.

2.  **Baseline Model is Unfair**: A standard Logistic Regression model, while accurate, exhibits significant racial bias and **fails the 80% rule** for disparate impact (Demographic Parity Ratio of 0.706).

3.  **Multilevel Model is Significantly Fairer**: By accounting for differences between judicial districts, the Multilevel Model **passes the 80% rule** (Ratio of 0.816) and reduces fairness disparities by up to 42%.

4.  **Improvement is Statistically Significant**: The fairness improvements of the Multilevel Model are statistically significant (p < 0.001), confirming it is a genuinely superior model.

---

## Model Comparison: The Evidence for a Fairer Model

| Metric | Logistic Regression | **Multilevel Model** | Improvement |
| :--- | :--- | :--- | :--- |
| **Demographic Parity Ratio** | 0.706 (FAIL) | **0.816 (PASS)** | **+15.6%** |
| Selection Rate Disparity | 0.227 | **0.143** | **-37.0%** |
| True Positive Rate Disparity | 0.239 | **0.139** | **-41.8%** |

![Confidence Intervals](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/RzaeOAm3tZk86qvwvPgC1F-images_1769325145597_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL3N0YXRpc3RpY2FsX3Rlc3RzL2NvbmZpZGVuY2VfaW50ZXJ2YWxz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L1J6YWVPQW0zdFprODZxdnd2UGdDMUYtaW1hZ2VzXzE3NjkzMjUxNDU1OTdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMM04wWVhScGMzUnBZMkZzWDNSbGMzUnpMMk52Ym1acFpHVnVZMlZmYVc1MFpYSjJZV3h6LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=dRecSHCSyWhr3zDELmwxbDZdKvS7AvbVHd1zG-KjiOtBXKevjr2IFTSs500G4ksMxKlbAGKLmJpuFWmbF6TuoIIr9jm4IlvQ8PCjmPu2bQdXXwkTjrun-gRVlqxD0R7~WPYjwdHZJmu3-MCG09Xn7MAiCaoN5Dn03XF3NeORCCFLvfoYM3mzmbVz6Pos8-LlpS5tjihryMgWOMEvgP9OO0gtC1luEB91dtmzLRAzCaE4x16fO~IFb1g533YS0rFoTTOzXNKPw2tw9~-Fjz-RIXsb5e7938bCAAI74rgpC7PNyx8n4m0-JhQpsSjrdcrjtCCq~mWVV6L3kX8JR-OZAQ__)
*Figure 1: The 95% confidence intervals for fairness disparities do not overlap, proving the Multilevel Model is statistically significantly fairer.*

---

## Conclusion & Implications

Simply building an accurate model is not enough. This project demonstrates that a more sophisticated, context-aware model can be both accurate **and significantly more fair**. The Multilevel Model, by accounting for district-level variations, provides a less biased and more ethically sound tool for understanding sentencing outcomes.

This work has critical implications for the responsible development of AI in the legal domain and showcases a data science approach that prioritizes both performance and fairness.

---

## Skills Demonstrated

-   **Advanced Statistical Modeling**: Multilevel (Mixed-Effects) Models
-   **Algorithmic Fairness Auditing**: Disparate Impact, Equalized Odds
-   **Statistical Significance Testing**: Bootstrapping, Permutation Tests
-   **Data Wrangling & Preprocessing**: Large-scale public datasets
-   **Reproducible Research**: Fully documented and reproducible code
-   **Communication**: Translating complex findings for diverse audiences
