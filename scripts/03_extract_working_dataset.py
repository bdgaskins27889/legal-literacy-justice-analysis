#!/usr/bin/env python3
"""
Extract Working Dataset with Correct Variable Names
Author: Barbara D. Gaskins
Date: January 2026

Strategy: Load data in chunks, extract only needed variables, and create a working dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'

print("=" * 80)
print("EXTRACTING WORKING DATASET - LEGAL LITERACY ANALYSIS")
print("=" * 80)
print()

# Correct variable names based on actual CSV columns
SELECTED_VARS = [
    # Demographics
    'NEWRACE',      # Race (recoded)
    'MONRACE',      # Race (monitoring)
    'MONSEX',       # Gender
    'AGE',          # Age at sentencing
    'AGECAT',       # Age category
    'CITIZEN',      # Citizenship status
    'EDUCATN',      # Education level
    'DISTRICT',     # Judicial district
    'CIRCDIST',     # Circuit
    
    # Representation (KEY VARIABLE)
    'TYPEMONY',     # Type of attorney/counsel
    
    # Offense Characteristics
    'NOCOUNTS',     # Number of counts
    'MWGT1',        # Drug weight (primary)
    
    # Criminal History
    'CRIMHIST',     # Criminal History Category (I-VI)
    'CRIMPTS',      # Criminal history points
    'TOTPRISN',     # Total prior prison sentences
    
    # Guideline Range
    'GLMIN',        # Guideline minimum (months)
    'GLMAX',        # Guideline maximum (months)
    'XFOLSOR',      # Final offense level
    
    # Procedural Engagement (Legal Literacy Proxies)
    'ACCAP',        # Acceptance of responsibility applied
    
    # Pretrial Status
    'MONCIRC',      # Monitoring circumstances (detention)
    'PRESENT',      # Presentence status
    
    # Sentencing Outcomes (DEPENDENT VARIABLES)
    'SENTTOT',      # Total sentence (months)
    'PRISDUM',      # Prison sentence indicator
    'PROBDUM',      # Probation indicator
    'PROBATN',      # Probation length (months)
    'FINE',         # Fine amount
    'SENTIMP',      # Sentence imposed relative to guideline
    
    # Case Processing
    'QUARTER',      # Quarter
]

print(f"Selected {len(SELECTED_VARS)} variables")
print()

# Load data with selected columns only
print("Loading data with selected variables...")
print("(This will take 1-2 minutes due to large file size)")
print()

try:
    df = pd.read_csv(
        DATA_DIR / 'opafy24nid.csv',
        usecols=SELECTED_VARS,
        low_memory=False
    )
    
    print(f"✓ Successfully loaded {len(df):,} cases")
    print(f"✓ Variables: {len(df.columns)}")
    print(f"✓ Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print()
    
    # Save immediately to avoid losing data
    output_file = DATA_DIR / 'ussc_fy2024_working.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Saved working dataset: {output_file}")
    print(f"✓ File size: {output_file.stat().st_size / 1024**2:.1f} MB")
    print()
    
    # Quick summary
    print("=" * 80)
    print("QUICK DATA SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Total cases: {len(df):,}")
    print(f"Variables: {len(df.columns)}")
    print()
    
    print("Key Variables:")
    print(f"  - Race (NEWRACE): {df['NEWRACE'].notna().sum():,} non-missing")
    print(f"  - Gender (MONSEX): {df['MONSEX'].notna().sum():,} non-missing")
    print(f"  - Attorney Type (TYPEMONY): {df['TYPEMONY'].notna().sum():,} non-missing")
    print(f"  - Criminal History (CRIMHIST): {df['CRIMHIST'].notna().sum():,} non-missing")
    print(f"  - Total Sentence (SENTTOT): {df['SENTTOT'].notna().sum():,} non-missing")
    print(f"  - Prison Indicator (PRISDUM): {df['PRISDUM'].notna().sum():,} non-missing")
    print()
    
    # Missing data overview
    print("Missing Data Overview:")
    missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)
    print(missing_pct.head(10))
    print()
    
    print("=" * 80)
    print("SUCCESS - Working dataset created!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Exploratory data analysis")
    print("2. Data cleaning and recoding")
    print("3. Feature engineering")
    print("4. Statistical modeling")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
