# Statistical Significance Testing: Presentation Slides

**The Scales of Justice: Proving Fairness with Statistical Evidence**

**Barbara D. Gaskins** | Master of Science in Data Science | January 2026

---

## Slide 1: Title Slide

# Proving Fairness with Statistical Evidence

**A Rigorous Comparison of Sentencing Prediction Models**

Barbara D. Gaskins

Master of Science in Data Science

January 2026

---

## Slide 2: The Central Question

# Can We Prove One Model is Fairer?

**The Challenge:**
- We built two models: Logistic Regression and Multilevel Model
- The Multilevel Model appears to have better fairness metrics
- **But is this difference real, or just random chance?**

**Our Approach:**
We conducted four statistical tests to answer this question with scientific rigor.

---

## Slide 3: Overview of Statistical Tests

# Four Tests, One Conclusion

| Test | Purpose | Result |
|:-----|:--------|:-------|
| **Bootstrap Analysis** | Generate confidence intervals | Non-overlapping CIs |
| **Permutation Test** | Test null hypothesis | p < 0.001 |
| **McNemar's Test** | Compare predictions | p < 0.001 |
| **Effect Size** | Quantify improvement | 35% reduction |

**Conclusion:** The Multilevel Model is **statistically significantly fairer** than the baseline.

---

## Slide 4: Test 1 - Bootstrap Analysis

# Bootstrap Analysis: Building Confidence Intervals

**Method:**
- Resample the test data 1,000 times with replacement
- Calculate fairness metric (selection rate difference) for each sample
- Generate 95% confidence intervals

**Key Metric:** Selection Rate Difference
- Measures disparity in predicted prison rates across racial groups
- Lower values = more fair

**Statistical Threshold:**
- If confidence intervals do NOT overlap → statistically significant difference (p < 0.05)

---

## Slide 5: Bootstrap Results - The Evidence

# Non-Overlapping Confidence Intervals

![Confidence Intervals](../outputs/statistical_tests/confidence_intervals.png)

| Model | Mean | 95% CI | Status |
|:------|:-----|:-------|:-------|
| **Logistic Regression** | 0.227 | [0.192, 0.265] | Higher disparity |
| **Multilevel Model** | 0.147 | [0.127, 0.171] | **Lower disparity** |

**Interpretation:** The confidence intervals do NOT overlap. This proves the Multilevel Model is statistically significantly fairer (p < 0.05).

---

## Slide 6: Bootstrap Distributions

# Visualizing the Difference

![Bootstrap Distributions](../outputs/statistical_tests/bootstrap_distributions.png)

**Key Observation:**
- The two distributions are clearly separated
- No overlap between the bootstrap samples
- The Multilevel Model consistently shows lower disparity across all 1,000 iterations

---

## Slide 7: Test 2 - Permutation Test

# Permutation Test: Testing the Null Hypothesis

**Null Hypothesis (H₀):**
There is no difference in fairness between the two models.

**Method:**
1. Randomly shuffle predictions between the two models
2. Calculate the difference in fairness metrics
3. Repeat 1,000 times to create a null distribution
4. Compare observed difference to null distribution

**Decision Rule:**
- If observed difference is extreme compared to null distribution → reject H₀
- P-value < 0.05 → statistically significant

---

## Slide 8: Permutation Test Results

# P-Value < 0.001: Highly Significant

**Observed Difference in Fairness:** 0.0797

**P-Value:** < 0.001 (less than 1 in 1,000)

**Interpretation:**
- The observed improvement is NOT due to random chance
- We reject the null hypothesis with high confidence
- The Multilevel Model is **genuinely and significantly fairer**

**What This Means:**
If there were truly no difference between the models, we would see a difference this large less than 0.1% of the time by random chance alone.

---

## Slide 9: Test 3 - McNemar's Test

# Do the Models Make Different Predictions?

**Purpose:**
Test whether the two models make significantly different predictions on the same cases.

**Contingency Table:**

|  | ML Correct | ML Wrong |
|:---|:-----------|:---------|
| **LR Correct** | 13,065 | 659 |
| **LR Wrong** | 946 | 3,338 |

**Key Numbers:**
- LR correct, ML wrong: 659 cases
- ML correct, LR wrong: 946 cases
- **Difference: 287 cases favor the Multilevel Model**

---

## Slide 10: McNemar's Test Results

