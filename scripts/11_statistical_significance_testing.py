#!/usr/bin/env python3
"""
Statistical Significance Testing for Fairness Metric Differences
Author: Barbara D. Gaskins
Date: January 2026

This script conducts statistical tests to determine whether the fairness
improvements in the Multilevel Model compared to the Logistic Regression
model are statistically significant.

Tests performed:
1. Bootstrap confidence intervals for fairness metrics
2. Permutation tests for difference in metrics
3. McNemar's test for prediction disagreement
4. Effect size calculations (Cohen's h)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Set random seed
np.random.seed(42)

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
OUTPUT_DIR = PROJECT_DIR / 'outputs'
MODELS_DIR = OUTPUT_DIR / 'models'
STATS_DIR = OUTPUT_DIR / 'statistical_tests'
STATS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("STATISTICAL SIGNIFICANCE TESTING")
print("Comparing Logistic Regression vs. Multilevel Model")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================

print("Loading model predictions...")

# Load fairness comparison results
comparison_df = pd.read_csv(OUTPUT_DIR / 'fairness' / 'model_fairness_comparison.csv')
print("✓ Loaded fairness comparison data")

# Load predictions from both models
# We need to regenerate these with the same test set
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(PROJECT_DIR / 'data' / 'ussc_fy2024_model_ready.csv')

# Prepare data
X_vars = ['race_black', 'race_hispanic', 'MONSEX', 'AGE', 'atty_appointed', 
          'atty_public_def', 'atty_pro_se', 'CRIMPTS', 'XFOLSOR', 'ACCAP']
y_var = 'PRISDUM'

RACE_LABELS = {1.0: 'White', 2.0: 'Black', 3.0: 'Hispanic', 6.0: 'Other'}

df_clean = df[X_vars + [y_var, 'NEWRACE', 'DISTRICT']].dropna()
X = df_clean[X_vars]
y = df_clean[y_var]
race = df_clean['NEWRACE'].map(RACE_LABELS)
district = df_clean['DISTRICT']

X_train, X_test, y_train, y_test, race_train, race_test, dist_train, dist_test = train_test_split(
    X, y, race, district, test_size=0.3, random_state=42, stratify=y
)

print("✓ Loaded and split data")
print(f"  Test set size: {len(X_test):,}")
print()

# Train both models
print("Training models...")

# Model 1: Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
print("✓ Logistic Regression trained")

# Model 2: Multilevel Model (with district dummies)
df_train_ml = pd.concat([X_train.reset_index(drop=True), 
                         dist_train.reset_index(drop=True)], axis=1)
df_test_ml = pd.concat([X_test.reset_index(drop=True), 
                        dist_test.reset_index(drop=True)], axis=1)

df_train_ml = pd.get_dummies(df_train_ml, columns=['DISTRICT'], drop_first=True, dtype=float)
df_test_ml = pd.get_dummies(df_test_ml, columns=['DISTRICT'], drop_first=True, dtype=float)

# Align columns
train_cols = df_train_ml.columns
test_cols = df_test_ml.columns
missing_in_test = set(train_cols) - set(test_cols)
missing_in_train = set(test_cols) - set(train_cols)

for col in missing_in_test:
    df_test_ml[col] = 0
for col in missing_in_train:
    df_train_ml[col] = 0

df_test_ml = df_test_ml[df_train_ml.columns]

ml_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
ml_model.fit(df_train_ml, y_train)
y_pred_ml = ml_model.predict(df_test_ml)
print("✓ Multilevel Model trained")
print()

# ============================================================================
# BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================================

print("=" * 80)
print("BOOTSTRAP CONFIDENCE INTERVALS")
print("=" * 80)
print()

def bootstrap_metric(y_true, y_pred, sensitive_features, metric_func, n_bootstrap=1000):
    """Calculate bootstrap confidence interval for a metric."""
    n = len(y_true)
    bootstrap_values = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(n, n, replace=True)
        y_true_boot = y_true.iloc[indices]
        y_pred_boot = y_pred[indices]
        sf_boot = sensitive_features.iloc[indices]
        
        # Calculate metric
        try:
            value = metric_func(y_true_boot, y_pred_boot, sf_boot)
            bootstrap_values.append(value)
        except:
            continue
    
    # Calculate confidence interval
    ci_lower = np.percentile(bootstrap_values, 2.5)
    ci_upper = np.percentile(bootstrap_values, 97.5)
    mean_value = np.mean(bootstrap_values)
    
    return mean_value, ci_lower, ci_upper, bootstrap_values

def selection_rate_diff(y_true, y_pred, sensitive_features):
    """Calculate selection rate difference across groups."""
    rates = {}
    for group in sensitive_features.unique():
        mask = sensitive_features == group
        rates[group] = y_pred[mask].mean()
    return max(rates.values()) - min(rates.values())

print("Calculating bootstrap confidence intervals (1000 iterations)...")
print("(This may take a few minutes...)")
print()

# Bootstrap for Logistic Regression
print("Logistic Regression:")
lr_mean, lr_lower, lr_upper, lr_boots = bootstrap_metric(
    y_test, y_pred_lr, race_test, selection_rate_diff, n_bootstrap=1000
)
print(f"  Selection Rate Difference: {lr_mean:.4f} [95% CI: {lr_lower:.4f}, {lr_upper:.4f}]")

# Bootstrap for Multilevel Model
print("Multilevel Model:")
ml_mean, ml_lower, ml_upper, ml_boots = bootstrap_metric(
    y_test, y_pred_ml, race_test, selection_rate_diff, n_bootstrap=1000
)
print(f"  Selection Rate Difference: {ml_mean:.4f} [95% CI: {ml_lower:.4f}, {ml_upper:.4f}]")
print()

# Check if confidence intervals overlap
overlap = not (ml_upper < lr_lower or lr_upper < ml_lower)
print(f"Confidence intervals overlap: {overlap}")
if not overlap:
    print("✓ The difference between models is statistically significant (p < 0.05)")
else:
    print("⚠ The difference may not be statistically significant")
print()

# ============================================================================
# PERMUTATION TEST
# ============================================================================

print("=" * 80)
print("PERMUTATION TEST")
print("=" * 80)
print()

print("Testing null hypothesis: No difference in fairness between models")
print("(Running 1000 permutations...)")
print()

# Observed difference
observed_diff = lr_mean - ml_mean

# Permutation test
n_permutations = 1000
permutation_diffs = []

for _ in range(n_permutations):
    # Randomly swap predictions between models
    swap_mask = np.random.rand(len(y_pred_lr)) < 0.5
    y_pred_perm1 = np.where(swap_mask, y_pred_lr, y_pred_ml)
    y_pred_perm2 = np.where(swap_mask, y_pred_ml, y_pred_lr)
    
    # Calculate metrics for permuted predictions
    try:
        diff1 = selection_rate_diff(y_test, y_pred_perm1, race_test)
        diff2 = selection_rate_diff(y_test, y_pred_perm2, race_test)
        permutation_diffs.append(diff1 - diff2)
    except:
        continue

# Calculate p-value
p_value = np.mean(np.abs(permutation_diffs) >= np.abs(observed_diff))

print(f"Observed difference: {observed_diff:.4f}")
print(f"P-value: {p_value:.4f}")
print()

if p_value < 0.05:
    print("✓ Result is statistically significant (p < 0.05)")
    print("  We reject the null hypothesis: The Multilevel Model has significantly")
    print("  better fairness metrics than the Logistic Regression model.")
else:
    print("⚠ Result is not statistically significant (p >= 0.05)")
    print("  We cannot reject the null hypothesis.")
print()

# ============================================================================
# MCNEMAR'S TEST
# ============================================================================

print("=" * 80)
print("MCNEMAR'S TEST")
print("=" * 80)
print()

print("Testing whether the models make significantly different predictions...")
print()

# Create contingency table
both_correct = np.sum((y_pred_lr == y_test) & (y_pred_ml == y_test))
lr_correct_ml_wrong = np.sum((y_pred_lr == y_test) & (y_pred_ml != y_test))
ml_correct_lr_wrong = np.sum((y_pred_ml == y_test) & (y_pred_lr != y_test))
both_wrong = np.sum((y_pred_lr != y_test) & (y_pred_ml != y_test))

print("Contingency Table:")
print(f"  Both correct: {both_correct:,}")
print(f"  LR correct, ML wrong: {lr_correct_ml_wrong:,}")
print(f"  ML correct, LR wrong: {ml_correct_lr_wrong:,}")
print(f"  Both wrong: {both_wrong:,}")
print()

# McNemar's test
if lr_correct_ml_wrong + ml_correct_lr_wrong > 0:
    mcnemar_stat = (abs(lr_correct_ml_wrong - ml_correct_lr_wrong) - 1)**2 / (lr_correct_ml_wrong + ml_correct_lr_wrong)
    mcnemar_p = 1 - stats.chi2.cdf(mcnemar_stat, 1)
    
    print(f"McNemar's statistic: {mcnemar_stat:.4f}")
    print(f"P-value: {mcnemar_p:.4f}")
    print()
    
    if mcnemar_p < 0.05:
        print("✓ Models make significantly different predictions (p < 0.05)")
    else:
        print("⚠ Models do not make significantly different predictions (p >= 0.05)")
else:
    print("⚠ Cannot perform McNemar's test (no discordant pairs)")

print()

# ============================================================================
# EFFECT SIZE (COHEN'S H)
# ============================================================================

print("=" * 80)
print("EFFECT SIZE CALCULATION")
print("=" * 80)
print()

print("Calculating Cohen's h for effect size...")
print()

def cohens_h(p1, p2):
    """Calculate Cohen's h effect size for proportions."""
    phi1 = 2 * np.arcsin(np.sqrt(p1))
    phi2 = 2 * np.arcsin(np.sqrt(p2))
    return phi1 - phi2

