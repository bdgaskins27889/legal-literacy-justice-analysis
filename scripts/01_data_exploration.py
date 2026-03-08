#!/usr/bin/env python3
"""
Legal Literacy and Access to Justice: Data Exploration
Author: Barbara D. Gaskins
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'

print("=" * 80)
print("LEGAL LITERACY AND ACCESS TO JUSTICE")
print("Exploratory Data Analysis - US Sentencing Commission FY 2024")
print("=" * 80)
print()

# Load data
print("Loading dataset...")
df = pd.read_csv(DATA_DIR / 'opafy24nid.csv', low_memory=False)
print(f"✓ Loaded {len(df):,} cases with {len(df.columns):,} variables")
print()

# Basic info
print("Dataset Overview:")
print(f"  Shape: {df.shape}")
print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print()

# Identify key variables based on research framework
print("Identifying key variables for legal literacy analysis...")
print()

# Search for relevant columns
key_patterns = {
    'Demographics': ['race', 'gender', 'age', 'ethnic', 'citizen'],
    'Representation': ['attorney', 'counsel', 'defend', 'represent'],
    'Offense': ['offense', 'charge', 'crime', 'convict'],
    'Criminal History': ['prior', 'criminal', 'history', 'recid'],
    'Pretrial': ['pretrial', 'detention', 'bail', 'release'],
    'Outcomes': ['sentence', 'prison', 'probation', 'fine', 'jail'],
    'Procedural': ['motion', 'plea', 'trial', 'hearing', 'appear']
}

found_vars = {}
for category, patterns in key_patterns.items():
    matches = []
    for col in df.columns:
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in patterns):
            matches.append(col)
    found_vars[category] = matches
    print(f"{category}: {len(matches)} variables found")

print()
print("Key Variables by Category:")
for category, vars_list in found_vars.items():
    if vars_list:
        print(f"\n{category}:")
        for var in vars_list[:10]:  # Show first 10
            print(f"  - {var}")
        if len(vars_list) > 10:
            print(f"  ... and {len(vars_list) - 10} more")

# Save variable mapping
var_mapping_df = pd.DataFrame([
    {'Category': cat, 'Variable': var}
    for cat, vars_list in found_vars.items()
    for var in vars_list
])
var_mapping_df.to_csv(OUTPUT_DIR / 'variable_mapping.csv', index=False)
print(f"\n✓ Variable mapping saved to {OUTPUT_DIR / 'variable_mapping.csv'}")

# Examine specific key variables
print("\n" + "=" * 80)
print("EXAMINING KEY VARIABLES")
print("=" * 80)

# Race/Ethnicity
if 'NEWRACE' in df.columns:
    print("\nRace Distribution (NEWRACE):")
    print(df['NEWRACE'].value_counts().head(10))
    print(f"Missing: {df['NEWRACE'].isna().sum()} ({df['NEWRACE'].isna().sum()/len(df)*100:.1f}%)")

# Age
if 'AGE' in df.columns:
    print("\nAge Statistics:")
    print(df['AGE'].describe())
    print(f"Missing: {df['AGE'].isna().sum()} ({df['AGE'].isna().sum()/len(df)*100:.1f}%)")

# Gender
if 'MONSEX' in df.columns:
    print("\nGender Distribution (MONSEX):")
    print(df['MONSEX'].value_counts())
    print(f"Missing: {df['MONSEX'].isna().sum()} ({df['MONSEX'].isna().sum()/len(df)*100:.1f}%)")

# Sentence type
if 'SENTTOT' in df.columns:
    print("\nTotal Sentence Length (SENTTOT) - in months:")
    print(df['SENTTOT'].describe())
    print(f"Missing: {df['SENTTOT'].isna().sum()} ({df['SENTTOT'].isna().sum()/len(df)*100:.1f}%)")

# Prison sentence
if 'PRISDUM' in df.columns:
    print("\nPrison Sentence Indicator (PRISDUM):")
    print(df['PRISDUM'].value_counts())
    print(f"Missing: {df['PRISDUM'].isna().sum()} ({df['PRISDUM'].isna().sum()/len(df)*100:.1f}%)")

# Probation
if 'PROBDUM' in df.columns:
    print("\nProbation Indicator (PROBDUM):")
    print(df['PROBDUM'].value_counts())
    print(f"Missing: {df['PROBDUM'].isna().sum()} ({df['PROBDUM'].isna().sum()/len(df)*100:.1f}%)")

# Criminal history category
if 'CRIMHIST' in df.columns:
    print("\nCriminal History Category (CRIMHIST):")
    print(df['CRIMHIST'].value_counts().sort_index())
    print(f"Missing: {df['CRIMHIST'].isna().sum()} ({df['CRIMHIST'].isna().sum()/len(df)*100:.1f}%)")

# Save summary statistics
print("\n" + "=" * 80)
print("Saving summary statistics...")

# Create comprehensive summary
summary_stats = df.describe(include='all').T
summary_stats.to_csv(OUTPUT_DIR / 'summary_statistics.csv')
print(f"✓ Summary statistics saved to {OUTPUT_DIR / 'summary_statistics.csv'}")

# Missing data analysis
missing_data = pd.DataFrame({
    'Variable': df.columns,
    'Missing_Count': df.isna().sum(),
    'Missing_Percent': (df.isna().sum() / len(df) * 100).round(2)
}).sort_values('Missing_Percent', ascending=False)
missing_data.to_csv(OUTPUT_DIR / 'missing_data_analysis.csv', index=False)
print(f"✓ Missing data analysis saved to {OUTPUT_DIR / 'missing_data_analysis.csv'}")

print("\n" + "=" * 80)
print("EXPLORATION COMPLETE")
print("=" * 80)
print(f"\nTotal cases analyzed: {len(df):,}")
print(f"Total variables: {len(df.columns):,}")
print(f"Output files saved to: {OUTPUT_DIR}")
