# Comparative Fairness Analysis Report

**Author**: Barbara D. Gaskins

**Date**: January 25, 2026

**Project**: The Scales of Justice: An Analysis of Representation and Sentencing Outcomes

---

## 1. Executive Summary

This report presents a comparative fairness analysis of three statistical models developed to predict prison sentences in U.S. federal courts:

1.  **Logistic Regression**: A baseline classification model.
2.  **Multilevel Model**: A mixed-effects model accounting for clustering by judicial district.
3.  **Mediation Analysis Model**: A model testing the pathway of race → attorney type → sentencing outcome.

The analysis reveals that while all models exhibit some degree of bias, the **Multilevel Model is demonstrably the least biased** of the three. It is the only model to pass the "80% rule" for disparate impact, and it shows the smallest disparities in error rates across racial groups.

## 2. Comparative Fairness Metrics

The models were evaluated on two primary fairness criteria:

-   **Demographic Parity (Disparate Impact)**: Assesses if predictions are made at equal rates across groups. A Demographic Parity Ratio greater than 0.8 is considered fair.
-   **Equalized Odds**: Assesses if the model's error rates (both false positives and false negatives) are equal across groups. An Equalized Odds Ratio of 1.0 indicates perfect fairness.

### Key Findings

The **Multilevel Model** consistently outperformed the other models on key fairness metrics.

| Model | Demographic Parity Ratio | Equalized Odds Ratio | Selection Rate Disparity | TPR Disparity | FPR Disparity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.706 (FAIL) | 0.380 | 0.227 | 0.239 | 0.171 |
| **Multilevel Model** | **0.816 (PASS)** | **0.423** | **0.143** | **0.139** | **0.139** |
| Mediation Model | 0.707 (FAIL) | 0.380 | 0.227 | 0.238 | 0.171 |

*Table 1: The Multilevel Model has the highest (best) fairness ratios and the lowest (best) disparity levels across the board.*

## 3. Detailed Comparison

### 3.1. Disparate Impact (Demographic Parity)

The Multilevel Model was the only model to pass the 80% rule, with a Demographic Parity Ratio of **0.816**. The other two models failed, indicating they have a disparate impact on different racial groups.

![Demographic Parity Ratio Comparison](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/huaYnagxcwHaeBNXSxLKUk-images_1769324239717_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL2NvbXBhcmlzb25fZGVtb2dyYXBoaWNfcGFyaXR5.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L2h1YVluYWd4Y3dIYWVCTlhTeExLVWstaW1hZ2VzXzE3NjkzMjQyMzk3MTdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMMk52YlhCaGNtbHpiMjVmWkdWdGIyZHlZWEJvYVdOZmNHRnlhWFI1LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=TLm0z4ImA0J4MLnjcYCV8B~glOhzGlyBH5Vo3Oqd0j-Oq~cuyzjIjY-5-m~HoCx7Bnlp4L8sLZwmdEv77lsd8JZS8aCvsk5iDwcmbWdjbrUCJpDifi1ZMni9ZWDGc30IwWIZRYsUHIDHNIVFUCoMYvah-pCQDbsZWb9gDM27EvTAsPMegX~VpSoqOTRq33Qzv19LY4t5whCmXAim-6kfONIeMe6ncFcU6cks6VpwVz6Q4GsqejYyPxwa8lIIdDhaaF0TMk4i34XHNFvU3rDGaebFvP6bI9cm-EQ5DuzVh93os3x1tX0EHZAKQYsLAnexa00mkzdSd6DnK3BWJVHYkA__)
*Figure 1: Only the Multilevel Model crosses the 80% threshold for fairness, indicating it makes predictions at more equitable rates across racial groups.*

### 3.2. Equalized Odds

While no model achieved perfect equalized odds (a ratio of 1.0), the **Multilevel Model came closest with a ratio of 0.423**. This indicates that its error rates are more balanced across groups compared to the other models.

