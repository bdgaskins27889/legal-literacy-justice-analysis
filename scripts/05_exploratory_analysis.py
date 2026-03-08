#!/usr/bin/env python3
"""
Exploratory Data Analysis - Legal Literacy and Access to Justice
Author: Barbara D. Gaskins
Date: January 2026

This script performs comprehensive EDA on the USSC FY 2024 data to examine
the relationship between legal literacy proxies, representation type, and
sentencing outcomes.
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
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("EXPLORATORY DATA ANALYSIS")
print("Legal Literacy and Access to Justice in Federal Sentencing")
print("=" * 80)
print()

# Load data
print("Loading working dataset...")
df = pd.read_csv(DATA_DIR / 'ussc_fy2024_working.csv')
print(f"✓ Loaded {len(df):,} cases with {len(df.columns)} variables")
print()

# Basic info
print("Dataset Overview:")
print(f"  Cases: {len(df):,}")
print(f"  Variables: {len(df.columns)}")
print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print()

# Variable names
print("Variables:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")
print()

# Missing data analysis
print("=" * 80)
print("MISSING DATA ANALYSIS")
print("=" * 80)
print()

missing = pd.DataFrame({
    'Variable': df.columns,
    'Missing': df.isna().sum(),
    'Percent': (df.isna().sum() / len(df) * 100).round(2)
}).sort_values('Percent', ascending=False)

print(missing)
print()

# Save missing data report
missing.to_csv(OUTPUT_DIR / 'missing_data_report.csv', index=False)
print(f"✓ Saved: {OUTPUT_DIR / 'missing_data_report.csv'}")
print()

# Key variable distributions
print("=" * 80)
print("KEY VARIABLE DISTRIBUTIONS")
print("=" * 80)
print()

# Race
print("1. RACE (NEWRACE):")
print(df['NEWRACE'].value_counts().sort_index())
print(f"   Missing: {df['NEWRACE'].isna().sum()}")
print()

# Gender
print("2. GENDER (MONSEX):")
print(df['MONSEX'].value_counts().sort_index())
print(f"   Missing: {df['MONSEX'].isna().sum()}")
print()

# Age
print("3. AGE:")
print(df['AGE'].describe())
print()

# Attorney Type (KEY VARIABLE)
print("4. ATTORNEY TYPE (TYPEMONY) - KEY VARIABLE:")
print(df['TYPEMONY'].value_counts().sort_index())
print(f"   Missing: {df['TYPEMONY'].isna().sum()}")
print()

# Criminal History
print("5. CRIMINAL HISTORY CATEGORY (CRIMHIST):")
print(df['CRIMHIST'].value_counts().sort_index())
print(f"   Missing: {df['CRIMHIST'].isna().sum()}")
print()

# Sentence outcomes
print("6. PRISON SENTENCE (PRISDUM):")
print(df['PRISDUM'].value_counts())
print(f"   Missing: {df['PRISDUM'].isna().sum()}")
print()

print("7. TOTAL SENTENCE LENGTH (SENTTOT) - in months:")
print(df['SENTTOT'].describe())
print()

# Sentence relative to guidelines
print("8. SENTENCE RELATIVE TO GUIDELINES (SENTIMP):")
print(df['SENTIMP'].value_counts().sort_index())
print(f"   Missing: {df['SENTIMP'].isna().sum()}")
print()

# Create summary statistics file
print("=" * 80)
print("GENERATING SUMMARY STATISTICS")
print("=" * 80)
print()

summary = df.describe(include='all').T
summary.to_csv(OUTPUT_DIR / 'descriptive_statistics.csv')
print(f"✓ Saved: {OUTPUT_DIR / 'descriptive_statistics.csv'}")
print()

# Bivariate analysis: Race x Attorney Type
print("=" * 80)
print("BIVARIATE ANALYSIS: RACE × ATTORNEY TYPE")
print("=" * 80)
print()

if df['NEWRACE'].notna().sum() > 0 and df['TYPEMONY'].notna().sum() > 0:
    crosstab = pd.crosstab(
        df['NEWRACE'],
        df['TYPEMONY'],
        margins=True,
        normalize='index'
    )
    print(crosstab.round(3))
    print()
    crosstab.to_csv(OUTPUT_DIR / 'race_attorney_crosstab.csv')
    print(f"✓ Saved: {OUTPUT_DIR / 'race_attorney_crosstab.csv'}")
    print()

# Bivariate: Attorney Type x Sentence Outcome
print("=" * 80)
print("BIVARIATE ANALYSIS: ATTORNEY TYPE × PRISON SENTENCE")
print("=" * 80)
print()

if df['TYPEMONY'].notna().sum() > 0 and df['PRISDUM'].notna().sum() > 0:
    crosstab2 = pd.crosstab(
        df['TYPEMONY'],
        df['PRISDUM'],
        margins=True,
        normalize='index'
    )
    print(crosstab2.round(3))
    print()
    crosstab2.to_csv(OUTPUT_DIR / 'attorney_prison_crosstab.csv')
    print(f"✓ Saved: {OUTPUT_DIR / 'attorney_prison_crosstab.csv'}")
    print()

# Sentence length by attorney type
print("=" * 80)
print("SENTENCE LENGTH BY ATTORNEY TYPE")
print("=" * 80)
print()

sent_by_atty = df.groupby('TYPEMONY')['SENTTOT'].describe()
print(sent_by_atty)
print()
sent_by_atty.to_csv(OUTPUT_DIR / 'sentence_by_attorney.csv')
print(f"✓ Saved: {OUTPUT_DIR / 'sentence_by_attorney.csv'}")
print()

# Sentence length by race
print("=" * 80)
print("SENTENCE LENGTH BY RACE")
print("=" * 80)
print()

sent_by_race = df.groupby('NEWRACE')['SENTTOT'].describe()
print(sent_by_race)
print()
sent_by_race.to_csv(OUTPUT_DIR / 'sentence_by_race.csv')
print(f"✓ Saved: {OUTPUT_DIR / 'sentence_by_race.csv'}")
print()

# Create visualizations
print("=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)
print()

# 1. Race distribution
fig, ax = plt.subplots(figsize=(10, 6))
race_counts = df['NEWRACE'].value_counts().sort_index()
race_counts.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Distribution of Cases by Race', fontsize=14, fontweight='bold')
ax.set_xlabel('Race Code', fontsize=12)
ax.set_ylabel('Number of Cases', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'fig1_race_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fig1_race_distribution.png")

# 2. Attorney type distribution
fig, ax = plt.subplots(figsize=(10, 6))
atty_counts = df['TYPEMONY'].value_counts().sort_index()
atty_counts.plot(kind='bar', ax=ax, color='coral')
ax.set_title('Distribution of Attorney Types', fontsize=14, fontweight='bold')
ax.set_xlabel('Attorney Type Code', fontsize=12)
ax.set_ylabel('Number of Cases', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'fig2_attorney_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fig2_attorney_distribution.png")

# 3. Sentence length distribution
fig, ax = plt.subplots(figsize=(10, 6))
df['SENTTOT'].hist(bins=50, ax=ax, color='seagreen', edgecolor='black')
ax.set_title('Distribution of Total Sentence Length', fontsize=14, fontweight='bold')
ax.set_xlabel('Sentence Length (months)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.axvline(df['SENTTOT'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {df["SENTTOT"].median():.0f} months')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'fig3_sentence_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fig3_sentence_distribution.png")

# 4. Sentence by attorney type (boxplot)
fig, ax = plt.subplots(figsize=(10, 6))
df_plot = df[df['SENTTOT'] <= df['SENTTOT'].quantile(0.95)]  # Remove outliers for visualization
df_plot.boxplot(column='SENTTOT', by='TYPEMONY', ax=ax)
ax.set_title('Sentence Length by Attorney Type', fontsize=14, fontweight='bold')
ax.set_xlabel('Attorney Type', fontsize=12)
ax.set_ylabel('Sentence Length (months)', fontsize=12)
plt.suptitle('')  # Remove default title
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'fig4_sentence_by_attorney.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fig4_sentence_by_attorney.png")

# 5. Prison rate by race
fig, ax = plt.subplots(figsize=(10, 6))
prison_by_race = df.groupby('NEWRACE')['PRISDUM'].mean() * 100
prison_by_race.plot(kind='bar', ax=ax, color='darkred')
ax.set_title('Prison Sentence Rate by Race', fontsize=14, fontweight='bold')
ax.set_xlabel('Race Code', fontsize=12)
ax.set_ylabel('Prison Rate (%)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'fig5_prison_rate_by_race.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: fig5_prison_rate_by_race.png")

print()
print("=" * 80)
print("EXPLORATORY ANALYSIS COMPLETE")
print("=" * 80)
print()
print(f"All outputs saved to: {OUTPUT_DIR}")
print()
print("Key Findings:")
print(f"  - Total cases analyzed: {len(df):,}")
print(f"  - Prison sentence rate: {df['PRISDUM'].mean()*100:.1f}%")
print(f"  - Median sentence: {df['SENTTOT'].median():.0f} months")
print(f"  - Mean sentence: {df['SENTTOT'].mean():.1f} months")
print()
print("Next steps:")
print("  1. Data cleaning and recoding")
print("  2. Feature engineering (legal literacy proxies)")
print("  3. Statistical modeling (logistic regression, multilevel models)")
print("  4. Mediation analysis")
print("  5. Fairness metrics evaluation")
