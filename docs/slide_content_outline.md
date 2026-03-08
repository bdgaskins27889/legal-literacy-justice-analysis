# Slide Content: The Scales of Justice
## DSC 680: Applied Data Science | Barbara D. Gaskins | March 2026

---

## Slide 1 — Title Slide

**Title:** The Scales of Justice

**Subtitle:** An Analysis of Legal Representation and Sentencing Outcomes in U.S. Federal Courts

**Author:** Barbara D. Gaskins
**Course:** DSC 680: Applied Data Science
**Date:** March 2026
**Data Source:** U.S. Sentencing Commission, FY 2024

> *Visual note: Dark navy background with gold scales-of-justice accent. Clean, authoritative, academic.*

**Speaker Notes:** Good [morning/afternoon/evening]. My name is Barbara Gaskins, and today I am presenting my capstone project for DSC 680. This project is titled "The Scales of Justice," and it uses federal sentencing data to ask a deceptively simple question: does the type of lawyer you have actually change the outcome of your case? The answer, as the data will show, is a resounding yes — and the implications reach far beyond the courtroom.

---

## Slide 2 — The Central Question

**Heading:** Equal Justice Under Law — But Is It Equal in Practice?

**Body:**
- The Sixth Amendment guarantees the right to counsel, but not the right to *equal* counsel
- 80% of criminal defendants in the U.S. rely on court-appointed public defenders
- Public defender caseloads average **300–500 cases per year** — far exceeding ABA recommendations of 150
- This study asks: **Does the type of legal representation predict the severity of a federal sentence?**

**Pull Quote:** *"The quality of justice a person receives should not depend on the size of their wallet."*

**Speaker Notes:** The Sixth Amendment guarantees every defendant the right to an attorney. But the right to an attorney is not the same as the right to an equally resourced attorney. Public defenders are among the most dedicated lawyers in the country, but they are systematically overworked and underfunded. The American Bar Association recommends a maximum of 150 felony cases per year per attorney. Studies show many public defenders carry two to three times that load. This study uses data science to ask whether that resource gap translates into a sentencing gap.

---

## Slide 3 — The Dataset: 61,679 Federal Cases

**Heading:** A Comprehensive, Publicly Verifiable Dataset from the Federal Government

**Body — two-column layout:**

**Left — Dataset Attributes:**
| Attribute | Value |
|:---|:---|
| Source | U.S. Sentencing Commission |
| Fiscal Year | 2024 |
| Total Cases | 61,679 |
| Variables Available | 27,000+ |
| Key Variables Used | 23 |

**Right — Key Variables Selected:**
- Race/Ethnicity (`NEWRACE`)
- Age at sentencing (`AGE`)
- Criminal history score (`CRIMINAL_HISTORY`)
- Type of legal counsel (`TYPEMONY`)
- Federal district (`DISTRICT`)
- Prison sentence outcome (`PRISDUM`)

**Speaker Notes:** The dataset powering this analysis comes directly from the U.S. Sentencing Commission — the independent federal agency responsible for establishing sentencing policies for the federal courts. This data is publicly available, fully anonymized, and updated annually, making it ideal for reproducible research. From the over 27,000 available variables, I selected 23 that are most relevant to the research question. The most critical variable is TYPEMONY, which records whether a defendant was represented by a private attorney, a public defender, or represented themselves.

---

## Slide 4 — Conceptual Framework: The Mediation Pathway

**Heading:** Legal Representation Sits at the Crossroads of Race and Sentencing

**Body:**
The analysis tests a mediation model with three components:
1. **Independent Variable:** Race and demographic characteristics
2. **Mediator:** Type of legal representation
3. **Outcome:** Prison sentence (yes/no) and sentence length (months)

A **direct effect** of race on sentencing is also tested, alongside the **indirect effect** operating through representation type.

*[Embed Figure 5 — Conceptual Framework Diagram]*

**Speaker Notes:** Before diving into the numbers, it is important to understand the conceptual model guiding this research. I am not simply asking whether race predicts sentencing — that relationship is well-documented in the literature. I am asking whether legal representation *mediates* that relationship. In other words, does part of the reason Black and Hispanic defendants receive harsher sentences operate through the fact that they are more likely to have court-appointed counsel? This diagram illustrates that pathway. The dashed blue line represents the direct effect of race on sentencing. The solid lines represent the indirect pathway running through the type of attorney. Disentangling these two pathways is the core analytical challenge of this project.

---

## Slide 5 — Finding 1: Race Predicts Prison Sentences

**Heading:** Hispanic Defendants Are Sentenced to Prison at a Rate 29% Higher Than White Defendants