# Calculate selection rates for each model
lr_selection_rate = y_pred_lr.mean()
ml_selection_rate = y_pred_ml.mean()

h = cohens_h(lr_selection_rate, ml_selection_rate)

print(f"Logistic Regression selection rate: {lr_selection_rate:.4f}")
print(f"Multilevel Model selection rate: {ml_selection_rate:.4f}")
print(f"Cohen's h: {h:.4f}")
print()

# Interpret effect size
if abs(h) < 0.2:
    interpretation = "small"
elif abs(h) < 0.5:
    interpretation = "medium"
else:
    interpretation = "large"

print(f"Effect size interpretation: {interpretation}")
print()

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("=" * 80)
print("SAVING RESULTS")
print("=" * 80)
print()

# Save bootstrap results
bootstrap_results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Multilevel Model'],
    'Mean_Selection_Rate_Diff': [lr_mean, ml_mean],
    'CI_Lower': [lr_lower, ml_lower],
    'CI_Upper': [lr_upper, ml_upper]
})
bootstrap_results.to_csv(STATS_DIR / 'bootstrap_results.csv', index=False)
print("✓ Saved: bootstrap_results.csv")

# Save permutation test results
permutation_results = pd.DataFrame({
    'Test': ['Permutation Test'],
    'Observed_Difference': [observed_diff],
    'P_Value': [p_value],
    'Significant': [p_value < 0.05]
})
permutation_results.to_csv(STATS_DIR / 'permutation_test_results.csv', index=False)
print("✓ Saved: permutation_test_results.csv")

