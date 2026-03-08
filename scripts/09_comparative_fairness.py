#!/usr/bin/env python3
"""
Comparative Fairness Analysis - All Three Models
Author: Barbara D. Gaskins
Date: January 2026

This script compares fairness metrics across:
1. Logistic Regression (baseline)
2. Multilevel Model (with district effects)
3. Mediation Analysis Model (race → attorney → prison)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    false_positive_rate,
    false_negative_rate,
    true_positive_rate,
    demographic_parity_ratio,
    equalized_odds_ratio
)

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
OUTPUT_DIR = PROJECT_DIR / 'outputs'
MODELS_DIR = OUTPUT_DIR / 'models'
FAIRNESS_DIR = OUTPUT_DIR / 'fairness'
FAIRNESS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("COMPARATIVE FAIRNESS ANALYSIS")
print("Comparing Three Models: Logistic, Multilevel, Mediation")
print("=" * 80)
print()

# Race labels
race_labels = {
    1.0: 'White',
    2.0: 'Black',
    3.0: 'Hispanic',
    6.0: 'Other'
}

# ============================================================================
# LOAD PREDICTIONS FROM ALL THREE MODELS
# ============================================================================

print("Loading model predictions...")
print()

# Model 1: Logistic Regression (from previous fairness analysis)
# We need to regenerate this from the original data
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(PROJECT_DIR / 'data' / 'ussc_fy2024_model_ready.csv')

X_vars = ['race_black', 'race_hispanic', 'MONSEX', 'AGE', 'atty_appointed', 
          'atty_public_def', 'atty_pro_se', 'CRIMPTS', 'XFOLSOR', 'ACCAP']
y_var = 'PRISDUM'

df_clean = df[X_vars + [y_var, 'NEWRACE']].dropna()
X = df_clean[X_vars]
y = df_clean[y_var]
sensitive_features = df_clean['NEWRACE'].map(race_labels)

X_train, X_test, y_train, y_test, sf_train, sf_test = train_test_split(
    X, y, sensitive_features, test_size=0.3, random_state=42, stratify=y
)

# Fit logistic regression
lr_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

print("✓ Model 1: Logistic Regression")
print(f"  Test accuracy: {lr_model.score(X_test, y_test):.4f}")
print()

# Model 2: Multilevel Model
ml_preds = pd.read_csv(MODELS_DIR / 'multilevel_predictions.csv')
y_true_ml = ml_preds['y_true']
y_pred_ml = ml_preds['y_pred']
sf_ml = ml_preds['race'].map(race_labels)

print("✓ Model 2: Multilevel Model")
print(f"  Test accuracy: {(y_true_ml == y_pred_ml).mean():.4f}")
print()

# Model 3: Mediation Analysis Model
med_preds = pd.read_csv(MODELS_DIR / 'mediation_predictions.csv')
y_true_med = med_preds['y_true']
y_pred_med = med_preds['y_pred']
sf_med = med_preds['race'].map(race_labels)

print("✓ Model 3: Mediation Analysis Model")
print(f"  Test accuracy: {(y_true_med == y_pred_med).mean():.4f}")
print()

# ============================================================================
# CALCULATE FAIRNESS METRICS FOR EACH MODEL
# ============================================================================

def calculate_fairness_metrics(y_true, y_pred, sensitive_features, model_name):
    """Calculate comprehensive fairness metrics for a model."""
    
    print(f"Calculating fairness metrics for {model_name}...")
    
    # Selection Rate
    sel_rate = MetricFrame(
        metrics=selection_rate,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # True Positive Rate
    tpr = MetricFrame(
        metrics=true_positive_rate,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # False Positive Rate
    fpr = MetricFrame(
        metrics=false_positive_rate,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # False Negative Rate
    fnr = MetricFrame(
        metrics=false_negative_rate,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # Demographic Parity Ratio
    dp_ratio = demographic_parity_ratio(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # Equalized Odds Ratio
    eo_ratio = equalized_odds_ratio(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # Compile results
    results = {
        'model': model_name,
        'demographic_parity_ratio': dp_ratio,
        'equalized_odds_ratio': eo_ratio,
        'selection_rate_diff': sel_rate.difference(),
        'tpr_diff': tpr.difference(),
        'fpr_diff': fpr.difference(),
        'fnr_diff': fnr.difference(),
        'selection_rate_ratio': sel_rate.ratio(),
        'tpr_ratio': tpr.ratio(),
        'fpr_ratio': fpr.ratio(),
        'fnr_ratio': fnr.ratio()
    }
    
    # By-group metrics
    by_group = pd.DataFrame({
        'Race': sorted(sensitive_features.unique()),
        'Selection_Rate': [sel_rate.by_group[race] for race in sorted(sensitive_features.unique())],
        'TPR': [tpr.by_group[race] for race in sorted(sensitive_features.unique())],
        'FPR': [fpr.by_group[race] for race in sorted(sensitive_features.unique())],
        'FNR': [fnr.by_group[race] for race in sorted(sensitive_features.unique())]
    })
    by_group['Model'] = model_name
    
    print(f"  ✓ Demographic Parity Ratio: {dp_ratio:.4f}")
    print(f"  ✓ Equalized Odds Ratio: {eo_ratio:.4f}")
    print()
    
    return results, by_group

# Calculate metrics for all models
print("=" * 80)
print("FAIRNESS METRICS CALCULATION")
print("=" * 80)
print()

results_lr, bygroup_lr = calculate_fairness_metrics(y_test, y_pred_lr, sf_test, "Logistic Regression")
results_ml, bygroup_ml = calculate_fairness_metrics(y_true_ml, y_pred_ml, sf_ml, "Multilevel Model")
results_med, bygroup_med = calculate_fairness_metrics(y_true_med, y_pred_med, sf_med, "Mediation Model")

# ============================================================================
# COMPARATIVE ANALYSIS
# ============================================================================

print("=" * 80)
print("COMPARATIVE FAIRNESS SUMMARY")
print("=" * 80)
print()

# Create comparison table
comparison_df = pd.DataFrame([results_lr, results_ml, results_med])
comparison_df = comparison_df.set_index('model')

print("Key Fairness Metrics Comparison:")
print("-" * 80)
print(comparison_df[['demographic_parity_ratio', 'equalized_odds_ratio', 
                     'selection_rate_diff', 'tpr_diff', 'fpr_diff']].to_string())
print()

# Save comparison table
comparison_df.to_csv(FAIRNESS_DIR / 'model_fairness_comparison.csv')
print(f"✓ Saved: model_fairness_comparison.csv")
print()

# Determine least biased model
print("Ranking Models by Fairness:")
print("-" * 80)

# Higher ratio = more fair (closer to 1.0)
# Lower difference = more fair (closer to 0)

# Calculate composite fairness score
# We want high ratios and low differences
comparison_df['fairness_score'] = (
    comparison_df['demographic_parity_ratio'] + 
    comparison_df['equalized_odds_ratio'] - 
    comparison_df['selection_rate_diff'] - 
    comparison_df['tpr_diff'] - 
    comparison_df['fpr_diff']
)

ranked = comparison_df.sort_values('fairness_score', ascending=False)
print(ranked[['demographic_parity_ratio', 'equalized_odds_ratio', 'fairness_score']].to_string())
print()

best_model = ranked.index[0]
print(f"🏆 LEAST BIASED MODEL: {best_model}")
print()

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("=" * 80)
print("CREATING COMPARATIVE VISUALIZATIONS")
print("=" * 80)
print()

# 1. Demographic Parity Ratio Comparison
fig, ax = plt.subplots(figsize=(10, 6))
models = comparison_df.index
dp_ratios = comparison_df['demographic_parity_ratio']
colors = ['steelblue', 'coral', 'seagreen']
bars = ax.bar(models, dp_ratios, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add 80% threshold line
ax.axhline(y=0.8, color='red', linestyle='--', linewidth=2, label='80% Rule Threshold')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Demographic Parity Ratio', fontsize=12, fontweight='bold')
ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_title('Demographic Parity Ratio Comparison\n(Higher = More Fair, >0.8 Passes 80% Rule)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'comparison_demographic_parity.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: comparison_demographic_parity.png")

# 2. Equalized Odds Ratio Comparison
fig, ax = plt.subplots(figsize=(10, 6))
eo_ratios = comparison_df['equalized_odds_ratio']
bars = ax.bar(models, eo_ratios, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Equalized Odds Ratio', fontsize=12, fontweight='bold')
ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_title('Equalized Odds Ratio Comparison\n(Higher = More Fair, 1.0 = Perfect Equality)', 
             fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'comparison_equalized_odds.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: comparison_equalized_odds.png")

# 3. Selection Rate by Race for All Models
bygroup_all = pd.concat([bygroup_lr, bygroup_ml, bygroup_med])

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(bygroup_lr['Race']))
width = 0.25

bars1 = ax.bar(x - width, bygroup_lr['Selection_Rate'], width, label='Logistic Regression', 
               color='steelblue', alpha=0.7)
bars2 = ax.bar(x, bygroup_ml['Selection_Rate'], width, label='Multilevel Model', 
               color='coral', alpha=0.7)
bars3 = ax.bar(x + width, bygroup_med['Selection_Rate'], width, label='Mediation Model', 
               color='seagreen', alpha=0.7)

ax.set_ylabel('Selection Rate (Predicted Prison)', fontsize=12, fontweight='bold')
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_title('Selection Rate by Race - Model Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(bygroup_lr['Race'])
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'comparison_selection_rate_by_race.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: comparison_selection_rate_by_race.png")

# 4. Comprehensive Fairness Metrics Heatmap
metrics_matrix = comparison_df[['demographic_parity_ratio', 'equalized_odds_ratio', 
                                 'selection_rate_ratio', 'tpr_ratio', 'fpr_ratio']].T

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(metrics_matrix, annot=True, fmt='.3f', cmap='RdYlGn', center=0.8, 
            vmin=0.3, vmax=1.0, cbar_kws={'label': 'Fairness Score'}, ax=ax)
ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_ylabel('Fairness Metric', fontsize=12, fontweight='bold')
ax.set_title('Comprehensive Fairness Metrics Heatmap\n(Green = More Fair)', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FAIRNESS_DIR / 'comparison_fairness_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: comparison_fairness_heatmap.png")

print()
print("=" * 80)
print("COMPARATIVE FAIRNESS ANALYSIS COMPLETE")
print("=" * 80)
print()
print(f"🏆 LEAST BIASED MODEL: {best_model}")
print()
print("Key Findings:")
print(f"  - {best_model} has the highest fairness score")
print(f"  - Demographic Parity Ratio: {comparison_df.loc[best_model, 'demographic_parity_ratio']:.3f}")
print(f"  - Equalized Odds Ratio: {comparison_df.loc[best_model, 'equalized_odds_ratio']:.3f}")
print()
print("All results saved to:", FAIRNESS_DIR)
print()
