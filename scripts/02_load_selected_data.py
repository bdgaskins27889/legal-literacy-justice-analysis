#!/usr/bin/env python3
"""
Load Selected Variables from USSC FY 2024 Dataset
Author: Barbara D. Gaskins
Date: January 2026

This script loads only the essential variables needed for the legal literacy analysis,
avoiding memory issues from loading all 27,000+ variables.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'

print("=" * 80)
print("LOADING SELECTED VARIABLES FROM USSC FY 2024 DATASET")
print("=" * 80)
print()

# Define selected variables based on codebook review
SELECTED_VARS = [
    # Demographics
    'NEWRACE',      # Race (recoded)
    'MONSEX',       # Gender
    'AGE',          # Age at sentencing
    'AGECAT',       # Age category
    'CITIZEN',      # Citizenship status
    'EDUCATN',      # Education level
    'DISTRICT',     # Judicial district
    'CIRCDIST',     # Circuit
    
    # Representation (KEY VARIABLE)
    'DEFCONSL',     # Type of defense counsel
    
    # Offense Characteristics
    'OFFTYPE2',     # Primary offense type
    'NOCOUNTS',     # Number of counts
    'MWGT1',        # Drug weight
    
    # Criminal History
    'CRIMHIST',     # Criminal History Category (I-VI)
    'CRIMPTS',      # Criminal history points
    'PRISOR',       # Prior incarceration
    'TOTPRISN',     # Total prior prison sentences
    'TOTPROB',      # Total prior probation sentences
    
    # Guideline Range
    'GLMIN',        # Guideline minimum (months)
    'GLMAX',        # Guideline maximum (months)
    'XFOLSOR',      # Final offense level
    
    # Procedural Engagement (Legal Literacy Proxies)
    'TRIAL',        # Trial indicator
    'ACCAP',        # Acceptance of responsibility applied
    'SAFE5C1',      # Safety valve
    'DEPART',       # Departure indicator
    'BOOKER4',      # Post-Booker variance
    
    # Pretrial Status
    'MONCIRC',      # Monitoring circumstances (detention)
    'PRESENT',      # Presentence status
    
    # Sentencing Outcomes (DEPENDENT VARIABLES)
    'SENTTOT',      # Total sentence (months)
    'PRISDUM',      # Prison sentence indicator
    'PRISON',       # Prison sentence length (months)
    'PROBDUM',      # Probation indicator
    'PROBATION',    # Probation length (months)
    'FINE',         # Fine amount
    'SENTIMP',      # Sentence imposed relative to guideline
    
    # Departure/Variance Details
    'REASON1',      # Primary reason for departure
    'NOREAS',       # No reason for departure
    
    # Case Processing
    'SENTDATE',     # Sentencing date
    'SENTYR',       # Sentencing year
    'QUARTER',      # Quarter
]

print(f"Selected {len(SELECTED_VARS)} variables for analysis")
print()

# Try to load with selected columns
print("Loading data (this may take a moment)...")
try:
    df = pd.read_csv(
        DATA_DIR / 'opafy24nid.csv',
        usecols=SELECTED_VARS,
        low_memory=False
    )
    print(f"✓ Successfully loaded {len(df):,} cases")
    print(f"✓ Dataset shape: {df.shape}")
    print(f"✓ Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    print("\nAttempting to identify available variables...")
    # Load just the header
    header_df = pd.read_csv(DATA_DIR / 'opafy24nid.csv', nrows=0)
    available_vars = header_df.columns.tolist()
    
    # Check which variables are available
    missing_vars = [v for v in SELECTED_VARS if v not in available_vars]
    if missing_vars:
        print(f"\n⚠ Missing variables ({len(missing_vars)}):")
        for var in missing_vars:
            print(f"  - {var}")
        
        # Load only available variables
        available_selected = [v for v in SELECTED_VARS if v in available_vars]
        print(f"\nLoading {len(available_selected)} available variables...")
        df = pd.read_csv(
            DATA_DIR / 'opafy24nid.csv',
            usecols=available_selected,
            low_memory=False
        )
        print(f"✓ Successfully loaded {len(df):,} cases")
        print(f"✓ Dataset shape: {df.shape}")

print()
print("=" * 80)
print("INITIAL DATA SUMMARY")
print("=" * 80)
print()

# Display first few rows
print("First 5 rows:")
print(df.head())
print()

# Basic statistics
print("Variable Types:")
print(df.dtypes.value_counts())
print()

print("Missing Data Summary:")
missing_summary = pd.DataFrame({
    'Variable': df.columns,
    'Missing_Count': df.isna().sum(),
    'Missing_Percent': (df.isna().sum() / len(df) * 100).round(2)
}).sort_values('Missing_Percent', ascending=False)
print(missing_summary.head(20))
print()

# Key variable distributions
print("=" * 80)
print("KEY VARIABLE DISTRIBUTIONS")
print("=" * 80)
print()

if 'NEWRACE' in df.columns:
    print("Race Distribution (NEWRACE):")
    print(df['NEWRACE'].value_counts().sort_index())
    print()

if 'MONSEX' in df.columns:
    print("Gender Distribution (MONSEX):")
    print(df['MONSEX'].value_counts())
    print()

if 'DEFCONSL' in df.columns:
    print("Defense Counsel Type (DEFCONSL):")
    print(df['DEFCONSL'].value_counts().sort_index())
    print()

if 'CRIMHIST' in df.columns:
    print("Criminal History Category (CRIMHIST):")
    print(df['CRIMHIST'].value_counts().sort_index())
    print()

if 'PRISDUM' in df.columns:
    print("Prison Sentence Indicator (PRISDUM):")
    print(df['PRISDUM'].value_counts())
    print()

# Save processed dataset
print("=" * 80)
print("SAVING PROCESSED DATASET")
print("=" * 80)
print()

output_file = DATA_DIR / 'ussc_fy2024_selected.csv'
df.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")
print(f"✓ File size: {output_file.stat().st_size / 1024**2:.1f} MB")
print()

# Save variable list
var_list_file = OUTPUT_DIR / 'selected_variables_list.txt'
with open(var_list_file, 'w') as f:
    f.write("Selected Variables for Legal Literacy Analysis\n")
    f.write("=" * 60 + "\n\n")
    for i, var in enumerate(df.columns, 1):
        f.write(f"{i:2d}. {var}\n")
print(f"✓ Variable list saved to: {var_list_file}")

print()
print("=" * 80)
print("DATA LOADING COMPLETE")
print("=" * 80)
print(f"\nNext steps:")
print("1. Review variable distributions")
print("2. Perform data cleaning and recoding")
print("3. Create derived variables (legal literacy proxies)")
print("4. Conduct exploratory data analysis")