**Body:**
- **White (Non-Hispanic):** 72.4% sentenced to prison
- **Black (Non-Hispanic):** 88.6% sentenced to prison
- **Hispanic:** 93.1% sentenced to prison — the highest of any group
- **Other:** 78.2% sentenced to prison
- Overall average: **83.1%**

*[Embed Figure 1 — Prison Rate by Race/Ethnicity bar chart]*

**Speaker Notes:** This chart presents one of the most striking findings of the exploratory analysis. When we look at the raw prison sentence rates by race and ethnicity, we see a 20-percentage-point gap between White, non-Hispanic defendants and Hispanic defendants. Nearly 93 out of every 100 Hispanic defendants in federal court in FY 2024 received a prison sentence, compared to roughly 72 out of 100 White defendants. It is critical to note that this is a descriptive finding — it does not yet control for offense severity, criminal history, or type of representation. That is exactly what the modeling phase does. But this raw disparity is the starting point, and it demands explanation.

---

## Slide 6 — Finding 2: Attorney Type Predicts Sentence Length

**Heading:** Defendants Without Private Attorneys Serve an Average of 35 More Months in Prison

**Body:**
| Attorney Type | Average Sentence Length |
|:---|:---|
| Private Attorney | **53.2 months** |
| Other Counsel | 65.7 months |
| Public Defender | 78.4 months |
| Pro Se (Self-Represented) | **88.1 months** |

- Gap between private attorney and pro se: **34.9 months** (nearly 3 years)
- Gap between private attorney and public defender: **25.2 months** (over 2 years)

*[Embed Figure 2 — Average Sentence Length by Attorney Type]*

**Speaker Notes:** This is perhaps the most policy-relevant finding in the entire study. When we look at average sentence length broken down by the type of attorney, the differences are dramatic. Defendants with private attorneys averaged 53 months in prison. Defendants with public defenders averaged 78 months — a difference of over two years. Defendants who represented themselves averaged 88 months — nearly three years longer than those with private counsel. Now, a critical thinker will immediately ask: isn't this just because wealthier defendants who can afford private attorneys also tend to commit less serious crimes? That is a fair challenge, and it is precisely what the regression models are designed to address by controlling for offense severity and criminal history.

---

## Slide 7 — Methodology: Three Models, One Goal

**Heading:** Three Distinct Models Tested for Both Accuracy and Fairness

**Body:**

**Model 1 — Logistic Regression (Baseline)**
Predicts prison sentence (yes/no) from demographics, criminal history, and attorney type. Standard L2 regularization.

**Model 2 — Multilevel Model (Context-Aware)**
A mixed-effects logistic regression that adds a random intercept for each of the 94 federal districts, accounting for geographic variation in sentencing culture.

**Model 3 — Mediation Analysis**
A two-stage regression that isolates the *indirect* effect of race on sentencing operating through attorney type, separating it from the direct effect.

**Speaker Notes:** Three different models were developed, each designed to answer a slightly different question. The Logistic Regression is the workhorse — it gives us a clean, interpretable baseline. The Multilevel Model is the most sophisticated. It recognizes that federal sentencing does not happen in a vacuum — a case in the Southern District of New York is processed in a very different environment than a case in the Eastern District of Texas. By adding a random intercept for each district, the model accounts for this geographic variation. The Mediation Analysis is the most theoretically interesting — it directly tests the hypothesis that legal representation is the mechanism through which racial disparities in sentencing operate.

---

## Slide 8 — Model Performance: Accuracy

**Heading:** All Three Models Achieve Strong Predictive Accuracy, Led by the Multilevel Model

**Body:**
| Model | AUC-ROC | Accuracy |
|:---|:---|:---|
| Logistic Regression | 0.87 | 77.8% |
| **Multilevel Model** | **0.89** | **80.1%** |
| Mediation Analysis | 0.83 | 76.2% |

- AUC-ROC of 0.87–0.89 indicates **strong discriminative ability**
- Multilevel Model outperforms on both metrics
- All models significantly outperform random chance (AUC = 0.50)

*[Embed Figure 3 — Model Performance Comparison]*

**Speaker Notes:** In terms of raw predictive performance, all three models are strong. An AUC-ROC above 0.80 is generally considered a good model; above 0.85 is considered very good. The Multilevel Model leads with an AUC of 0.89 and an accuracy of 80.1%, meaning it correctly predicts the sentencing outcome for more than four out of every five cases. However, accuracy alone is an insufficient standard for a model that could be used in a justice context. A model could be highly accurate overall while being systematically wrong for a particular racial group. That is why the fairness audit is not an afterthought — it is the central evaluation criterion.

---

## Slide 9 — Model Fairness: Only One Model Passes the 80% Rule

**Heading:** The Multilevel Model Is the Only Model to Pass the Standard Disparate Impact Test

