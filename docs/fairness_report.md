# Fairness Analysis Report: Logistic Regression Model

**Author**: Barbara D. Gaskins

**Date**: January 25, 2026

**Project**: The Scales of Justice: An Analysis of Representation and Sentencing Outcomes

---

## 1. Executive Summary

This report details the fairness analysis conducted on the logistic regression model developed to predict the likelihood of a prison sentence in U.S. federal courts. The analysis assesses whether the model exhibits bias across different racial groups, using standard fairness metrics from the `fairlearn` library. 

The key finding is that the model **fails to meet standard criteria for fairness**, exhibiting significant disparities in both its predictions and its error rates across racial groups. Specifically, the model shows evidence of **disparate impact** and does not satisfy the conditions for **equal opportunity** or **equalized odds**.

## 2. Fairness Metrics Overview

Three primary fairness criteria were evaluated:

1.  **Demographic Parity (Disparate Impact)**: This metric assesses whether the model predicts a positive outcome (in this case, a prison sentence) at equal rates across different groups. A common threshold for fairness is the "80% rule," which states that the selection rate for any group should be at least 80% of the rate for the group with the highest rate.

2.  **Equal Opportunity**: This metric requires that the model has an equal True Positive Rate (TPR) across groups. In this context, it means the model should be equally good at correctly identifying individuals who will receive a prison sentence, regardless of their race.

3.  **Equalized Odds**: This is a stricter criterion that requires the model to have both an equal True Positive Rate (TPR) and an equal False Positive Rate (FPR) across groups. This means the model should have balanced error rates for all groups.

## 3. Analysis Results

The analysis revealed significant disparities across all major fairness metrics.

### 3.1. Disparate Impact (Demographic Parity)

The model fails the 80% rule for demographic parity.

-   **Demographic Parity Ratio**: 0.706
-   **Interpretation**: The selection rate (predicted prison sentence) for the least-favored group (Other) is only **70.6%** of the rate for the most-favored group (Black). This is below the 80% threshold, indicating the presence of disparate impact.

![Selection Rate by Race](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/nQWH9t1taxIo2QBm6q4so6-images_1769322318591_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL3NlbGVjdGlvbl9yYXRlX2J5X3JhY2U.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L25RV0g5dDF0YXhJbzJRQm02cTRzbzYtaW1hZ2VzXzE3NjkzMjIzMTg1OTFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMM05sYkdWamRHbHZibDl5WVhSbFgySjVYM0poWTJVLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=LMZAPrgaSiOCu~1UC~TryMrY9IrXgA4BqOFCxC3lVHcKEgFaOWjdQXnp2~f~iOw6mPctO6k7e4gL1BCN1JuIetE19fNXTzTfp31rrlyheqvPUP-Diod7RVjlgpQTxJ4p6TxrBXnpTfSVf4yn~Bjd1KsDceZafmMlXjaoNrDvdztInAOVc8DMphVfEtC-nHJMj7uV1tEXYxnzJXicLTrMwcTIVB62D4TNRJPtJVmB4ssbFa4UiLNA-gjJgQKAtrCXn6pu7wg9XAZTTR77IJOi0ib1BW7HremTMAiNahfH-GDXSlev0S9QNvATxZO~bhVUWEcOiNRjnAklwUIPAqYZLA__)
*Figure 1: The model predicts prison sentences at substantially different rates for different racial groups, with Black defendants having the highest selection rate and defendants of "Other" races having the lowest.*

### 3.2. Equal Opportunity

The model does not provide equal opportunity across racial groups.

-   **True Positive Rate (TPR) Difference**: 0.239
-   **Interpretation**: There is a **23.9 percentage point difference** between the highest TPR (Black defendants, 82.7%) and the lowest TPR (Other defendants, 58.8%). This means the model is significantly better at correctly identifying prison-bound individuals for some racial groups than for others.

![True Positive Rate by Race](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/nQWH9t1taxIo2QBm6q4so6-images_1769322318592_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL3RydWVfcG9zaXRpdmVfcmF0ZV9ieV9yYWNl.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L25RV0g5dDF0YXhJbzJRQm02cTRzbzYtaW1hZ2VzXzE3NjkzMjIzMTg1OTJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMM1J5ZFdWZmNHOXphWFJwZG1WZmNtRjBaVjlpZVY5eVlXTmwucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=JDBZ2u8kqlCv0CUxJhZWQ5Qi6CjJkAP9Z0xGrBmAd7HfKgv98sw1uHeTRY~dmAg3Z7kXvQ0kdMxuehKR5K9Qt8ZTs9E0~8ketJ6o0nPdC7kLC9ohA9WTyFUoer~gZoGM-mhUg~zNTESS--psSX-XAaRXvninzw7pf5oE~ppHByi5TktgVOI~g75z1MEZQDLJds23P06cY78R-rNBhf51sn1AyEKxJrs-X4o6bPcR3yDZ2XKPACS9u-TbGtcoWcYpq1SyIYBKcD-5fIPAOq61jcYdtkr1g7XO7cUTAERzSj97b4kN3jp93Vo4SNHRPJ6RoY4hf6aPKqUFv2uySDR3hw__)
*Figure 2: The model correctly identifies a much higher proportion of actual prison cases for Black defendants compared to White and Other defendants.*