![Equalized Odds Ratio Comparison](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/huaYnagxcwHaeBNXSxLKUk-images_1769324239718_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL2NvbXBhcmlzb25fZXF1YWxpemVkX29kZHM.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L2h1YVluYWd4Y3dIYWVCTlhTeExLVWstaW1hZ2VzXzE3NjkzMjQyMzk3MThfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMMk52YlhCaGNtbHpiMjVmWlhGMVlXeHBlbVZrWDI5a1pITS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=rsv2ZQRNqPdr7Vyj75390R4BxB-qQspsZUK5Q~ubkHX9i2Z2puXr24TJXNBbgexLUzkBwT5qux0eGM43ouODTgiinmSKN2nV-0-5F4rNQ5Te4nuMGbcUuJEHZYWI1HfACQ5gsPVTFlpfcnRIYicjQW7ukhI9XulBbWbZgA8RmjXzeBhDS4deGWPzZC5t6rZg8H2r-NYHtRynLW5QtJ16y96LIi0HhQKQH8urjOepfdXnsnvwPtnH6GUoPcICFjGehEqrhuhfY7T04TnpAsiy5XXuwiDwGOuJV6uFWqeQxwc7eRFsWM1pkIRFZ-e8mZQnH41XDYJN7C2kGVdH~eun9A__)
*Figure 2: The Multilevel Model has the highest Equalized Odds Ratio, indicating its error rates are the most consistent across racial groups.*

### 3.3. Comprehensive Fairness Heatmap

A heatmap of all fairness ratios provides a comprehensive view of the comparison. The Multilevel Model consistently shows higher (more green) scores across all metrics.

![Fairness Heatmap](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/huaYnagxcwHaeBNXSxLKUk-images_1769324239719_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL2NvbXBhcmlzb25fZmFpcm5lc3NfaGVhdG1hcA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L2h1YVluYWd4Y3dIYWVCTlhTeExLVWstaW1hZ2VzXzE3NjkzMjQyMzk3MTlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMMk52YlhCaGNtbHpiMjVmWm1GcGNtNWxjM05mYUdWaGRHMWhjQS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=ZP5t9fXNF7yhpnamhEzZ96O3s8d1pmUc3VMc5aAfswrBhgNHDsVy-g~ILK0D1v5BKi~ATqOyZF0Z-qcFUjsmEVGDWkERAhWkTC1IZvq3rqvH-I~kospE4TcuqzQr7lAXatxfIiyOJDGReF37O84mbeHPwKoL9J3GOdyHDs-qWdGmRoYX9Ra8W7wPwA1H3ji4cln5vgkDmoE5fBgtsFnulAl80GAsI3A~k9w1-Ks9VN8lws1dHUdmoUl26TcuBjID3cAsWW~ZjGnQsJjdXsZ5D3I-qUXCaneqoQshESnS~O5ZSHil~CgJ-Tiv-bkEVxeVID-iWcKoOLtGd~2io37ptg__)
*Figure 3: The Multilevel Model column is consistently greener, indicating superior performance across all fairness metrics evaluated.*

## 4. Conclusion: The Least Biased Model

Based on this comparative analysis, the **Multilevel Model is the least biased and most fair** of the three models.

**Why is the Multilevel Model more fair?**

By accounting for the clustering of cases within judicial districts, the multilevel model can better distinguish between disparities caused by individual-level factors and those that may be attributable to systemic differences between districts. This allows the model to make more nuanced and less biased predictions.

### Implications for Your Portfolio

This comparative analysis is a powerful addition to your portfolio. It demonstrates:

-   **Advanced Modeling Skills**: You can build and compare sophisticated models like multilevel and mediation analyses.
-   **Deep Understanding of Fairness**: You can conduct a nuanced, comparative fairness analysis and interpret the results.
-   **Rigorous Model Selection**: You can justify your choice of a final model not just on accuracy, but also on its ethical performance.

This elevates the project from a simple prediction task to a sophisticated piece of data science research that grapples with complex, real-world challenges.
