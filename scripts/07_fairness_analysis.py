#!/usr/bin/env python3
"""
Fairness Analysis - Legal Representation and Sentencing Outcomes
Author: Barbara D. Gaskins
Date: January 2026

This script conducts a comprehensive fairness analysis of the logistic regression
model, examining disparate impact, equal opportunity, equalized odds, and other
fairness metrics across racial groups.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Machine learning and fairness packages
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    false_positive_rate,
    false_negative_rate,
    true_positive_rate,
    true_negative_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    equalized_odds_ratio
)

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'
FAIRNESS_DIR = OUTPUT_DIR / 'fairness'
FAIRNESS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("FAIRNESS ANALYSIS - LOGISTIC REGRESSION MODEL")
print("Legal Representation and Sentencing Outcomes")
print("=" * 80)
print()

# Load model-ready data
print("Loading data...")
df = pd.read_csv(DATA_DIR / 'ussc_fy2024_model_ready.csv')
print(f"✓ Loaded {len(df):,} cases")
print()

# Prepare data for modeling
print("Preparing data for fairness analysis...")

# Select features and target
X_vars = ['race_black', 'race_hispanic', 'MONSEX', 'AGE', 'atty_appointed', 
          'atty_public_def', 'atty_pro_se', 'CRIMPTS', 'XFOLSOR', 'ACCAP']
y_var = 'PRISDUM'

# Remove missing values
df_clean = df[X_vars + [y_var, 'NEWRACE']].dropna()
X = df_clean[X_vars]
y = df_clean[y_var]
sensitive_features = df_clean['NEWRACE']

print(f"✓ Clean dataset: {len(df_clean):,} cases")
print()

# Map race codes to labels
race_labels = {
    1.0: 'White',
    2.0: 'Black',
    3.0: 'Hispanic',
    6.0: 'Other'
}
sensitive_features_labeled = sensitive_features.map(race_labels)

# Split data
X_train, X_test, y_train, y_test, sf_train, sf_test = train_test_split(
    X, y, sensitive_features_labeled, test_size=0.3, random_state=42, stratify=y
)

print(f"Training set: {len(X_train):,} cases")
print(f"Test set: {len(X_test):,} cases")
print()

# Train model
print("Training logistic regression model...")
model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)
print("✓ Model trained")
print()

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Overall performance
print("=" * 80)
print("OVERALL MODEL PERFORMANCE")
print("=" * 80)
print()
print(f"Accuracy: {model.score(X_test, y_test):.4f}")
print()
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['No Prison', 'Prison']))
print()

# ============================================================================
# FAIRNESS METRICS ANALYSIS
# ============================================================================

print("=" * 80)
print("FAIRNESS METRICS BY RACE")
print("=" * 80)
print()

# 1. Selection Rate (Positive Prediction Rate)
print("1. SELECTION RATE (Predicted Prison Rate)")
print("-" * 80)
selection_rates = MetricFrame(
    metrics=selection_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(selection_rates.by_group)
print(f"\nOverall: {selection_rates.overall:.4f}")
print(f"Difference (max - min): {selection_rates.difference():.4f}")
print(f"Ratio (min / max): {selection_rates.ratio():.4f}")
print()

# 2. True Positive Rate (Sensitivity / Recall)
print("2. TRUE POSITIVE RATE (Sensitivity)")
print("-" * 80)
print("Proportion of actual prison cases correctly predicted as prison")
tpr_frame = MetricFrame(
    metrics=true_positive_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(tpr_frame.by_group)
print(f"\nOverall: {tpr_frame.overall:.4f}")
print(f"Difference (max - min): {tpr_frame.difference():.4f}")
print(f"Ratio (min / max): {tpr_frame.ratio():.4f}")
print()

# 3. False Positive Rate
print("3. FALSE POSITIVE RATE")
print("-" * 80)
print("Proportion of actual non-prison cases incorrectly predicted as prison")
fpr_frame = MetricFrame(
    metrics=false_positive_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(fpr_frame.by_group)
print(f"\nOverall: {fpr_frame.overall:.4f}")
print(f"Difference (max - min): {fpr_frame.difference():.4f}")
print(f"Ratio (min / max): {fpr_frame.ratio():.4f}")
print()

# 4. False Negative Rate
print("4. FALSE NEGATIVE RATE")
print("-" * 80)
print("Proportion of actual prison cases incorrectly predicted as non-prison")
fnr_frame = MetricFrame(
    metrics=false_negative_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(fnr_frame.by_group)
print(f"\nOverall: {fnr_frame.overall:.4f}")
print(f"Difference (max - min): {fnr_frame.difference():.4f}")
print(f"Ratio (min / max): {fnr_frame.ratio():.4f}")
print()

# 5. Demographic Parity
print("5. DEMOGRAPHIC PARITY")
print("-" * 80)
print("Measures whether selection rates are equal across groups")
dp_diff = demographic_parity_difference(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
dp_ratio = demographic_parity_ratio(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(f"Demographic Parity Difference: {dp_diff:.4f}")
print(f"Demographic Parity Ratio: {dp_ratio:.4f}")
print()
print("Interpretation:")
print("  - Difference of 0 = perfect parity")
print("  - Ratio of 1.0 = perfect parity")
print("  - Ratio < 0.8 = potential disparate impact (80% rule)")
print()

# 6. Equalized Odds
print("6. EQUALIZED ODDS")
print("-" * 80)
print("Measures whether TPR and FPR are equal across groups")
eo_diff = equalized_odds_difference(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
eo_ratio = equalized_odds_ratio(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sf_test
)
print(f"Equalized Odds Difference: {eo_diff:.4f}")
print(f"Equalized Odds Ratio: {eo_ratio:.4f}")
print()
print("Interpretation:")
print("  - Difference of 0 = perfect equalized odds")
print("  - Ratio of 1.0 = perfect equalized odds")
print()

# ============================================================================
# CONFUSION MATRICES BY RACE
# ============================================================================

print("=" * 80)
print("CONFUSION MATRICES BY RACE")
print("=" * 80)
print()

for race in sorted(sf_test.unique()):
    mask = sf_test == race
    y_test_race = y_test[mask]
    y_pred_race = y_pred[mask]
    
    print(f"\n{race}:")
    print(f"  Sample size: {mask.sum():,}")
    cm = confusion_matrix(y_test_race, y_pred_race)
    print(f"  Confusion Matrix:")
    print(f"    [[TN={cm[0,0]:4d}, FP={cm[0,1]:4d}]")
    print(f"     [FN={cm[1,0]:4d}, TP={cm[1,1]:4d}]]")
    
    # Calculate rates
    tn, fp, fn, tp = cm.ravel()
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    tnr = tn / (tn + fp) if (tn + fp) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    
    print(f"  Rates:")
    print(f"    TPR (Sensitivity): {tpr:.4f}")
    print(f"    FPR: {fpr:.4f}")
    print(f"    TNR (Specificity): {tnr:.4f}")
    print(f"    FNR: {fnr:.4f}")

print()

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("=" * 80)
print("SAVING FAIRNESS METRICS")
print("=" * 80)
print()

# Create comprehensive fairness metrics table
fairness_metrics = pd.DataFrame({
    'Race': sorted(sf_test.unique()),
    'Sample_Size': [sf_test.value_counts()[race] for race in sorted(sf_test.unique())],
    'Selection_Rate': [selection_rates.by_group[race] for race in sorted(sf_test.unique())],
    'True_Positive_Rate': [tpr_frame.by_group[race] for race in sorted(sf_test.unique())],
    'False_Positive_Rate': [fpr_frame.by_group[race] for race in sorted(sf_test.unique())],
    'False_Negative_Rate': [fnr_frame.by_group[race] for race in sorted(sf_test.unique())]
})

fairness_metrics.to_csv(FAIRNESS_DIR / 'fairness_metrics_by_race.csv', index=False)
print(f"✓ Saved: {FAIRNESS_DIR / 'fairness_metrics_by_race.csv'}")

# Save summary metrics
summary_metrics = pd.DataFrame({
    'Metric': [
        'Demographic Parity Difference',
        'Demographic Parity Ratio',
        'Equalized Odds Difference',
        'Equalized Odds Ratio',
        'Selection Rate Difference',
        'Selection Rate Ratio',
        'TPR Difference',
        'TPR Ratio',
        'FPR Difference',
        'FPR Ratio'
    ],
    'Value': [
        dp_diff,
        dp_ratio,
        eo_diff,
        eo_ratio,
        selection_rates.difference(),
        selection_rates.ratio(),
        tpr_frame.difference(),
        tpr_frame.ratio(),
        fpr_frame.difference(),
        fpr_frame.ratio()
    ]
})

summary_metrics.to_csv(FAIRNESS_DIR / 'fairness_summary_metrics.csv', index=False)
print(f"✓ Saved: {FAIRNESS_DIR / 'fairness_summary_metrics.csv'}")
print()

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)
print()

# 1. Selection Rate by Race
fig, ax = plt.subplots(figsize=(10, 6))
races = sorted(sf_test.unique())
sel_rates = [selection_rates.by_group[race] for race in races]
bars = ax.bar(races, sel_rates, color=['steelblue', 'coral', 'seagreen', 'gold'])
ax.axhline(y=selection_rates.overall, color='red', linestyle='--', linewidth=2, 
           label=f'Overall: {selection_rates.overall:.3f}')
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('Selection Rate (Predicted Prison)', fontsize=12, fontweight='bold')
ax.set_title('Selection Rate by Race\n(Proportion Predicted to Receive Prison)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'selection_rate_by_race.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: selection_rate_by_race.png")

# 2. True Positive Rate by Race
fig, ax = plt.subplots(figsize=(10, 6))
tpr_rates = [tpr_frame.by_group[race] for race in races]
bars = ax.bar(races, tpr_rates, color=['steelblue', 'coral', 'seagreen', 'gold'])
ax.axhline(y=tpr_frame.overall, color='red', linestyle='--', linewidth=2,
           label=f'Overall: {tpr_frame.overall:.3f}')
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12, fontweight='bold')
ax.set_title('True Positive Rate by Race\n(Proportion of Prison Cases Correctly Predicted)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'true_positive_rate_by_race.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: true_positive_rate_by_race.png")

# 3. False Positive Rate by Race
fig, ax = plt.subplots(figsize=(10, 6))
fpr_rates = [fpr_frame.by_group[race] for race in races]
bars = ax.bar(races, fpr_rates, color=['steelblue', 'coral', 'seagreen', 'gold'])
ax.axhline(y=fpr_frame.overall, color='red', linestyle='--', linewidth=2,
           label=f'Overall: {fpr_frame.overall:.3f}')
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('False Positive Rate', fontsize=12, fontweight='bold')
ax.set_title('False Positive Rate by Race\n(Proportion of Non-Prison Cases Incorrectly Predicted as Prison)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'false_positive_rate_by_race.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: false_positive_rate_by_race.png")

# 4. Fairness Metrics Comparison
fig, ax = plt.subplots(figsize=(12, 6))
metrics_to_plot = fairness_metrics.set_index('Race')[['Selection_Rate', 'True_Positive_Rate', 
                                                        'False_Positive_Rate', 'False_Negative_Rate']]
metrics_to_plot.plot(kind='bar', ax=ax, width=0.8)
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('Rate', fontsize=12, fontweight='bold')
ax.set_title('Fairness Metrics Comparison by Race', fontsize=14, fontweight='bold')
ax.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'fairness_metrics_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fairness_metrics_comparison.png")

print()
print("=" * 80)
print("FAIRNESS ANALYSIS COMPLETE")
print("=" * 80)
print()
print(f"All results saved to: {FAIRNESS_DIR}")
print()
print("Key Findings:")
print(f"  - Demographic Parity Ratio: {dp_ratio:.3f} {'(FAIL 80% rule)' if dp_ratio < 0.8 else '(PASS 80% rule)'}")
print(f"  - Selection Rate Range: {min(sel_rates):.3f} to {max(sel_rates):.3f}")
print(f"  - TPR Range: {min(tpr_rates):.3f} to {max(tpr_rates):.3f}")
print(f"  - FPR Range: {min(fpr_rates):.3f} to {max(fpr_rates):.3f}")
print()
print("Interpretation:")
if dp_ratio < 0.8:
    print("  ⚠ WARNING: Model exhibits disparate impact (fails 80% rule)")
    print("  The selection rate for the least favored group is less than 80% of")
    print("  the selection rate for the most favored group.")
else:
    print("  ✓ Model passes the 80% rule for disparate impact")
print()
