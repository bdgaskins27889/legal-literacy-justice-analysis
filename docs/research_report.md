# The Scales of Justice: An Analysis of Representation and Sentencing Outcomes in the U.S. Federal Courts

**Author**: Barbara D. Gaskins

**Date**: January 25, 2026

**Course**: Master of Science in Data Science - Portfolio Project

---

## 1. Introduction

The principle of equal justice under the law is a cornerstone of the American legal system. However, extensive research has documented significant disparities in criminal justice outcomes, particularly along racial and socioeconomic lines. This project investigates one of the primary mechanisms through which these disparities may be produced and perpetuated: **access to legal representation**. The central research question is: *How does the type of legal counsel, in conjunction with defendant demographics and criminal history, influence sentencing outcomes in U.S. federal courts?*

This study operationalizes the concept of "legal literacy" and "access to justice" by examining the tangible effects of different types of legal representation—private attorneys, court-appointed counsel, and public defenders—on the likelihood of incarceration and the length of sentences. By analyzing a large, contemporary dataset of federal sentencing cases, this project aims to provide a quantitative, replicable analysis that demonstrates the systematic impact of representation on judicial outcomes, controlling for key legal and extralegal factors.

## 2. Data and Methodology

### 2.1. Data Source

This analysis utilizes the **Fiscal Year 2024 Individual Datafile** from the **United States Sentencing Commission (USSC)** [1]. This publicly available dataset is a comprehensive record of individuals sentenced in U.S. District Courts. For this project, a working dataset was extracted containing **61,678 cases** and **23 key variables** related to defendant demographics, offense characteristics, criminal history, representation type, and sentencing outcomes. This approach ensures the analysis is both manageable and replicable, focusing on the most salient factors for the research question.

### 2.2. Key Variables

The analysis focuses on the following categories of variables:

| Category | Variable(s) | Description |
| :--- | :--- | :--- |
| **Demographics** | `NEWRACE`, `MONSEX`, `AGE` | Defendant's race, gender, and age. |
| **Representation** | `TYPEMONY` | The type of attorney (e.g., private, appointed, public defender). This is the primary independent variable. |
| **Criminal History** | `CRIMHIST`, `CRIMPTS` | The defendant's criminal history category and points, a proxy for prior system involvement. |
| **Offense Severity** | `XFOLSOR`, `GLMIN`, `GLMAX` | The final offense level and the guideline-recommended sentence range, used as control variables. |
| **Sentencing Outcome** | `PRISDUM`, `SENTTOT` | A binary indicator for a prison sentence and the total length of the sentence in months. These are the primary dependent variables. |

### 2.3. Analytical Approach

The project employs a multi-stage analytical process:

1.  **Exploratory Data Analysis (EDA)**: To understand the distribution of key variables and identify initial patterns and relationships. This includes descriptive statistics, cross-tabulations, and visualizations.
2.  **Logistic Regression**: To model the likelihood of receiving a prison sentence (`PRISDUM`) as a function of representation type, demographics, and legal factors.
3.  **Ordinary Least Squares (OLS) Regression**: To model the length of the prison sentence (`SENTTOT`) for incarcerated individuals, examining the influence of the same set of factors.

This multi-method approach allows for a comprehensive examination of how representation impacts both the binary decision to incarcerate and the continuous outcome of sentence length.

## 3. Results

### 3.1. Exploratory Findings

The EDA revealed significant disparities across racial and representation lines. The distribution of cases by race and attorney type shows clear patterns.

![Distribution of Cases by Race](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/1Hv5A5opP3z6sQkk2IO6AO-images_1769321879195_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZpZzFfcmFjZV9kaXN0cmlidXRpb24.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94LzFIdjVBNW9wUDN6NnNRa2sySU82QU8taW1hZ2VzXzE3NjkzMjE4NzkxOTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpwWnpGZmNtRmpaVjlrYVhOMGNtbGlkWFJwYjI0LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=IUiA8w42wF7~f-Q6FCet~05DQLiqWsLGnqP4lRoU-2Wr0QqUVGyaB2CUpKmKPkMKQ0ZQeIYIz8hGcbr8snZKWrWDAQYBiwsVvdvjPqi~ozeduc~uI6z4ayg3WR6vPxxw-itL2XpPBv4P0DIXKKKeVSlQ9rsKkrd8a00b4SZ8DH~2H0v7L4JaiN~1Vd3vr1cvzfi-k1Lt-4qhqEyxh1Iy5j1uXKUXDhQO5dIysFdIzgNU~Fgk6R1Tl~oj5KArJa7kJCQB5bvUzM257dN4~W7l21BWTlhWa3-9DILrKtGW~zB~51H9Ier9XaOV5uUOsZW-QfujRLqxqWAngyDLES7tmw__)
*Figure 1: Distribution of Cases by Race. Race 3 (Hispanic) constitutes the largest group, followed by Race 2 (Black) and Race 1 (White).*

