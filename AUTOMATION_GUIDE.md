# Automation Guide: Verification and Update Script

**Script**: `scripts/14_automate_verification_and_update.py`  
**Author**: Barbara D. Gaskins  
**Date**: February 2026

---

## Overview

This automation script eliminates manual verification work by automatically:

1. ✅ Loading and validating data
2. ✅ Training and evaluating models
3. ✅ Calculating fairness metrics
4. ✅ Generating verification reports
5. ✅ Updating README with latest statistics
6. ✅ Creating timestamped backups
7. ✅ Saving results as JSON

**Key Benefit**: Whenever you get new data, simply run this script and your entire portfolio is updated with verified statistics.

---

## Quick Start

### Basic Usage

```bash
# Run with default settings
python scripts/14_automate_verification_and_update.py
```

This will:
- Load data from `data/ussc_fy2024_model_ready.csv`
- Generate report in `docs/AUTO_VERIFICATION_REPORT.md`
- Update `README.md` with latest statistics
- Create backups in `backups/` directory

### Expected Output

```
================================================================================
AUTOMATED VERIFICATION PIPELINE
================================================================================
Started: 2026-02-08 17:30:00

================================================================================
LOADING AND VALIDATING DATA
================================================================================
✓ Loaded: data/ussc_fy2024_model_ready.csv
  Rows: 52,456
  Columns: 23
✓ All required columns present

Calculating descriptive statistics...
  Complete cases: 52,456
  Missing rate: 0.00%
  Prison rate: 87.50%

Preparing data for modeling...
  Train set: 36,719
  Test set: 15,737

Training Logistic Regression...
✓ Model trained

Evaluating model...
  Accuracy: 0.7780
  AUC-ROC: 0.8700

Calculating fairness metrics...
  Demographic Parity Ratio: 0.8160
  Passes 80% rule: True
  TPR Disparity: 0.1390
  FPR Disparity: 0.1390

Generating verification report...
✓ Verification report saved: docs/AUTO_VERIFICATION_REPORT.md

Updating README...
✓ README updated: README.md

✓ Results saved: docs/verification_results.json

================================================================================
VERIFICATION COMPLETE
================================================================================
Completed: 2026-02-08 17:32:15

Summary:
  ✓ Data verified: 52,456 cases
  ✓ Model accuracy: 77.80%
  ✓ Demographic Parity: 0.816 (PASS)
  ✓ Report generated: docs/AUTO_VERIFICATION_REPORT.md
  ✓ README updated: README.md
```

---

## Advanced Usage

### Custom Data Path

```bash
python scripts/14_automate_verification_and_update.py \
    --data-path /path/to/new_data.csv
```

### Custom Output Directory

```bash
python scripts/14_automate_verification_and_update.py \
    --output-dir /path/to/output
```

### Skip Backup Creation

```bash
python scripts/14_automate_verification_and_update.py --no-backup
```

### Combine Options

```bash
python scripts/14_automate_verification_and_update.py \
    --data-path data/ussc_fy2025.csv \
    --output-dir docs/fy2025 \
    --no-backup
```

---

## Command Line Options

| Option | Description | Default |
|:-------|:------------|:--------|
| `--data-path PATH` | Path to data file | `data/ussc_fy2024_model_ready.csv` |
| `--output-dir PATH` | Output directory for reports | `docs/` |
| `--no-backup` | Skip creating backups | Backups enabled |

---

## What Gets Generated

### 1. Verification Report

**File**: `docs/AUTO_VERIFICATION_REPORT.md`

A comprehensive markdown report containing:
- Data source information
- Model performance metrics
- Fairness metrics (demographic parity, error rates)
- Verification summary and certification

**Sections**:
1. Executive Summary
2. Data Source
3. Model Performance
4. Fairness Metrics
5. Verification Summary
6. Certification

### 2. Updated README

**File**: `README.md`

The script updates your README with:
- Latest verification timestamp badge
- Current statistics
- Verified metrics

**Badge Added**:
```markdown
[![Last Verified](https://img.shields.io/badge/Last%20Verified-2026--02--08-success)](docs/AUTO_VERIFICATION_REPORT.md)
```

### 3. Results JSON

**File**: `docs/verification_results.json`

Machine-readable results for programmatic access:

```json
{
  "data": {
    "total_cases": 52456,
    "complete_cases": 52456,
    "missing_rate": 0.0,
    "race_distribution": {...},
    "prison_rate": 0.875
  },
  "model": {
    "accuracy": 0.778,
    "auc_roc": 0.87,
    "confusion_matrix": {...}
  },
  "fairness": {
    "demographic_parity_ratio": 0.816,
    "selection_rate_disparity": 0.143,
    "passes_80_rule": true,
    "tpr_disparity": 0.139,
    "fpr_disparity": 0.139,
    ...
  }
}
```

### 4. Backups

**Directory**: `backups/`

Timestamped backups of files before modification:
- `AUTO_VERIFICATION_REPORT_20260208_173000.md`
- `README_20260208_173000.md`

---

## Use Cases

### 1. Annual Data Updates

When USSC releases new fiscal year data:

```bash
# Download FY 2025 data
wget https://www.ussc.gov/.../opafy25nid.csv

# Extract relevant columns (same as before)
csvcut -c 681,684,... opafy25nid.csv > data/ussc_fy2025.csv

# Run automation
python scripts/14_automate_verification_and_update.py \
    --data-path data/ussc_fy2025.csv
```

Your entire portfolio is now updated with FY 2025 data!

### 2. Model Improvements

After improving your model:

```bash
# Modify the script's model training section
# Then re-run verification
python scripts/14_automate_verification_and_update.py
```

All metrics automatically recalculated and documented.

### 3. Pre-Presentation Check

Before a presentation or interview:

```bash
# Verify all statistics are current
python scripts/14_automate_verification_and_update.py

# Review the generated report
cat docs/AUTO_VERIFICATION_REPORT.md
```

Confidence that all numbers are accurate!

### 4. Continuous Integration

Add to GitHub Actions for automatic verification:

```yaml
# .github/workflows/verify.yml
name: Verify Statistics

on:
  push:
    paths:
      - 'data/**'
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python scripts/14_automate_verification_and_update.py
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Auto-update verification report"
```

---

## Configuration

### Modifying Default Settings

Edit the `Config` class in the script:

```python
class Config:
    def __init__(self, data_path=None, output_dir=None):
        # Change default paths
        self.DATA_PATH = Path(data_path) if data_path else ...
        
        # Change model settings
        self.RANDOM_SEED = 42
        self.TEST_SIZE = 0.3
        
        # Change feature columns
        self.FEATURE_COLS = ['NEWRACE', 'AGE', ...]
        
        # Change thresholds
        self.DISPARATE_IMPACT_THRESHOLD = 0.80
```

### Adding New Metrics

To add new fairness metrics:

1. **Add calculation method** to `FairnessCalculator` class:

```python
def calculate_new_metric(self, y_true, y_pred):
    """Calculate your new metric"""
    metric_value = ...  # Your calculation
    self.results['new_metric'] = metric_value
    return metric_value
```

2. **Call in pipeline**:

```python
# In VerificationPipeline.run()
calculator.calculate_new_metric(y_test, y_pred)
```

3. **Add to report template** in `ReportGenerator`:

```python
report += f"""
### New Metric

| Metric | Value |
|:-------|:------|
| **New Metric** | {all_results['fairness']['new_metric']:.4f} |
"""
```

---

## Troubleshooting

### Issue: "Data file not found"

**Solution**: Verify the data path is correct

```bash
# Check if file exists
ls -lh data/ussc_fy2024_model_ready.csv

# Or specify full path
python scripts/14_automate_verification_and_update.py \
    --data-path /full/path/to/data.csv
```

### Issue: "Missing required columns"

**Solution**: Ensure your data has the required columns

```python
# Required columns (default):
FEATURE_COLS = ['NEWRACE', 'AGE', 'CRIMINAL_HISTORY', 'TYPEMONY']
TARGET_COL = 'PRISDUM'
```

Check your data:
```bash
head -1 data/ussc_fy2024_model_ready.csv
```

### Issue: "Model training failed"

**Solution**: Check for data quality issues

```python
# The script handles missing values, but check for:
# - Infinite values
# - Non-numeric data in numeric columns
# - Extreme outliers

# Add data cleaning if needed
```

### Issue: Script runs but README not updated

**Solution**: Check README path and permissions

```bash
# Verify README exists
ls -lh README.md

# Check write permissions
chmod u+w README.md
```

---

## Best Practices

### 1. Run Before Major Events

- ✅ Before job interviews
- ✅ Before academic presentations
- ✅ Before submitting to organizations
- ✅ After any data or model changes

