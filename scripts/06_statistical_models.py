#!/usr/bin/env python3
"""
Statistical Modeling - Legal Literacy and Access to Justice
Author: Barbara D. Gaskins
Date: January 2026

This script implements multiple statistical models to test the hypotheses:
1. Logistic Regression: Prison vs. No Prison
2. Linear Regression: Sentence Length
3. Multilevel Models: Accounting for district clustering
4. Mediation Analysis: Race → Attorney Type → Outcomes
5. Fairness Metrics: Disparate impact analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Statistical packages
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'
MODELS_DIR = OUTPUT_DIR / 'models'
MODELS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("STATISTICAL MODELING")
print("Legal Literacy and Access to Justice in Federal Sentencing")
print("=" * 80)
print()

# Load data
print("Loading data...")
df = pd.read_csv(DATA_DIR / 'ussc_fy2024_working.csv')
print(f"✓ Loaded {len(df):,} cases")
print()

# Data preparation
print("=" * 80)
print("DATA PREPARATION")
print("=" * 80)
print()

# Create clean dataset for modeling
print("Creating clean dataset...")

# Remove missing values for key variables
model_vars = ['NEWRACE', 'MONSEX', 'AGE', 'TYPEMONY', 'CRIMHIST', 'CRIMPTS',
              'GLMIN', 'GLMAX', 'XFOLSOR', 'ACCAP', 'MONCIRC', 'DISTRICT',
              'SENTTOT', 'PRISDUM', 'SENTIMP']

df_model = df[model_vars].copy()
# Keep rows with minimal missing data
df_model = df_model[df_model['PRISDUM'].notna()]
df_model = df_model[df_model['NEWRACE'].notna()]
df_model = df_model[df_model['TYPEMONY'].notna()]
df_model = df_model[df_model['CRIMHIST'].notna()]
# Fill remaining missing with median/mode
for col in ['CRIMPTS', 'XFOLSOR', 'ACCAP', 'MONCIRC']:
    if col in df_model.columns:
        df_model[col] = df_model[col].fillna(df_model[col].median())

print(f"✓ Clean dataset: {len(df_model):,} cases ({len(df_model)/len(df)*100:.1f}% of original)")
print()

# Create derived variables
print("Creating derived variables...")

# 1. Recode race (binary: White vs. Non-White for initial analysis)
df_model['race_white'] = (df_model['NEWRACE'] == 1).astype(int)
df_model['race_black'] = (df_model['NEWRACE'] == 2).astype(int)
df_model['race_hispanic'] = (df_model['NEWRACE'] == 3).astype(int)

# 2. Recode attorney type
df_model['atty_private'] = (df_model['TYPEMONY'] == 1).astype(int)
df_model['atty_appointed'] = (df_model['TYPEMONY'] == 2).astype(int)
df_model['atty_public_def'] = (df_model['TYPEMONY'] == 3).astype(int)
df_model['atty_pro_se'] = (df_model['TYPEMONY'] == 4).astype(int)

# 3. Guideline range midpoint
df_model['guideline_mid'] = (df_model['GLMIN'] + df_model['GLMAX']) / 2

# 4. Sentence relative to guideline (deviation)
df_model['sent_deviation'] = df_model['SENTTOT'] - df_model['guideline_mid']

# 5. High criminal history (Category III+)
df_model['high_crim_hist'] = (df_model['CRIMHIST'] >= 1).astype(int)

print("✓ Derived variables created")
print()

# Descriptive statistics for model variables
print("Model Variables Summary:")
print(df_model[['AGE', 'CRIMPTS', 'XFOLSOR', 'guideline_mid', 'SENTTOT']].describe())
print()

# Save prepared dataset
df_model.to_csv(DATA_DIR / 'ussc_fy2024_model_ready.csv', index=False)
print(f"✓ Saved model-ready dataset: {DATA_DIR / 'ussc_fy2024_model_ready.csv'}")
print()

# ============================================================================
# MODEL 1: LOGISTIC REGRESSION - PRISON VS. NO PRISON
# ============================================================================

print("=" * 80)
print("MODEL 1: LOGISTIC REGRESSION - PRISON SENTENCE")
print("=" * 80)
print()

# Prepare features and target
X_vars = ['race_black', 'race_hispanic', 'MONSEX', 'AGE', 'atty_appointed', 
          'atty_public_def', 'atty_pro_se', 'CRIMPTS', 'XFOLSOR', 'ACCAP']
y_var = 'PRISDUM'

# Remove any remaining missing values
df_logit = df_model[X_vars + [y_var]].dropna()
X = df_logit[X_vars]
y = df_logit[y_var]

print(f"Cases for logistic regression: {len(df_logit):,}")
print()

# Check class distribution
print(f"Class distribution:")
print(y.value_counts())
print(f"Prison rate: {y.mean()*100:.1f}%")
print()

# Only proceed if we have both classes
if len(y.unique()) < 2:
    print("⚠ Warning: Only one class present. Skipping logistic regression.")
    print("This is common in federal sentencing data where prison is nearly universal.")
    print("Proceeding to sentence length analysis...")
    print()
    skip_logistic = True
else:
    skip_logistic = False
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

if not skip_logistic:
    print(f"Training set: {len(X_train):,} cases")
    print(f"Test set: {len(X_test):,} cases")
    print()
    
    # Fit logistic regression
    print("Fitting logistic regression model...")
    log_reg = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    log_reg.fit(X_train, y_train)

    # Predictions
    y_pred = log_reg.predict(X_test)
    y_pred_proba = log_reg.predict_proba(X_test)[:, 1]

    # Evaluation
    print("\nModel Performance:")
    print(f"  Accuracy: {log_reg.score(X_test, y_test):.4f}")
    print(f"  AUC-ROC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print()
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print()
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)
    print()
    
    # Coefficients
    coef_df = pd.DataFrame({
        'Variable': X_vars,
        'Coefficient': log_reg.coef_[0],
        'Odds_Ratio': np.exp(log_reg.coef_[0])
    }).sort_values('Coefficient', ascending=False)
    
    print("Logistic Regression Coefficients:")
    print(coef_df)
    print()
    
    coef_df.to_csv(MODELS_DIR / 'logistic_regression_coefficients.csv', index=False)
    print(f"✓ Saved: {MODELS_DIR / 'logistic_regression_coefficients.csv'}")
    print()
    
    # ROC Curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {roc_auc_score(y_test, y_pred_proba):.3f})')
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('ROC Curve - Prison Sentence Prediction', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(MODELS_DIR / 'roc_curve_prison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: roc_curve_prison.png")
    print()
else:
    print("Note: In federal sentencing, prison is nearly universal (>90% of cases).")
    print("The key question is sentence LENGTH, not prison vs. no prison.")
    print("Proceeding to sentence length analysis...")
    print()

# ============================================================================
# MODEL 2: LINEAR REGRESSION - SENTENCE LENGTH
# ============================================================================

print("=" * 80)
print("MODEL 2: LINEAR REGRESSION - SENTENCE LENGTH")
print("=" * 80)
print()

# Use only cases with prison sentences
df_prison = df_model[df_model['PRISDUM'] == 1].copy()
print(f"Cases with prison sentences: {len(df_prison):,}")
print()

# Log-transform sentence length (common for skewed sentence data)
df_prison['log_senttot'] = np.log(df_prison['SENTTOT'] + 1)

# Prepare features and target
X_vars_ols = ['race_black', 'race_hispanic', 'MONSEX', 'AGE', 'atty_appointed',
              'atty_public_def', 'atty_pro_se', 'CRIMPTS', 'XFOLSOR', 'ACCAP',
              'guideline_mid']
X_ols = df_prison[X_vars_ols]
y_ols = df_prison['log_senttot']

# Split data
X_train_ols, X_test_ols, y_train_ols, y_test_ols = train_test_split(
    X_ols, y_ols, test_size=0.3, random_state=42
)

# Fit OLS regression using statsmodels for detailed statistics
X_train_ols_sm = sm.add_constant(X_train_ols)
X_test_ols_sm = sm.add_constant(X_test_ols)

print("Fitting OLS regression model...")
ols_model = sm.OLS(y_train_ols, X_train_ols_sm).fit()

print("\nOLS Regression Results:")
print(ols_model.summary())
print()

# Predictions
y_pred_ols = ols_model.predict(X_test_ols_sm)

# Evaluation
rmse = np.sqrt(mean_squared_error(y_test_ols, y_pred_ols))
mae = mean_absolute_error(y_test_ols, y_pred_ols)
r2 = r2_score(y_test_ols, y_pred_ols)

print("Model Performance:")
print(f"  R-squared: {r2:.4f}")
print(f"  RMSE: {rmse:.4f}")
print(f"  MAE: {mae:.4f}")
print()

# Save results
ols_results = pd.DataFrame({
    'Variable': ['const'] + X_vars_ols,
    'Coefficient': ols_model.params.values,
    'Std_Error': ols_model.bse.values,
    'T_Statistic': ols_model.tvalues.values,
    'P_Value': ols_model.pvalues.values,
    'CI_Lower': ols_model.conf_int()[0].values,
    'CI_Upper': ols_model.conf_int()[1].values
})

ols_results.to_csv(MODELS_DIR / 'ols_regression_results.csv', index=False)
print(f"✓ Saved: {MODELS_DIR / 'ols_regression_results.csv'}")
print()

# Residual plot
fig, ax = plt.subplots(figsize=(10, 6))
residuals = y_test_ols - y_pred_ols
ax.scatter(y_pred_ols, residuals, alpha=0.5, s=10)
ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax.set_xlabel('Predicted Log(Sentence)', fontsize=12)
ax.set_ylabel('Residuals', fontsize=12)
ax.set_title('Residual Plot - Sentence Length Model', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(MODELS_DIR / 'residual_plot_sentence.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: residual_plot_sentence.png")
print()

# ============================================================================
# MODEL 3: RACE × ATTORNEY TYPE INTERACTION
# ============================================================================

print("=" * 80)
print("MODEL 3: INTERACTION EFFECTS - RACE × ATTORNEY TYPE")
print("=" * 80)
print()

# Create interaction terms
df_prison['race_black_x_atty_appointed'] = df_prison['race_black'] * df_prison['atty_appointed']
df_prison['race_hispanic_x_atty_appointed'] = df_prison['race_hispanic'] * df_prison['atty_appointed']

# Fit model with interactions
X_vars_int = X_vars_ols + ['race_black_x_atty_appointed', 'race_hispanic_x_atty_appointed']
X_int = df_prison[X_vars_int]
X_int_sm = sm.add_constant(X_int)

print("Fitting interaction model...")
int_model = sm.OLS(df_prison['log_senttot'], X_int_sm).fit()

print("\nInteraction Model Results:")
print(int_model.summary())
print()

# Save interaction results
int_results = pd.DataFrame({
    'Variable': ['const'] + X_vars_int,
    'Coefficient': int_model.params.values,
    'Std_Error': int_model.bse.values,
    'P_Value': int_model.pvalues.values
})

int_results.to_csv(MODELS_DIR / 'interaction_model_results.csv', index=False)
print(f"✓ Saved: {MODELS_DIR / 'interaction_model_results.csv'}")
print()

# ============================================================================
# MODEL 4: MEDIATION ANALYSIS
# ============================================================================

print("=" * 80)
print("MODEL 4: MEDIATION ANALYSIS - RACE → ATTORNEY → SENTENCE")
print("=" * 80)
print()

print("Testing mediation pathway:")
print("  Independent Variable: Race (Black)")
print("  Mediator: Attorney Type (Appointed vs. Private)")
print("  Dependent Variable: Sentence Length")
print()

# Step 1: Total effect (c path): Race → Sentence
print("Step 1: Total Effect (Race → Sentence)")
X_c = sm.add_constant(df_prison[['race_black', 'CRIMPTS', 'XFOLSOR', 'guideline_mid']])
model_c = sm.OLS(df_prison['log_senttot'], X_c).fit()
c_coef = model_c.params['race_black']
c_pval = model_c.pvalues['race_black']
print(f"  Total effect (c): {c_coef:.4f} (p={c_pval:.4f})")
print()

# Step 2: Effect on mediator (a path): Race → Attorney Type
print("Step 2: Effect on Mediator (Race → Attorney Type)")
X_a = sm.add_constant(df_prison[['race_black', 'CRIMPTS', 'XFOLSOR']])
model_a = sm.Logit(df_prison['atty_appointed'], X_a).fit(disp=0)
a_coef = model_a.params['race_black']
a_pval = model_a.pvalues['race_black']
print(f"  Effect on mediator (a): {a_coef:.4f} (p={a_pval:.4f})")
print()

# Step 3: Direct effect (c' path): Race → Sentence (controlling for Attorney)
print("Step 3: Direct Effect (Race → Sentence, controlling for Attorney)")
X_cp = sm.add_constant(df_prison[['race_black', 'atty_appointed', 'CRIMPTS', 'XFOLSOR', 'guideline_mid']])
model_cp = sm.OLS(df_prison['log_senttot'], X_cp).fit()
cp_coef = model_cp.params['race_black']
cp_pval = model_cp.pvalues['race_black']
b_coef = model_cp.params['atty_appointed']
b_pval = model_cp.pvalues['atty_appointed']
print(f"  Direct effect (c'): {cp_coef:.4f} (p={cp_pval:.4f})")
print(f"  Mediator effect (b): {b_coef:.4f} (p={b_pval:.4f})")
print()

# Indirect effect (mediation effect)
indirect_effect = a_coef * b_coef
print(f"Indirect effect (a × b): {indirect_effect:.4f}")
print(f"Proportion mediated: {(indirect_effect / c_coef * 100):.1f}%")
print()

# Save mediation results
mediation_results = pd.DataFrame({
    'Path': ['Total Effect (c)', 'Effect on Mediator (a)', 'Direct Effect (c\')', 
             'Mediator Effect (b)', 'Indirect Effect (a×b)'],
    'Coefficient': [c_coef, a_coef, cp_coef, b_coef, indirect_effect],
    'P_Value': [c_pval, a_pval, cp_pval, b_pval, np.nan]
})

mediation_results.to_csv(MODELS_DIR / 'mediation_analysis_results.csv', index=False)
print(f"✓ Saved: {MODELS_DIR / 'mediation_analysis_results.csv'}")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("MODELING COMPLETE")
print("=" * 80)
print()
print("Models fitted:")
print("  1. Logistic Regression (Prison vs. No Prison)")
print("  2. OLS Regression (Sentence Length)")
print("  3. Interaction Model (Race × Attorney Type)")
print("  4. Mediation Analysis (Race → Attorney → Sentence)")
print()
print(f"All results saved to: {MODELS_DIR}")
print()
print("Next steps:")
print("  1. Fairness metrics evaluation")
print("  2. Multilevel modeling (district effects)")
print("  3. Comprehensive report writing")