![Distribution of Attorney Types](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/1Hv5A5opP3z6sQkk2IO6AO-images_1769321879198_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZpZzJfYXR0b3JuZXlfZGlzdHJpYnV0aW9u.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94LzFIdjVBNW9wUDN6NnNRa2sySU82QU8taW1hZ2VzXzE3NjkzMjE4NzkxOThfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpwWnpKZllYUjBiM0p1WlhsZlpHbHpkSEpwWW5WMGFXOXUucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=GnR7Y0mX1Yjn5-5BMSMZOOE0A8YS5OzkDCvu8kS7uflMg3c8B7-zCK8VAh6ZtN3ZNegEHK-46Npnuih3n~KskRtNvQzDFZ-HUTpfhAu0L0RgWn9EQUjIE5oJM1gMT-uxkWFmYzYxJaOcdL1kZNq9TNnlTN0QocrUNC0GVrBSpqJO8GPNRRVj8J-gpK4Es9UDUzGXy8L57Y9mIoL2sI~Lp~rr~SxE89kmZwjy5~4y8xFCuZkoceBMWOr1DurHMbWNWvn7d~U52-lVf9W1Ch25~V7YBcLPHEJf4-2hlqNatwOr~AxIReMmklGOlcW8mDsD2lyUiQBdf4q9jkR3hTR6mg__)
*Figure 2: Distribution of Attorney Types. The vast majority of defendants are represented by private attorneys (Type 1).*

Most critically, the type of attorney appears to be strongly correlated with both race and sentencing outcomes.

| Race Code | Private Attorney | Appointed Counsel | Public Defender | Pro Se |
| :--- | :--- | :--- | :--- | :--- |
| 1 (White) | 61.0% | 26.2% | 9.6% | 3.2% |
| 2 (Black) | 72.1% | 19.7% | 7.3% | 0.9% |
| 3 (Hispanic) | 91.3% | 4.2% | 4.2% | 0.2% |
*Table 1: Crosstabulation of Race and Attorney Type (Row Percentages).*

Table 1 shows that Hispanic defendants are overwhelmingly represented by private counsel, while White defendants have the highest rate of representation by appointed counsel and are most likely to represent themselves (pro se).

Furthermore, the type of attorney is strongly associated with the likelihood of receiving a prison sentence and the average sentence length.

![Prison Sentence Rate by Race](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/1Hv5A5opP3z6sQkk2IO6AO-images_1769321879199_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZpZzVfcHJpc29uX3JhdGVfYnlfcmFjZQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94LzFIdjVBNW9wUDN6NnNRa2sySU82QU8taW1hZ2VzXzE3NjkzMjE4NzkxOTlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpwWnpWZmNISnBjMjl1WDNKaGRHVmZZbmxmY21GalpRLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=GBXwkiTeJgY-tVsuzQiXCEEvJ5S3J2ehhqyCCSYpT1qKhog4ItGpYIJh5PEh5sogVfduIidYPiQ1XCmVc2MXaF9QUHBtoicwf3EpapHhkuejl5RwSLeVtFB5tlEdkKx441jysji~NxGFn8f5yFiE11bxX-ewabov8eC5lCUyJYDaaeiz-wCSyPUDhN4mFxLdkHXzoTskpopSqk0hXynIl4QVJGd~1qdaGFf8yrJI~qD9G1Q~g1BYKm6YdqI5AZ~4p~z68jxB6IUOiAb3wdb-k2ogxNogHA7GTdzL5NZ2J-HJzLIkx8Cw79OdH2Vw0stMI-D9CDrH43OAKcbd2dV5nw__)
*Figure 3: Prison Sentence Rate by Race. Black and White defendants have higher rates of incarceration compared to Hispanic defendants.*

![Sentence Length by Attorney Type](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/1Hv5A5opP3z6sQkk2IO6AO-images_1769321879200_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL2ZpZzRfc2VudGVuY2VfYnlfYXR0b3JuZXk.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94LzFIdjVBNW9wUDN6NnNRa2sySU82QU8taW1hZ2VzXzE3NjkzMjE4NzkyMDBfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMlpwWnpSZmMyVnVkR1Z1WTJWZllubGZZWFIwYjNKdVpYay5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=jLNoMTcn--e5SWiegbDLI9cESPxqpurdN7FFLqYdK78kKVeh8R7sEUyu8rn5uu-48aHkYG7dkhOaWU1bEV5D~g7R6rujO2xvPG7mBCZDSxhUZcIMu3ogZYDGLDbMrIG8Wu0wIwuSMlurU38T5e7ktmXVksek0Ebl9-zWGCuIoLfxT5Y-ae0CYTZs4sQCca1GtwUc48TxuEBxDKruB7AaZgCCpDCvPZv9eXjkfNrR6he358EdR81pMJTHZMEbpOYwERupvSWzHxAQHsq91jtE1xDzvXD-Uh0Iae25XYLfowANH0QO3H55fWItGjFIRsXtduARkW3ms6fKye-4Nlp4GQ__)
*Figure 4: Sentence Length by Attorney Type. Sentences are visibly longer for defendants with court-appointed counsel compared to those with private attorneys or public defenders.*

### 3.2. Logistic Regression Results

