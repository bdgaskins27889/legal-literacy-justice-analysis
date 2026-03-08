# Policy Brief: Building Fairer Sentencing Models

**To**: Policymakers, Judicial Administrators, and Criminal Justice Reform Advocates

**From**: Barbara D. Gaskins, Data Scientist

**Date**: January 25, 2026

**Subject**: Mitigating Algorithmic Bias in Predictive Sentencing Models

---

## The Challenge: Hidden Bias in AI

As artificial intelligence (AI) is increasingly used in the criminal justice system, there is a risk that these tools can perpetuate and even amplify existing societal biases. Our analysis of over 60,000 federal sentencing cases demonstrates that a standard predictive model, while seemingly accurate, can be significantly unfair, disproportionately flagging minority defendants for prison sentences.

**A standard model failed to be fair, with a racial disparity 29% worse than the legal threshold for disparate impact.**

## The Solution: A More Context-Aware Approach

Our research shows that a more sophisticated **Multilevel Model**—one that accounts for the systemic differences between judicial districts—is **statistically significantly fairer**. This model passes the legal threshold for fairness and reduces racial disparities in prediction errors by up to 42%.

| Metric | Standard Model | **Fairer Model** | Improvement |
| :--- | :--- | :--- | :--- |
| **Disparate Impact** | Fails 80% Rule | **Passes 80% Rule** | **15.6% Fairer** |
| **Error Disparity** | High | **Low** | **41.8% Reduction** |

## Key Policy Recommendations

1.  **Mandate Fairness Audits for All Predictive Models**: Before any predictive model is deployed in the justice system, it must undergo a rigorous fairness audit that goes beyond simple accuracy. This audit should, at a minimum, test for disparate impact across racial, ethnic, and gender groups.

2.  **Require Context-Aware Models**: Simple, one-size-fits-all models are not sufficient. Policymakers should require the use of models that account for local context, such as the variations between judicial districts, to ensure that predictions are not simply reflecting systemic biases.

3.  **Prioritize Transparency and Reproducibility**: The code and data used to train these models must be open to inspection by independent researchers and the public. Our project includes a fully reproducible script to demonstrate this can be done.

## The Bottom Line

It is not enough for a predictive model to be accurate. It must also be fair. Our research proves that it is possible to build models that are both. By mandating a more sophisticated and context-aware approach to predictive modeling, we can harness the power of AI to create a more just and equitable legal system, rather than one that automates and amplifies existing biases.

**The choice is not between accuracy and fairness. We can and should demand both.**