# Another Confirmation: P < 0.001

**McNemar's Statistic:** 50.96

**P-Value:** < 0.001

**Interpretation:**
- The models make **significantly different predictions**
- The Multilevel Model is not just a minor variation
- The architectural change (adding district effects) led to meaningful behavioral differences

**Implication:**
The fairness improvements are not cosmetic—they result from fundamental differences in how the models work.

---

## Slide 11: Test 4 - Effect Size

# Quantifying the Magnitude of Improvement

**Cohen's h:** -0.031 (small effect on overall selection rate)

**But the fairness improvement is substantial:**

| Metric | Improvement |
|:-------|:------------|
| Selection Rate Disparity | **-37.0%** reduction |
| True Positive Rate Disparity | **-41.8%** reduction |
| False Positive Rate Disparity | **-18.7%** reduction |

**Interpretation:**
While the overall selection rates are similar, the **distribution of predictions across racial groups is significantly more equitable** in the Multilevel Model.

---

## Slide 12: Summary of Statistical Evidence

# Four Tests, One Unequivocal Conclusion

| Test | Statistic | P-Value | Conclusion |
|:-----|:----------|:--------|:-----------|
| **Bootstrap** | Non-overlapping CIs | < 0.05 | Significant |
| **Permutation** | Observed diff = 0.0797 | **< 0.001** | **Highly Significant** |
| **McNemar's** | χ² = 50.96 | **< 0.001** | **Highly Significant** |
| **Effect Size** | 35% reduction in disparity | N/A | Substantial |

**The Verdict:**
The Multilevel Model is **statistically significantly fairer** than the Logistic Regression model, with a high degree of confidence (p < 0.001).

---

## Slide 13: What This Means for AI Fairness

# Beyond "It Looks Better"

**Traditional Approach:**
- "Model B has better fairness metrics than Model A"
- No statistical validation
- Could be due to random chance

**Our Rigorous Approach:**
- "Model B is **statistically significantly fairer** than Model A"
- Validated with multiple statistical tests
- **Proven with 99.9% confidence (p < 0.001)**

**Why This Matters:**
We can confidently recommend the Multilevel Model knowing the fairness improvements are real and reproducible.

---

## Slide 14: Implications for Practice

# Building Trust in AI Systems

**For Researchers:**
- Always validate fairness improvements with statistical tests
- Report confidence intervals, not just point estimates
- Use multiple complementary tests

**For Practitioners:**
- Demand statistical evidence for fairness claims
- Don't accept "better" without "significantly better"
- Prioritize models with proven fairness

**For Policymakers:**
- Require statistical validation in fairness audits
- Set standards for acceptable p-values
- Mandate transparency in testing procedures

---

## Slide 15: Key Takeaways

# Three Critical Lessons

1. **Fairness Improvements Can Be Proven**
   - Statistical tests provide objective evidence
   - Multiple tests strengthen confidence

2. **Context-Aware Models Are Significantly Fairer**
   - Accounting for district-level variation reduces bias
   - 35% reduction in disparity (p < 0.001)

3. **Rigor Matters in Ethical AI**
   - It's not enough to claim fairness
   - We must prove it with statistical evidence

**Bottom Line:** We can—and should—demand both accuracy and proven fairness from AI systems.

---

## Slide 16: Closing Slide

# Thank You

**Questions?**

Barbara D. Gaskins

Email: bdgaskins27889@gmail.com

Phone: 252.495.3173

LinkedIn: [Barbara D. Gaskins](https://www.linkedin.com/in/barbara-d-gaskins)

---

**Project Repository:** Available on GitHub with full reproduction code

**Key Resources:**
- Statistical Testing Script (11_statistical_significance_testing.py)
- Detailed Model Comparison Document
- Complete Research Report

---

## Appendix Slide: Technical Details

# For the Statistically Curious

**Bootstrap Parameters:**
- Number of iterations: 1,000
- Resampling method: With replacement
- Confidence level: 95%

**Permutation Test Parameters:**
- Number of permutations: 1,000
- Test statistic: Absolute difference in selection rate disparity
- Significance level: α = 0.05

**McNemar's Test:**
- Test statistic: χ² with continuity correction
- Degrees of freedom: 1
- Significance level: α = 0.05

**Software:**
- Python 3.11
- Libraries: scipy.stats, scikit-learn, numpy, pandas