**Body:**
- The **80% Rule** (EEOC standard): A model passes if the selection rate for the least-favored group is at least 80% of the rate for the most-favored group
- **Logistic Regression:** Demographic Parity Ratio = **0.706 — FAILS ✗**
- **Multilevel Model:** Demographic Parity Ratio = **0.816 — PASSES ✓**
- Improvement: **+15.6 percentage points**
- The Multilevel Model also reduces selection rate disparity by **37%** and FPR disparity by **41.8%**

*[Embed Figure 4 — Fairness Metrics Comparison]*

**Speaker Notes:** This is the most important slide in the presentation. The 80% rule, originally developed by the EEOC for employment discrimination cases, provides a clear, defensible threshold for evaluating whether a model has a disparate impact on a protected group. The standard Logistic Regression model fails this test with a ratio of 0.706 — meaning the model is significantly more likely to predict prison for Black and Hispanic defendants than for White defendants, even after controlling for other factors. The Multilevel Model, by contrast, passes with a ratio of 0.816. This is not a marginal improvement. Across all fairness metrics, the Multilevel Model is dramatically better. The selection rate disparity drops by 37%. The false positive rate disparity — the rate at which the model incorrectly predicts prison for someone who should not receive it — drops by over 41%. This is the model we recommend.

---

## Slide 10 — Why the Multilevel Model Is Fairer

**Heading:** Accounting for Geographic Context Reduces Racial Bias by Over 37%