### 3.3. Equalized Odds

The model fails to meet the equalized odds criterion.

-   **Equalized Odds Difference**: 0.239 (driven by the large TPR difference)
-   **False Positive Rate (FPR) Difference**: 0.171
-   **Interpretation**: The model has unequal error rates. Most notably, the False Positive Rate for Hispanic defendants (27.5%) is **more than double** the rate for White defendants (10.4%). This means a Hispanic individual who should *not* receive a prison sentence is far more likely to be incorrectly predicted to receive one by the model compared to a White individual.

![False Positive Rate by Race](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/nQWH9t1taxIo2QBm6q4so6-images_1769322318593_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL2ZhbHNlX3Bvc2l0aXZlX3JhdGVfYnlfcmFjZQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L25RV0g5dDF0YXhJbzJRQm02cTRzbzYtaW1hZ2VzXzE3NjkzMjIzMTg1OTNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMMlpoYkhObFgzQnZjMmwwYVhabFgzSmhkR1ZmWW5sZmNtRmpaUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=a3dZGbG-sGQJp8ZNRBgsGzOJb~Yvm6kKo6SXaV5XdjXJJx8xnxk0cVFpDbeweMtLU3ROcXQ3Nrw91pM6VSp5-We7h0uy8lORFhFujtXRqGEq96jJ9BkFA5cF4qxUbfHalWeO7Hfys3lWSA6foMwd5aQY5fvNIQ8WFRVLtEJ0gGtBPXXCTO1xHJwXw-SNUSjVttYG5kokdDQPLOIAwNZB7VpjaasH8CcI-CwiUIEW-SPdsMekcdUMXBtfagcrLaTiBDNOW7DzS5LNvXJHIVtfwwWzmRgH075lsIRgmyxFeLqkMkcYFlh8p6QrCnALCdnLnO4bUrmR2sl93SLwoeQbtA__)
*Figure 3: The model incorrectly predicts a prison sentence for non-prison-bound Hispanic defendants at a much higher rate than for other groups.*

## 4. Summary of Metrics

The following table summarizes the key fairness metrics across racial groups:

| Metric | Black | Hispanic | Other | White | **Disparity (Max - Min)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Selection Rate** | 0.774 | 0.729 | 0.547 | 0.642 | **0.227** |
| **True Positive Rate** | 0.827 | 0.755 | 0.588 | 0.717 | **0.239** |
| **False Positive Rate** | 0.143 | 0.275 | 0.152 | 0.104 | **0.171** |
| **False Negative Rate** | 0.173 | 0.245 | 0.412 | 0.283 | **0.239** |

![Fairness Metrics Comparison](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/nQWH9t1taxIo2QBm6q4so6-images_1769322318593_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZhaXJuZXNzL2ZhaXJuZXNzX21ldHJpY3NfY29tcGFyaXNvbg.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94L25RV0g5dDF0YXhJbzJRQm02cTRzbzYtaW1hZ2VzXzE3NjkzMjIzMTg1OTNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpoYVhKdVpYTnpMMlpoYVhKdVpYTnpYMjFsZEhKcFkzTmZZMjl0Y0dGeWFYTnZiZy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=t5Ht8yuzfVvcm81FpMopmjgDk6Je9ydlOgyNbar7bhkytG6UIwWziihxU6iJm7mGYMlwKXRH~NLREBXGtbyMtw~z~qVz7B5xFDYEFTdv5xwclqhQaOQwO6uew3eXLvNUvEnzrBL0LjzglVmlxUwhDreuGEylMxdlsn1iUJWICEjjuFierePBnU6zQcU9sCBca~IobU2XdZH4G4dluIPMkxU8aU3hoZdJu3YA-ln1PMAByukn0Ovx6gi3Nwksu8Qt2wr-OdcsB0YWm9IZPa80t-RHbQc7dtLA~1ExNxXYsq7vNUOqb9YcxUJUrBHKQe7UejXNXDDPS8Euh37NY3AjRw__)
*Figure 4: This chart provides a comprehensive view of the disparities across the four primary fairness metrics, highlighting the model's inconsistent performance across racial groups.*

## 5. Conclusion and Implications

The fairness analysis demonstrates that the logistic regression model, while having good overall predictive accuracy, is **not fair** in its application across different racial groups. The model exhibits biases that could lead to discriminatory outcomes if deployed in a real-world setting.

-   **Disparate Impact**: The model disproportionately predicts prison sentences for Black and Hispanic defendants.
-   **Unequal Errors**: The model makes different types of errors for different groups. It is more likely to incorrectly flag a non-prison-bound Hispanic individual for prison (high FPR) and more likely to fail to identify a prison-bound White or Other individual (high FNR).

These findings are critical for a comprehensive data science portfolio project. They show an understanding of the ethical implications of machine learning and the ability to diagnose and quantify algorithmic bias. Any real-world application of this model would require significant mitigation steps to address these fairness issues, such as re-weighting the data, using fairness-aware algorithms, or adjusting the prediction threshold for different groups.

This analysis adds a crucial layer of depth to the project, moving beyond simple predictive accuracy to a more nuanced evaluation of the model's societal impact.