# Save McNemar's test results
if lr_correct_ml_wrong + ml_correct_lr_wrong > 0:
    mcnemar_results = pd.DataFrame({
        'Test': ['McNemar Test'],
        'Statistic': [mcnemar_stat],
        'P_Value': [mcnemar_p],
        'Significant': [mcnemar_p < 0.05]
    })
    mcnemar_results.to_csv(STATS_DIR / 'mcnemar_test_results.csv', index=False)
    print("✓ Saved: mcnemar_test_results.csv")

# Save effect size results
effect_size_results = pd.DataFrame({
    'Metric': ['Cohen\'s h'],
    'Value': [h],
    'Interpretation': [interpretation]
})
effect_size_results.to_csv(STATS_DIR / 'effect_size_results.csv', index=False)
print("✓ Saved: effect_size_results.csv")

print()

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)
print()

# 1. Bootstrap distributions
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(lr_boots, bins=30, alpha=0.5, label='Logistic Regression', color='steelblue', edgecolor='black')
ax.hist(ml_boots, bins=30, alpha=0.5, label='Multilevel Model', color='coral', edgecolor='black')
ax.axvline(lr_mean, color='steelblue', linestyle='--', linewidth=2)
ax.axvline(ml_mean, color='coral', linestyle='--', linewidth=2)
ax.set_xlabel('Selection Rate Difference', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax.set_title('Bootstrap Distribution of Selection Rate Difference\n(1000 iterations)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(STATS_DIR / 'bootstrap_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: bootstrap_distributions.png")

# 2. Confidence intervals comparison
fig, ax = plt.subplots(figsize=(10, 6))
models = ['Logistic\nRegression', 'Multilevel\nModel']
means = [lr_mean, ml_mean]
errors = [[lr_mean - lr_lower, ml_mean - ml_lower], 
          [lr_upper - lr_mean, ml_upper - ml_mean]]

ax.errorbar(models, means, yerr=errors, fmt='o', markersize=10, capsize=10, 
            capthick=2, linewidth=2, color='black')
ax.scatter(models, means, s=200, c=['steelblue', 'coral'], zorder=3, edgecolor='black', linewidth=2)

for i, (model, mean, lower, upper) in enumerate(zip(models, means, [lr_lower, ml_lower], [lr_upper, ml_upper])):
    ax.text(i, mean + 0.01, f'{mean:.3f}\n[{lower:.3f}, {upper:.3f}]', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Selection Rate Difference', fontsize=12, fontweight='bold')
ax.set_title('95% Confidence Intervals for Selection Rate Difference', 
             fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(STATS_DIR / 'confidence_intervals.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: confidence_intervals.png")

print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("STATISTICAL TESTING COMPLETE")
print("=" * 80)
print()

print("Summary of Findings:")
print("-" * 80)
print(f"1. Bootstrap Analysis:")
print(f"   - LR Selection Rate Diff: {lr_mean:.4f} [{lr_lower:.4f}, {lr_upper:.4f}]")
print(f"   - ML Selection Rate Diff: {ml_mean:.4f} [{ml_lower:.4f}, {ml_upper:.4f}]")
print(f"   - Improvement: {(lr_mean - ml_mean):.4f} ({(lr_mean - ml_mean)/lr_mean*100:.1f}% reduction)")
print()

print(f"2. Permutation Test:")
print(f"   - P-value: {p_value:.4f}")
print(f"   - Result: {'Significant' if p_value < 0.05 else 'Not significant'}")
print()

if lr_correct_ml_wrong + ml_correct_lr_wrong > 0:
    print(f"3. McNemar's Test:")
    print(f"   - P-value: {mcnemar_p:.4f}")
    print(f"   - Result: {'Significant' if mcnemar_p < 0.05 else 'Not significant'}")
    print()

print(f"4. Effect Size:")
print(f"   - Cohen's h: {h:.4f}")
print(f"   - Interpretation: {interpretation.capitalize()} effect")
print()

print("All results saved to:", STATS_DIR)
print()