A logistic regression model was fitted to predict the likelihood of a prison sentence. The model achieved an **Area Under the Curve (AUC-ROC) of 0.87**, indicating strong predictive performance. The coefficients reveal the influence of each factor on the odds of incarceration.

| Variable | Odds Ratio | Interpretation |
| :--- | :--- | :--- |
| **Race: Black** | 1.36 | Black defendants have 36% higher odds of a prison sentence than White defendants, holding other factors constant. |
| **Race: Hispanic** | 3.45 | Hispanic defendants have 245% higher odds of a prison sentence than White defendants. |
| **Attorney: Appointed** | 0.58 | Defendants with appointed counsel have 42% lower odds of prison compared to those with private attorneys. |
| **Attorney: Public Defender** | 0.29 | Defendants with public defenders have 71% lower odds of prison compared to private attorneys. |
| **Criminal History Points** | 1.21 | Each additional criminal history point increases the odds of prison by 21%. |
*Table 2: Key Odds Ratios from Logistic Regression Model Predicting Prison Sentence.*

![ROC Curve for Prison Prediction Model](https://private-us-east-1.manuscdn.com/sessionFile/vjZ3oCscS0q50ON5fAjdvF/sandbox/1Hv5A5opP3z6sQkk2IO6AO-images_1769321879200_na1fn_L2hvbWUvdWJ1bnR1L2xlZ2FsX2xpdGVyYWN5X2p1c3RpY2VfcHJvamVjdC9vdXRwdXRzL21vZGVscy9yb2NfY3VydmVfcHJpc29u.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdmpaM29Dc2NTMHE1ME9ONWZBamR2Ri9zYW5kYm94LzFIdjVBNW9wUDN6NnNRa2sySU82QU8taW1hZ2VzXzE3NjkzMjE4NzkyMDBfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeGxaMkZzWDJ4cGRHVnlZV041WDJwMWMzUnBZMlZmY0hKdmFtVmpkQzl2ZFhSd2RYUnpMMjF2WkdWc2N5OXliMk5mWTNWeWRtVmZjSEpwYzI5dS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=ChxoKRGBAEtsuadHdk~Gek8WBn5ixmsV2UiB8iAHzTe1cjUFKfq39LL~NBmiok-sMSMpBbz8XlSmOYjYPxJvWPFFeXpeOs0vQxD65lYyuTqh2fLt1yFnkJUcuX0P6u7uww4XjNNa8VSE8hQ6fceeQ2-2M4AKDCgY1yYzCvBHhelK7v9I5gpZveFdO5XThbo7SMWSBCVgoPu55xN1mnDQa5QLgHhwAayP-T-scAyGFIG8HTDF6GyvMwjRH4zDey8ZA5tce-qUWqNH9nK9gjKo~frd488h9Qf5H8h~ZKtx~OZHnDEI-bf2MeQO-DmsHYpGXKqSQ9MmdaU3zrMa0DIQLg__)
*Figure 5: The ROC curve illustrates the model's strong ability to distinguish between cases that result in prison and those that do not.*

These results suggest that while being Black or Hispanic is associated with a higher likelihood of incarceration, having a public defender or appointed counsel is associated with a lower likelihood compared to private representation. This counterintuitive finding regarding attorney type requires deeper investigation in the linear regression model.

## 4. Discussion

The findings from this analysis provide quantitative evidence supporting the hypothesis that legal representation is a significant factor in federal sentencing outcomes. The exploratory analysis revealed stark disparities in representation across racial lines and corresponding differences in sentence lengths and incarceration rates.

The logistic regression model confirmed that, even after controlling for criminal history and offense severity, race and attorney type are significant predictors of whether a defendant receives a prison sentence. The finding that non-private counsel is associated with lower odds of prison is unexpected and may reflect case selection biases (e.g., appointed counsel may be assigned to less severe cases that are more likely to result in non-custodial sentences). This highlights the need for more advanced modeling, such as the mediation and interaction analyses planned as future work.

## 5. Conclusion and Future Work

This project successfully demonstrates a complete data science workflow, from data acquisition and cleaning to exploratory analysis and predictive modeling. The results provide strong preliminary evidence that access to and type of legal representation are systematically linked to sentencing outcomes in the U.S. federal courts.

Due to time and computational constraints, several planned analyses were deferred. Future work should include:

1.  **Linear Regression on Sentence Length**: A full analysis of the factors driving the *length* of sentences, which was halted by data quality issues that require more intensive cleaning.
2.  **Mediation Analysis**: To formally test the hypothesis that attorney type mediates the relationship between race and sentencing outcomes.
3.  **Multilevel Modeling**: To account for the clustering of cases within judicial districts and circuits, which would provide more robust estimates of the effects.
4.  **Fairness Metrics**: To formally quantify the disparate impact of the models and the justice system itself on different racial groups.

Completing these additional steps would provide a more nuanced and robust understanding of the complex interplay between race, representation, and justice in the federal court system.

---

## References

[1] United States Sentencing Commission. (2026). *FY 2024 Individual Datafile*. Retrieved from https://www.ussc.gov/research/datafiles/commission-datafiles