**Body:**
- Federal sentencing varies significantly by district — a known phenomenon called **"zip code justice"**
- Standard models treat all districts as identical, inadvertently encoding geographic bias that correlates with race
- The Multilevel Model adds a **random intercept per district**, separating district-level effects from individual-level race effects
- Statistical significance: Bootstrap test confirms improvement is **not due to chance (p < 0.001)**
- Effect size (Cohen's h): **0.21** — a meaningful, practically significant reduction in bias

**Speaker Notes:** Why does the Multilevel Model perform so much better on fairness? The answer lies in what statisticians call "omitted variable bias." Federal districts are not racially neutral environments. Some districts have historically higher incarceration rates; some have more resources for public defenders; some have different prosecutorial cultures. When a standard model ignores these district-level differences, it inadvertently attributes to race what is actually a function of geography. By explicitly modeling the district as a random effect, the Multilevel Model separates these two sources of variation. The result is a model that is both more accurate and more fair — a rare and important outcome that demonstrates that fairness and accuracy are not inherently in tension.

---

## Slide 11 — Discussion: What the Data Tells Us

**Heading:** The Data Reveals a System Where Access to Counsel Shapes the Scales of Justice

**Body:**
Three key conclusions emerge from this analysis:

1. **Representation matters, measurably.** After controlling for offense severity and criminal history, attorney type remains a significant predictor of sentence length — a gap of over two years.

2. **Standard AI models can amplify bias.** The Logistic Regression model failed the disparate impact test, demonstrating that deploying unaudited predictive tools in justice settings carries serious risk.

3. **Fairer models are achievable.** The Multilevel Model demonstrates that incorporating contextual information reduces algorithmic bias by over 37% without sacrificing accuracy.

**Speaker Notes:** Let me step back from the numbers for a moment and discuss what this all means. Three conclusions stand out. First, legal representation is not just symbolically important — it is quantifiably important. Even after we control for what you did, your criminal history, and where you were sentenced, who represents you still predicts how long you will be incarcerated. Second, this study is a cautionary tale for anyone who believes that algorithms are inherently neutral. The standard logistic regression model, built from real data, learned and reproduced the biases embedded in that data. Third, and most importantly, this study offers a path forward. The Multilevel Model shows that with more thoughtful modeling choices, we can build tools that are both accurate and fair.

---

## Slide 12 — Policy Implications

**Heading:** Data-Driven Evidence Supports Three Actionable Policy Reforms

**Body:**

**1. Invest in Public Defender Resources**
The sentencing gap between private and public defender clients is a resource gap. Reducing public defender caseloads to ABA-recommended levels is a direct, evidence-based intervention.

**2. Mandate Fairness Audits for Predictive Tools**
Any algorithm used in a justice context — risk assessment, bail, sentencing recommendations — must be audited against the 80% rule and equalized odds standards before deployment.

**3. Adopt Multilevel Modeling Standards**
Courts and researchers using predictive analytics in sentencing should adopt multilevel modeling approaches that account for district-level variation to reduce geographic bias.

**Speaker Notes:** This research is not just an academic exercise. It points toward three concrete policy recommendations. First, the most direct intervention is also the most straightforward: fund public defenders adequately. The data shows a clear correlation between representation quality and outcomes. Second, any jurisdiction considering the use of predictive analytics in sentencing or bail decisions must require a fairness audit as a condition of deployment. The tools exist; the will to use them must be mandated. Third, the modeling community should adopt multilevel approaches as a standard for justice applications. The improvement in fairness is significant, the computational cost is minimal, and the ethical stakes are too high to use less rigorous methods.

---

## Slide 13 — Limitations and Future Work

**Heading:** This Study Is a Foundation, Not a Final Word

**Body:**

**Current Limitations:**
- Federal courts represent only ~5% of all criminal cases in the U.S.
- Correlation, not causation: the study cannot fully rule out confounding variables
- The 80% rule is a threshold, not a guarantee of full fairness

**Future Research Directions:**
- Extend analysis to state-level court data for broader generalizability
- Incorporate plea bargain data to capture earlier stages of the process
- Develop a longitudinal model tracking the same cohort over multiple years
- Explore intersectionality (race × gender × income) as compound predictors

**Speaker Notes:** Good science is honest about its limitations. This study uses federal court data, which covers a relatively small and specialized slice of the American criminal justice system. The vast majority of criminal cases — over 95% — are handled in state courts, where the dynamics may be quite different. Additionally, while the statistical controls are rigorous, this is an observational study. We cannot randomly assign defendants to different attorney types, so we cannot claim causation with certainty. Future work should extend this framework to state-level data, incorporate earlier stages of the process like charging and plea bargaining, and explore the compounding effects of race, gender, and socioeconomic status together.

---

## Slide 14 — Conclusion

**Heading:** The Scales of Justice Can Be Recalibrated — With Data, Rigor, and Political Will

**Body:**
This study demonstrates that:

- **Legal representation is a measurable driver** of sentencing disparities in U.S. federal courts
- **Algorithmic fairness is achievable** — the Multilevel Model reduces bias by 37% while improving accuracy
- **Data science has a role** in diagnosing, and potentially correcting, systemic inequities in the justice system

*"The arc of the moral universe is long, but it bends toward justice."* — Dr. Martin Luther King Jr.

**Speaker Notes:** I want to close with a reflection on why this work matters. The criminal justice system is one of the most consequential institutions in American life. Decisions made within it affect not just individuals, but families and communities for generations. Data science cannot solve the deep structural inequities in this system. But it can illuminate them with a precision and scale that was not previously possible. It can hold models accountable to fairness standards. And it can provide policymakers with the evidence they need to act. The scales of justice are not perfectly balanced today. But with rigorous, responsible data science, we can understand exactly where the imbalance lies — and that is the first step toward correcting it. Thank you.

---

## Slide 15 — Questions & Answers

**Heading:** Anticipated Questions

**Body — two columns:**

**Column 1:**
1. Isn't this just about ability to pay, not attorney quality?
2. Does this data account for crime severity?
3. What is a Multilevel Model in plain terms?
4. Is the 80% rule the right standard for justice?
5. Could this model be misused by prosecutors?

**Column 2:**
6. What specific policy changes do you recommend?
7. What is the root cause — overworked defenders or better private attorneys?
8. How would state court data differ?
9. Is it ethical to use a model that still has some bias?
10. What comes next in this research?

**Speaker Notes:** I have prepared answers to each of these questions. I will address them as they arise, but I want to briefly acknowledge the most important one: question 9 — is it ethical to use a model that still has some bias? My answer is: it depends on the alternative. If the alternative is a human decision-maker who is also biased — and the research on judicial bias is extensive — then a model that is more transparent, auditable, and demonstrably fairer may be the more ethical choice. The goal is not a perfect model. The goal is a more just system.

---

## Slide 16 — References & Data Availability

**Heading:** All Data and Code Are Publicly Available for Independent Verification

**Body:**

**Primary Data Source:**
United States Sentencing Commission. (2025). *Individual Offender Datafiles, FY 1999–2024*. https://www.ussc.gov/research/datafiles/commission-datafiles

**Code Repository:**
Full Python analysis scripts, model specifications, and fairness audit code available on GitHub.

**Key Python Libraries Used:**
`scikit-learn` | `statsmodels` | `fairlearn` | `pandas` | `matplotlib` | `seaborn`

**Reproducibility Statement:**
All analyses use a fixed random seed (42). Results can be independently replicated using the publicly available USSC dataset and the provided code.

**Speaker Notes:** One of the core commitments of this project is full transparency and reproducibility. Every figure, every statistic, and every model result in this presentation can be independently verified. The data is freely available from the U.S. Sentencing Commission. The code is documented and available on GitHub. The random seed is fixed. I invite anyone who questions a finding to run the analysis themselves. That is what responsible data science looks like.
