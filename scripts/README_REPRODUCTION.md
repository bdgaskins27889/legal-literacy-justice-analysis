# Multilevel Model Fairness Analysis - Reproduction Guide

**Author**: Barbara D. Gaskins

**Date**: January 25, 2026

---

## Overview

This guide provides complete instructions for reproducing the Multilevel Model's fairness analysis from scratch. The reproduction script (`10_reproduce_multilevel_fairness.py`) is a standalone, fully documented Python script that performs all steps from data loading to fairness evaluation.

## What This Script Does

The reproduction script performs the following steps:

1.  **Data Loading**: Loads the USSC FY 2024 dataset
2.  **Variable Selection**: Selects relevant features for the multilevel model
3.  **Data Preprocessing**: Handles missing values and creates district-level features
4.  **Train-Test Split**: Splits data into training (70%) and test (30%) sets
5.  **Model Training**: Trains a logistic regression model with district fixed effects
6.  **Model Evaluation**: Evaluates accuracy and classification performance
7.  **Fairness Metrics**: Calculates comprehensive fairness metrics by race
8.  **Saves Results**: Exports all metrics and predictions to CSV files
9.  **Visualizations**: Creates publication-quality charts

## Requirements

### Python Packages

```bash
pip install pandas numpy scikit-learn fairlearn matplotlib seaborn
```

### Data

The script requires the preprocessed dataset:
- `data/ussc_fy2024_model_ready.csv`

This file should already exist in your project directory if you've run the earlier data extraction scripts.

## Usage

### Basic Usage

Run the script from the project root directory:

```bash
cd /home/ubuntu/legal_literacy_justice_project
python3 scripts/10_reproduce_multilevel_fairness.py
```

### Expected Runtime

- On a standard machine: 2-5 minutes
- The model training step may take longer due to the large number of features (10 individual-level + 93 district dummy variables)

### Output

The script creates the following files in `outputs/reproduction/`:

#### Data Files
- `multilevel_fairness_by_race.csv` - Fairness metrics for each racial group
- `multilevel_summary_metrics.csv` - Overall fairness summary
- `multilevel_predictions.csv` - Model predictions on test set

#### Visualizations
- `multilevel_selection_rate.png` - Selection rate by race
- `multilevel_fairness_comparison.png` - All fairness metrics by race
- `multilevel_key_metrics.png` - Summary of key performance metrics

#### Log File
- `outputs/reproduction_log.txt` - Complete execution log

## Expected Results

### Model Performance

- **Test Accuracy**: ~0.778 (77.8%)
- **Training Accuracy**: ~0.783 (78.3%)

### Fairness Metrics

| Metric | Expected Value | Interpretation |
|:-------|:---------------|:---------------|
| **Demographic Parity Ratio** | **0.816** | **PASS** (> 0.8 threshold) |
| **Equalized Odds Ratio** | 0.423 | Higher is better |
| **Selection Rate Difference** | 0.143 | Lower is better |
| **TPR Difference** | 0.139 | Lower is better |
| **FPR Difference** | 0.139 | Lower is better |

### Key Finding

The Multilevel Model **passes the 80% rule** for disparate impact, making it the least biased of the three models evaluated in this project.

## Understanding the Code

### Model Architecture

The multilevel model is implemented as a **logistic regression with district fixed effects**:

```python
# Individual-level features (10)
individual_features = [
    'race_black', 'race_hispanic', 'MONSEX', 'AGE',
    'atty_appointed', 'atty_public_def', 'atty_pro_se',
    'CRIMPTS', 'XFOLSOR', 'ACCAP'
]

# District dummy variables (93)
district_dummies = pd.get_dummies(df, columns=['DISTRICT'], drop_first=True)

# Combined feature set
X = df[individual_features + district_dummies]
```

### Why District Fixed Effects?

Including district dummy variables allows the model to account for systematic differences between judicial districts. This helps isolate the effects of individual characteristics (like race and attorney type) from district-level factors (like local sentencing practices or case composition).

### Fairness Evaluation

The script uses the `fairlearn` library to calculate standard fairness metrics:

- **Selection Rate**: Proportion predicted to receive prison
- **True Positive Rate (TPR)**: Sensitivity
- **False Positive Rate (FPR)**: Type I error rate
- **False Negative Rate (FNR)**: Type II error rate
- **Demographic Parity Ratio**: min(selection_rate) / max(selection_rate)
- **Equalized Odds Ratio**: Measures balance in TPR and FPR across groups

## Troubleshooting

### Issue: Script runs slowly

**Solution**: The model has 103 features (10 individual + 93 district dummies). This is expected. Consider:
- Reducing `max_iter` in LogisticRegression (default: 1000)
- Using a smaller test set size (default: 0.3)

### Issue: Memory error

**Solution**: The dataset has 60,000+ cases. If you encounter memory issues:
- Close other applications
- Use a machine with more RAM
- Sample a subset of the data (modify the script to use `df.sample(frac=0.5)`)

### Issue: Different results than reported

**Solution**: Ensure you're using the same random seed:
- The script uses `RANDOM_SEED = 42`
- This ensures reproducibility across runs

## Customization

### Changing the Test Set Size

Modify line 60:

```python
# Change from 0.3 (30%) to desired proportion
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y
)
```

### Adding More Fairness Metrics

The `fairlearn` library provides additional metrics. Add them in Step 7:

```python
from fairlearn.metrics import accuracy_score_group_min

# Calculate minimum accuracy across groups
min_acc = accuracy_score_group_min(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=race_test
)
```

### Changing Output Directory

Modify line 48:

```python
REPRODUCTION_DIR = OUTPUT_DIR / 'your_custom_directory'
```

## Validation

To verify the script is working correctly:

1.  **Check the log output**: Should show "PASS ✓" for the 80% rule
2.  **Inspect the CSV files**: Should contain 4 rows (one per racial group)
3.  **View the visualizations**: Should show clear differences across groups
4.  **Compare to reported results**: Demographic Parity Ratio should be ~0.816

## Citation

If you use this reproduction script in your work, please cite:

> Gaskins, B. D. (2026). The Scales of Justice: An Analysis of Representation and Sentencing Outcomes in U.S. Federal Courts. Master's Portfolio Project, Data Science Program.

## Support

For questions or issues with this reproduction script, please contact:

**Barbara D. Gaskins**
- Email: bdgaskins27889@gmail.com
- Phone: 252.495.3173
- LinkedIn: [Barbara D. Gaskins](https://www.linkedin.com/in/barbara-d-gaskins)

---

**Last Updated**: January 25, 2026
