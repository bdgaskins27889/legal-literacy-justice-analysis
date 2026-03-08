#!/usr/bin/env python3
"""
Reproducible Multilevel Model Fairness Analysis
Author: Barbara D. Gaskins
Date: January 2026

This script provides a complete, standalone reproduction of the Multilevel Model's
fairness metrics, including all data loading, preprocessing, model training, and
fairness evaluation steps.

USAGE:
    python3 10_reproduce_multilevel_fairness.py

REQUIREMENTS:
    - pandas
    - numpy
    - scikit-learn
    - fairlearn
    - matplotlib
    - seaborn

OUTPUT:
    - Trained multilevel model
    - Fairness metrics by racial group
    - Visualizations comparing fairness metrics
    - Detailed log of all steps
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Machine learning packages
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Fairness evaluation packages
from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    false_positive_rate,
    false_negative_rate,
    true_positive_rate,
    demographic_parity_ratio,
    equalized_odds_ratio
)

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# ============================================================================
# CONFIGURATION
# ============================================================================

print("=" * 80)
print("MULTILEVEL MODEL FAIRNESS ANALYSIS - COMPLETE REPRODUCTION")
print("=" * 80)
print()

# Define paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'
REPRODUCTION_DIR = OUTPUT_DIR / 'reproduction'
REPRODUCTION_DIR.mkdir(exist_ok=True)

# Race labels mapping
RACE_LABELS = {
    1.0: 'White',
    2.0: 'Black',
    3.0: 'Hispanic',
    6.0: 'Other'
}

print("Configuration:")
print(f"  Project Directory: {PROJECT_DIR}")
print(f"  Data Directory: {DATA_DIR}")
print(f"  Output Directory: {REPRODUCTION_DIR}")
print(f"  Random Seed: {RANDOM_SEED}")
print()

# ============================================================================
# STEP 1: DATA LOADING
# ============================================================================

print("=" * 80)
print("STEP 1: DATA LOADING")
print("=" * 80)
print()

print("Loading USSC FY 2024 dataset...")
df_raw = pd.read_csv(DATA_DIR / 'ussc_fy2024_model_ready.csv')
print(f"✓ Loaded {len(df_raw):,} cases")
print(f"✓ Number of variables: {len(df_raw.columns)}")
print()

print("Dataset preview:")
print(df_raw.head())
print()

print("Dataset info:")
print(f"  Shape: {df_raw.shape}")
print(f"  Memory usage: {df_raw.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print()

# ============================================================================
# STEP 2: VARIABLE SELECTION
# ============================================================================

print("=" * 80)
print("STEP 2: VARIABLE SELECTION")
print("=" * 80)
print()

print("Selecting variables for multilevel model...")

# Define required variables
required_vars = [
    # Demographic variables
    'NEWRACE',           # Race (1=White, 2=Black, 3=Hispanic, 6=Other)
    'race_black',        # Binary: Black race
    'race_hispanic',     # Binary: Hispanic race
    'MONSEX',            # Gender (0=Male, 1=Female)
    'AGE',               # Age in years
    
    # Attorney type variables
    'TYPEMONY',          # Attorney type (1=Private, 2=Appointed, 3=Public Defender, 4=Pro Se)
    'atty_appointed',    # Binary: Appointed attorney
    'atty_public_def',   # Binary: Public defender
    'atty_pro_se',       # Binary: Pro se (self-representation)
    
    # Criminal history variables
    'CRIMPTS',           # Criminal history points
    'XFOLSOR',           # Prior convictions
    
    # Case characteristics
    'ACCAP',             # Acceptance of responsibility
    'DISTRICT',          # Judicial district (for multilevel clustering)
    
    # Outcome variable
    'PRISDUM'            # Prison sentence (0=No, 1=Yes)
]

print(f"Required variables ({len(required_vars)}):")
for var in required_vars:
    print(f"  - {var}")
print()

# Check for missing variables
missing_vars = [var for var in required_vars if var not in df_raw.columns]
if missing_vars:
    print(f"⚠ WARNING: Missing variables: {missing_vars}")
    print("These will be handled in preprocessing.")
    print()

# ============================================================================
# STEP 3: DATA PREPROCESSING
# ============================================================================

print("=" * 80)
print("STEP 3: DATA PREPROCESSING")
print("=" * 80)
print()

print("Step 3.1: Handling missing values...")
print("-" * 80)

# Select relevant columns
df = df_raw[required_vars].copy()

# Report missing values
missing_counts = df.isnull().sum()
missing_pct = (missing_counts / len(df) * 100).round(2)
missing_report = pd.DataFrame({
    'Variable': missing_counts.index,
    'Missing_Count': missing_counts.values,
    'Missing_Percent': missing_pct.values
})
missing_report = missing_report[missing_report['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_report) > 0:
    print("Missing values detected:")
    print(missing_report.to_string(index=False))
    print()
    
    # Drop rows with missing values
    df_clean = df.dropna()
    print(f"✓ Dropped {len(df) - len(df_clean):,} rows with missing values")
    print(f"✓ Clean dataset: {len(df_clean):,} cases ({len(df_clean)/len(df)*100:.1f}% retained)")
else:
    df_clean = df.copy()
    print("✓ No missing values detected")

print()

print("Step 3.2: Creating district-level features...")
print("-" * 80)

# Check district variable
if 'DISTRICT' in df_clean.columns:
    district_var = 'DISTRICT'
    print(f"✓ Using DISTRICT variable for multilevel clustering")
else:
    print("⚠ DISTRICT variable not found, creating synthetic district variable")
    # Create synthetic district based on case characteristics
    df_clean['DISTRICT'] = (df_clean['NEWRACE'] * 10 + df_clean['TYPEMONY']).astype(int)
    district_var = 'DISTRICT'

# Report district statistics
n_districts = df_clean[district_var].nunique()
district_sizes = df_clean[district_var].value_counts()

print(f"✓ Number of districts: {n_districts}")
print(f"✓ District size range: {district_sizes.min()} to {district_sizes.max()} cases")
print(f"✓ Mean district size: {district_sizes.mean():.1f} cases")
print(f"✓ Median district size: {district_sizes.median():.1f} cases")
print()

print("Step 3.3: Creating dummy variables for districts...")
print("-" * 80)

# Create district dummy variables (fixed effects approach)
df_with_dummies = pd.get_dummies(df_clean, columns=[district_var], drop_first=True, dtype=float)
district_cols = [col for col in df_with_dummies.columns if col.startswith(f'{district_var}_')]

print(f"✓ Created {len(district_cols)} district dummy variables")
print()

# ============================================================================
# STEP 4: TRAIN-TEST SPLIT
# ============================================================================

print("=" * 80)
print("STEP 4: TRAIN-TEST SPLIT")
print("=" * 80)
print()

print("Preparing features and target...")

# Define feature columns
feature_cols = [
    'race_black', 'race_hispanic', 'MONSEX', 'AGE', 
    'atty_appointed', 'atty_public_def', 'atty_pro_se', 
    'CRIMPTS', 'XFOLSOR', 'ACCAP'
] + district_cols

# Prepare X and y
X = df_with_dummies[feature_cols]
y = df_with_dummies['PRISDUM']
race = df_with_dummies['NEWRACE'].map(RACE_LABELS)

print(f"✓ Feature matrix shape: {X.shape}")
print(f"✓ Target variable shape: {y.shape}")
print(f"✓ Number of features: {len(feature_cols)}")
print(f"  - Individual-level features: 10")
print(f"  - District dummy variables: {len(district_cols)}")
print()

# Split data
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test, race_train, race_test = train_test_split(
    X, y, race, 
    test_size=0.3, 
    random_state=RANDOM_SEED, 
    stratify=y
)

print(f"✓ Training set: {len(X_train):,} cases ({len(X_train)/len(X)*100:.1f}%)")
print(f"✓ Test set: {len(X_test):,} cases ({len(X_test)/len(X)*100:.1f}%)")
print()

# Report class distribution
print("Class distribution:")
print(f"  Training set:")
print(f"    No Prison: {(y_train == 0).sum():,} ({(y_train == 0).sum()/len(y_train)*100:.1f}%)")
print(f"    Prison: {(y_train == 1).sum():,} ({(y_train == 1).sum()/len(y_train)*100:.1f}%)")
print(f"  Test set:")
print(f"    No Prison: {(y_test == 0).sum():,} ({(y_test == 0).sum()/len(y_test)*100:.1f}%)")
print(f"    Prison: {(y_test == 1).sum():,} ({(y_test == 1).sum()/len(y_test)*100:.1f}%)")
print()

# Report race distribution in test set
print("Race distribution in test set:")
race_dist = race_test.value_counts()
for race_label in sorted(race_dist.index):
    count = race_dist[race_label]
    pct = count / len(race_test) * 100
    print(f"  {race_label}: {count:,} ({pct:.1f}%)")
print()

# ============================================================================
# STEP 5: MODEL TRAINING
# ============================================================================

print("=" * 80)
print("STEP 5: MULTILEVEL MODEL TRAINING")
print("=" * 80)
print()

print("Training logistic regression with district fixed effects...")
print("(This may take a few minutes due to the large number of features...)")
print()

# Train model
model = LogisticRegression(
    max_iter=1000, 
    random_state=RANDOM_SEED, 
    class_weight='balanced',  # Handle class imbalance
    solver='lbfgs',           # Efficient solver for large datasets
    verbose=0
)

model.fit(X_train, y_train)

print("✓ Model training complete")
print()

# ============================================================================
# STEP 6: MODEL EVALUATION
# ============================================================================

print("=" * 80)
print("STEP 6: MODEL EVALUATION")
print("=" * 80)
print()

print("Making predictions on test set...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("✓ Predictions complete")
print()

# Overall accuracy
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, y_pred)

print("Model Performance:")
print(f"  Training accuracy: {train_acc:.4f}")
print(f"  Test accuracy: {test_acc:.4f}")
print()

# Classification report
print("Classification Report:")
print("-" * 80)
print(classification_report(y_test, y_pred, target_names=['No Prison', 'Prison']))
print()

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(f"  [[TN={cm[0,0]:5d}, FP={cm[0,1]:5d}]")
print(f"   [FN={cm[1,0]:5d}, TP={cm[1,1]:5d}]]")
print()

# ============================================================================
# STEP 7: FAIRNESS METRICS CALCULATION
# ============================================================================

print("=" * 80)
print("STEP 7: FAIRNESS METRICS CALCULATION")
print("=" * 80)
print()

print("Calculating fairness metrics by race...")
print()

# 1. Selection Rate
print("1. Selection Rate (Predicted Prison Rate)")
print("-" * 80)
selection_rates = MetricFrame(
    metrics=selection_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(selection_rates.by_group)
print(f"\nOverall: {selection_rates.overall:.4f}")
print(f"Difference (max - min): {selection_rates.difference():.4f}")
print(f"Ratio (min / max): {selection_rates.ratio():.4f}")
print()

# 2. True Positive Rate
print("2. True Positive Rate (Sensitivity)")
print("-" * 80)
tpr_frame = MetricFrame(
    metrics=true_positive_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(tpr_frame.by_group)
print(f"\nOverall: {tpr_frame.overall:.4f}")
print(f"Difference (max - min): {tpr_frame.difference():.4f}")
print(f"Ratio (min / max): {tpr_frame.ratio():.4f}")
print()

# 3. False Positive Rate
print("3. False Positive Rate")
print("-" * 80)
fpr_frame = MetricFrame(
    metrics=false_positive_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(fpr_frame.by_group)
print(f"\nOverall: {fpr_frame.overall:.4f}")
print(f"Difference (max - min): {fpr_frame.difference():.4f}")
print(f"Ratio (min / max): {fpr_frame.ratio():.4f}")
print()

# 4. False Negative Rate
print("4. False Negative Rate")
print("-" * 80)
fnr_frame = MetricFrame(
    metrics=false_negative_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(fnr_frame.by_group)
print(f"\nOverall: {fnr_frame.overall:.4f}")
print(f"Difference (max - min): {fnr_frame.difference():.4f}")
print(f"Ratio (min / max): {fnr_frame.ratio():.4f}")
print()

# 5. Demographic Parity
print("5. Demographic Parity (Disparate Impact)")
print("-" * 80)
dp_ratio = demographic_parity_ratio(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(f"Demographic Parity Ratio: {dp_ratio:.4f}")
print()
print("Interpretation:")
print(f"  - Ratio of 1.0 = perfect parity")
print(f"  - Ratio > 0.8 = passes 80% rule (no disparate impact)")
print(f"  - This model: {'PASS ✓' if dp_ratio >= 0.8 else 'FAIL ✗'}")
print()

# 6. Equalized Odds
print("6. Equalized Odds")
print("-" * 80)
eo_ratio = equalized_odds_ratio(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
print(f"Equalized Odds Ratio: {eo_ratio:.4f}")
print()
print("Interpretation:")
print(f"  - Ratio of 1.0 = perfect equalized odds")
print(f"  - Higher ratio = more fair")
print()

# ============================================================================
# STEP 8: SAVE RESULTS
# ============================================================================

print("=" * 80)
print("STEP 8: SAVING RESULTS")
print("=" * 80)
print()

# Create comprehensive results dataframe
fairness_results = pd.DataFrame({
    'Race': sorted(race_test.unique()),
    'Sample_Size': [race_test.value_counts()[race] for race in sorted(race_test.unique())],
    'Selection_Rate': [selection_rates.by_group[race] for race in sorted(race_test.unique())],
    'True_Positive_Rate': [tpr_frame.by_group[race] for race in sorted(race_test.unique())],
    'False_Positive_Rate': [fpr_frame.by_group[race] for race in sorted(race_test.unique())],
    'False_Negative_Rate': [fnr_frame.by_group[race] for race in sorted(race_test.unique())]
})

fairness_results.to_csv(REPRODUCTION_DIR / 'multilevel_fairness_by_race.csv', index=False)
print(f"✓ Saved: multilevel_fairness_by_race.csv")

# Save summary metrics
summary_metrics = pd.DataFrame({
    'Metric': [
        'Demographic Parity Ratio',
        'Equalized Odds Ratio',
        'Selection Rate Difference',
        'Selection Rate Ratio',
        'TPR Difference',
        'TPR Ratio',
        'FPR Difference',
        'FPR Ratio',
        'FNR Difference',
        'FNR Ratio',
        'Test Accuracy'
    ],
    'Value': [
        dp_ratio,
        eo_ratio,
        selection_rates.difference(),
        selection_rates.ratio(),
        tpr_frame.difference(),
        tpr_frame.ratio(),
        fpr_frame.difference(),
        fpr_frame.ratio(),
        fnr_frame.difference(),
        fnr_frame.ratio(),
        test_acc
    ]
})

summary_metrics.to_csv(REPRODUCTION_DIR / 'multilevel_summary_metrics.csv', index=False)
print(f"✓ Saved: multilevel_summary_metrics.csv")

# Save predictions
predictions_df = pd.DataFrame({
    'y_true': y_test,
    'y_pred': y_pred,
    'y_pred_proba': y_pred_proba,
    'race': race_test
})
predictions_df.to_csv(REPRODUCTION_DIR / 'multilevel_predictions.csv', index=False)
print(f"✓ Saved: multilevel_predictions.csv")

print()

# ============================================================================
# STEP 9: VISUALIZATIONS
# ============================================================================

print("=" * 80)
print("STEP 9: CREATING VISUALIZATIONS")
print("=" * 80)
print()

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300

# 1. Selection Rate by Race
fig, ax = plt.subplots(figsize=(10, 6))
races = sorted(race_test.unique())
sel_rates = [selection_rates.by_group[race] for race in races]
colors = ['steelblue', 'coral', 'seagreen', 'gold']
bars = ax.bar(races, sel_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.axhline(y=selection_rates.overall, color='red', linestyle='--', linewidth=2, 
           label=f'Overall: {selection_rates.overall:.3f}')
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('Selection Rate (Predicted Prison)', fontsize=12, fontweight='bold')
ax.set_title('Multilevel Model: Selection Rate by Race', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(REPRODUCTION_DIR / 'multilevel_selection_rate.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: multilevel_selection_rate.png")

# 2. Fairness Metrics Comparison
fig, ax = plt.subplots(figsize=(12, 6))
metrics_df = fairness_results.set_index('Race')[['Selection_Rate', 'True_Positive_Rate', 
                                                   'False_Positive_Rate', 'False_Negative_Rate']]
metrics_df.plot(kind='bar', ax=ax, width=0.8, color=['steelblue', 'coral', 'seagreen', 'gold'])
ax.set_xlabel('Race', fontsize=12, fontweight='bold')
ax.set_ylabel('Rate', fontsize=12, fontweight='bold')
ax.set_title('Multilevel Model: Fairness Metrics by Race', fontsize=14, fontweight='bold')
ax.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(REPRODUCTION_DIR / 'multilevel_fairness_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: multilevel_fairness_comparison.png")

# 3. Summary Metrics Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
key_metrics = summary_metrics[summary_metrics['Metric'].isin([
    'Demographic Parity Ratio', 'Equalized Odds Ratio', 'Test Accuracy'
])]
bars = ax.barh(key_metrics['Metric'], key_metrics['Value'], 
               color=['seagreen', 'coral', 'steelblue'], alpha=0.7, edgecolor='black', linewidth=1.5)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{width:.3f}',
            ha='left', va='center', fontsize=11, fontweight='bold', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.axvline(x=0.8, color='red', linestyle='--', linewidth=2, label='80% Rule Threshold')
ax.set_xlabel('Score', fontsize=12, fontweight='bold')
ax.set_title('Multilevel Model: Key Performance Metrics', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(REPRODUCTION_DIR / 'multilevel_key_metrics.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: multilevel_key_metrics.png")

print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("=" * 80)
print("REPRODUCTION COMPLETE")
print("=" * 80)
print()

print("Summary of Results:")
print("-" * 80)
print(f"✓ Model: Multilevel Logistic Regression with District Fixed Effects")
print(f"✓ Test Accuracy: {test_acc:.4f}")
print(f"✓ Demographic Parity Ratio: {dp_ratio:.4f} {'(PASS 80% rule)' if dp_ratio >= 0.8 else '(FAIL 80% rule)'}")
print(f"✓ Equalized Odds Ratio: {eo_ratio:.4f}")
print()

print("Fairness Assessment:")
print("-" * 80)
if dp_ratio >= 0.8:
    print("✓ This model PASSES the 80% rule for disparate impact")
    print("  The selection rate for the least favored group is at least 80% of")
    print("  the selection rate for the most favored group.")
else:
    print("✗ This model FAILS the 80% rule for disparate impact")
    print("  The selection rate for the least favored group is less than 80% of")
    print("  the selection rate for the most favored group.")
print()

print("Output Files:")
print("-" * 80)
print(f"  Data: {REPRODUCTION_DIR / 'multilevel_fairness_by_race.csv'}")
print(f"  Metrics: {REPRODUCTION_DIR / 'multilevel_summary_metrics.csv'}")
print(f"  Predictions: {REPRODUCTION_DIR / 'multilevel_predictions.csv'}")
print(f"  Visualizations: {REPRODUCTION_DIR}/*.png")
print()

print("=" * 80)
print("All results saved to:", REPRODUCTION_DIR)
print("=" * 80)
print()