### 2. Review Generated Reports

Don't just run blindly—always review:
- Check the verification report for anomalies
- Verify metrics make sense
- Review any warnings or errors

### 3. Keep Backups

The script creates backups automatically, but also:
- Commit to Git before running
- Keep copies of important versions
- Document major changes

### 4. Version Control

```bash
# After running automation
git add docs/AUTO_VERIFICATION_REPORT.md
git add docs/verification_results.json
git add README.md
git commit -m "Auto-update: verification run $(date +%Y-%m-%d)"
git push
```

### 5. Schedule Regular Runs

Set up a cron job for automatic verification:

```bash
# Edit crontab
crontab -e

# Add line to run weekly on Sundays at midnight
0 0 * * 0 cd /path/to/project && python scripts/14_automate_verification_and_update.py
```

---

## Integration with Existing Workflow

### Workflow Diagram

```
New Data Available
       ↓
Download & Extract
       ↓
Run Automation Script ← You are here
       ↓
Review Generated Reports
       ↓
Commit to Git
       ↓
Push to GitHub
       ↓
Portfolio Updated! ✓
```

### Complete Update Workflow

```bash
#!/bin/bash
# complete_update.sh - Complete portfolio update workflow

echo "Starting portfolio update..."

# 1. Download new data (if needed)
# wget https://www.ussc.gov/.../new_data.csv

# 2. Extract relevant columns (if needed)
# csvcut -c 681,684,... new_data.csv > data/processed.csv

# 3. Run automation
python scripts/14_automate_verification_and_update.py

# 4. Review changes
echo "Review the following files:"
echo "  - docs/AUTO_VERIFICATION_REPORT.md"
echo "  - docs/verification_results.json"
echo "  - README.md"

read -p "Proceed with Git commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # 5. Commit to Git
    git add docs/AUTO_VERIFICATION_REPORT.md
    git add docs/verification_results.json
    git add README.md
    git commit -m "Auto-update: verification run $(date +%Y-%m-%d)"
    
    # 6. Push to GitHub
    git push origin main
    
    echo "Portfolio updated successfully!"
fi
```

Make it executable:
```bash
chmod +x complete_update.sh
./complete_update.sh
```

---

## Performance

### Typical Runtime

| Dataset Size | Runtime |
|:-------------|:--------|
| 10,000 cases | ~30 seconds |
| 50,000 cases | ~2 minutes |
| 100,000 cases | ~5 minutes |

### Memory Usage

- **Minimum**: 1 GB RAM
- **Recommended**: 4 GB RAM
- **Large datasets (>100k)**: 8 GB RAM

### Optimization Tips

For large datasets:

```python
# In Config class, add:
self.SAMPLE_SIZE = 50000  # Sample for faster processing

# In DataVerifier.load_data():
df = pd.read_csv(self.config.DATA_PATH)
if len(df) > self.config.SAMPLE_SIZE:
    df = df.sample(n=self.config.SAMPLE_SIZE, random_state=42)
```

---

## Security Considerations

### Data Privacy

- ✅ Script processes data locally
- ✅ No data sent to external services
- ✅ Backups stored locally only

### Sensitive Information

If your data contains sensitive information:

```python
# Add data anonymization before processing
def anonymize_data(df):
    # Remove or hash sensitive columns
    df = df.drop(columns=['DEFENDANT_NAME', 'SSN'], errors='ignore')
    return df
```

---

## Support and Maintenance

### Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the script's error messages
3. Check the GitHub issues page
4. Contact: bdgaskins27889@gmail.com

### Updating the Script

To update the script with new features:

```bash
# Pull latest version
git pull origin main

# Or download manually
wget https://raw.githubusercontent.com/YOUR_USERNAME/legal-literacy-justice-analysis/main/scripts/14_automate_verification_and_update.py
```

---

## Summary

This automation script transforms your portfolio maintenance from a manual, error-prone process into a single command. It ensures:

✅ **Accuracy**: All statistics verified from source  
✅ **Consistency**: Same methodology every time  
✅ **Efficiency**: Minutes instead of hours  
✅ **Confidence**: Comprehensive verification reports  
✅ **Professionalism**: Always up-to-date portfolio  

**Run it regularly, trust the results, and focus on what matters: your analysis and insights!**

---

*For questions or improvements, contact Barbara D. Gaskins at bdgaskins27889@gmail.com*
