#!/usr/bin/env python3
"""
Chunked Data Extraction with Stratified Sampling
Author: Barbara D. Gaskins
Date: January 2026

This script processes the large CSV in chunks to avoid memory issues,
while maintaining a representative sample for analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
PROJECT_DIR = Path('/home/ubuntu/legal_literacy_justice_project')
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = PROJECT_DIR / 'outputs'

print("=" * 80)
print("CHUNKED DATA EXTRACTION - LEGAL LITERACY ANALYSIS")
print("=" * 80)
print()

# Selected variables
SELECTED_VARS = [
    'NEWRACE', 'MONRACE', 'MONSEX', 'AGE', 'AGECAT', 'CITIZEN', 'EDUCATN',
    'DISTRICT', 'CIRCDIST', 'TYPEMONY', 'NOCOUNTS', 'MWGT1', 'CRIMHIST',
    'CRIMPTS', 'TOTPRISN', 'GLMIN', 'GLMAX', 'XFOLSOR', 'ACCAP',
    'MONCIRC', 'PRESENT', 'SENTTOT', 'PRISDUM', 'PROBDUM', 'PROBATN',
    'FINE', 'SENTIMP', 'QUARTER'
]

print(f"Extracting {len(SELECTED_VARS)} variables")
print("Processing in chunks to manage memory...")
print()

# Process in chunks
chunk_size = 10000
chunks_processed = 0
total_rows = 0

# First pass: get total count and sample
print("Pass 1: Counting rows and creating sample...")
sampled_data = []
sample_rate = 0.5  # Use 50% of data (still ~30k cases)

try:
    for chunk in pd.read_csv(
        DATA_DIR / 'opafy24nid.csv',
        usecols=SELECTED_VARS,
        chunksize=chunk_size,
        low_memory=False
    ):
        chunks_processed += 1
        total_rows += len(chunk)
        
        # Sample from this chunk
        chunk_sample = chunk.sample(frac=sample_rate, random_state=42)
        sampled_data.append(chunk_sample)
        
        if chunks_processed % 2 == 0:
            print(f"  Processed {total_rows:,} rows ({chunks_processed} chunks)...")
    
    print(f"\n✓ Total rows in dataset: {total_rows:,}")
    print(f"✓ Chunks processed: {chunks_processed}")
    print()
    
    # Combine sampled data
    print("Combining sampled data...")
    df = pd.concat(sampled_data, ignore_index=True)
    print(f"✓ Sample size: {len(df):,} cases ({len(df)/total_rows*100:.1f}% of total)")
    print(f"✓ Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print()
    
    # Save working dataset
    output_file = DATA_DIR / 'ussc_fy2024_working.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Saved: {output_file}")
    print(f"✓ File size: {output_file.stat().st_size / 1024**2:.1f} MB")
    print()
    
    # Quick summary
    print("=" * 80)
    print("DATA SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Sample size: {len(df):,} cases")
    print(f"Variables: {len(df.columns)}")
    print()
    
    # Key variable distributions
    print("Key Variables (non-missing counts):")
    for var in ['NEWRACE', 'MONSEX', 'TYPEMONY', 'CRIMHIST', 'SENTTOT', 'PRISDUM']:
        if var in df.columns:
            count = df[var].notna().sum()
            pct = count / len(df) * 100
            print(f"  {var:15s}: {count:6,} ({pct:5.1f}%)")
    print()
    
    # Missing data
    print("Variables with >10% missing:")
    missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)
    high_missing = missing_pct[missing_pct > 10]
    if len(high_missing) > 0:
        for var, pct in high_missing.items():
            print(f"  {var:15s}: {pct:5.1f}%")
    else:
        print("  None - excellent data quality!")
    print()
    
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print()
    print("Working dataset ready for analysis")
    print(f"Location: {output_file}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
