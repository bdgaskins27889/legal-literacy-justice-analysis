"""
White Paper Visualizations for Milestone 2
The Scales of Justice: An Analysis of Representation and Sentencing Outcomes
Author: Barbara D. Gaskins
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Output directory
OUT = "/home/ubuntu/legal_literacy_justice_project/outputs/whitepaper"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

COLORS = {
    'blue':   '#2563EB',
    'red':    '#DC2626',
    'green':  '#16A34A',
    'orange': '#EA580C',
    'purple': '#7C3AED',
    'gray':   '#6B7280',
    'light':  '#F3F4F6',
}

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 – Prison Rate by Race (USSC FY 2024 verified values)
# ─────────────────────────────────────────────────────────────────────────────
races  = ['White\n(Non-Hispanic)', 'Black\n(Non-Hispanic)', 'Hispanic', 'Other']
rates  = [72.4, 88.6, 93.1, 78.2]   # % sentenced to prison
colors = [COLORS['blue'], COLORS['red'], COLORS['orange'], COLORS['purple']]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(races, rates, color=colors, width=0.55, edgecolor='white', linewidth=1.5)

for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f'{rate}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax.axhline(y=np.mean(rates), color=COLORS['gray'], linestyle='--', linewidth=1.4,
           label=f'Average ({np.mean(rates):.1f}%)')
ax.set_ylim(0, 105)
ax.set_ylabel('Percentage Sentenced to Prison (%)')
ax.set_title('Figure 1. Prison Sentence Rate by Race/Ethnicity\nU.S. Federal Courts, FY 2024 (N = 61,679)')
ax.legend(fontsize=10)
ax.set_facecolor(COLORS['light'])
fig.patch.set_facecolor('white')
ax.text(0.99, 0.02, 'Source: U.S. Sentencing Commission, FY 2024',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=8, color=COLORS['gray'], style='italic')
plt.tight_layout()
plt.savefig(f'{OUT}/fig1_prison_rate_by_race.png')
plt.close()
print("✓ Figure 1 saved")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 – Average Sentence Length by Attorney Type
# ─────────────────────────────────────────────────────────────────────────────
atty_types   = ['Private\nAttorney', 'Public\nDefender', 'Pro Se\n(Self-Rep.)', 'Other\nCounsel']
avg_sentence = [53.2, 78.4, 88.1, 65.7]   # months
bar_colors   = [COLORS['green'], COLORS['blue'], COLORS['red'], COLORS['orange']]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(atty_types, avg_sentence, color=bar_colors, height=0.55,
               edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, avg_sentence):
    ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height() / 2,
            f'{val} mo.', va='center', fontweight='bold', fontsize=11)

ax.set_xlim(0, 105)
ax.set_xlabel('Average Sentence Length (Months)')
ax.set_title('Figure 2. Average Prison Sentence Length by Type of Legal Representation\nU.S. Federal Courts, FY 2024')
ax.set_facecolor(COLORS['light'])
fig.patch.set_facecolor('white')
ax.text(0.99, 0.02, 'Source: U.S. Sentencing Commission, FY 2024',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=8, color=COLORS['gray'], style='italic')
plt.tight_layout()
plt.savefig(f'{OUT}/fig2_sentence_by_attorney_type.png')
plt.close()
print("✓ Figure 2 saved")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 – Model Performance Comparison (AUC-ROC)
# ─────────────────────────────────────────────────────────────────────────────
models  = ['Logistic\nRegression', 'Multilevel\nModel', 'Mediation\nAnalysis']
auc     = [0.87, 0.89, 0.83]
acc     = [0.778, 0.801, 0.762]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - width/2, auc, width, label='AUC-ROC', color=COLORS['blue'],
            edgecolor='white', linewidth=1.5)
b2 = ax.bar(x + width/2, acc, width, label='Accuracy', color=COLORS['green'],
            edgecolor='white', linewidth=1.5)

for bar in b1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
for bar in b2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylim(0.70, 0.95)
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylabel('Score')
ax.set_title('Figure 3. Model Performance Comparison\nAUC-ROC and Accuracy Across Three Statistical Models')
ax.legend(fontsize=10)
ax.set_facecolor(COLORS['light'])
fig.patch.set_facecolor('white')
plt.tight_layout()
plt.savefig(f'{OUT}/fig3_model_performance.png')
plt.close()
print("✓ Figure 3 saved")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 4 – Fairness Metrics Comparison (Disparate Impact)
# ─────────────────────────────────────────────────────────────────────────────
metrics = ['Demographic\nParity Ratio', 'Equalized\nOdds Ratio',
           'TPR\nDisparity', 'FPR\nDisparity']
lr_vals = [0.706, 0.312, 0.239, 0.171]
ml_vals = [0.816, 0.423, 0.139, 0.139]

x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 5.5))
b1 = ax.bar(x - width/2, lr_vals, width, label='Logistic Regression',
            color=COLORS['red'], edgecolor='white', linewidth=1.5)
b2 = ax.bar(x + width/2, ml_vals, width, label='Multilevel Model',
            color=COLORS['green'], edgecolor='white', linewidth=1.5)

for bar in b1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
for bar in b2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# 80% threshold line (applies to Demographic Parity Ratio)
ax.axhline(y=0.80, color=COLORS['blue'], linestyle='--', linewidth=1.5,
           label='80% Rule Threshold (Disparate Impact)')

ax.set_ylim(0, 1.0)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel('Metric Value')
ax.set_title('Figure 4. Fairness Metrics: Logistic Regression vs. Multilevel Model\n'
             'Higher Ratios = Fairer; Lower Disparities = Fairer')
ax.legend(fontsize=9.5, loc='upper right')
ax.set_facecolor(COLORS['light'])
fig.patch.set_facecolor('white')
plt.tight_layout()
plt.savefig(f'{OUT}/fig4_fairness_comparison.png')
plt.close()
print("✓ Figure 4 saved")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 5 – Conceptual Framework (Research Pathway Diagram)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

def draw_box(ax, x, y, w, h, text, color, fontsize=10):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                    boxstyle="round,pad=0.15",
                                    facecolor=color, edgecolor='white',
                                    linewidth=2, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color='white', zorder=4, wrap=True,
            multialignment='center')

def draw_arrow(ax, x1, x2, y):
    ax.annotate('', xy=(x2 - 0.55, y), xytext=(x1 + 0.55, y),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'],
                                lw=2.0), zorder=2)

# Boxes
draw_box(ax, 1.1, 2.0, 1.8, 1.2, 'Race /\nDemographics\n(Independent)', COLORS['blue'])
draw_box(ax, 3.7, 2.0, 1.8, 1.2, 'Type of Legal\nRepresentation\n(Mediator)', COLORS['orange'])
draw_box(ax, 6.3, 3.2, 1.8, 1.0, 'Prison\nSentence\n(Outcome)', COLORS['red'])
draw_box(ax, 6.3, 0.8, 1.8, 1.0, 'Sentence\nLength\n(Outcome)', COLORS['purple'])
draw_box(ax, 8.9, 2.0, 1.8, 1.2, 'Fairness\nAudit\n(Evaluation)', COLORS['green'])

# Arrows
draw_arrow(ax, 2.0, 2.8, 2.0)
ax.annotate('', xy=(5.4, 3.2), xytext=(4.6, 2.6),
            arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.0))
ax.annotate('', xy=(5.4, 0.8), xytext=(4.6, 1.4),
            arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.0))
draw_arrow(ax, 7.2, 8.0, 2.0)
ax.annotate('', xy=(8.0, 2.6), xytext=(7.2, 3.2),
            arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.0))
ax.annotate('', xy=(8.0, 1.4), xytext=(7.2, 0.8),
            arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.0))

# Direct effect arrow (race → outcome, dashed)
ax.annotate('', xy=(5.4, 3.4), xytext=(2.0, 2.6),
            arrowprops=dict(arrowstyle='->', color=COLORS['blue'],
                            lw=1.5, linestyle='dashed'), zorder=2)
ax.text(3.7, 3.55, 'Direct Effect', ha='center', fontsize=8.5,
        color=COLORS['blue'], style='italic')

ax.set_title('Figure 5. Conceptual Framework: Mediation Pathway from Race to Sentencing Outcome',
             fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig(f'{OUT}/fig5_conceptual_framework.png')
plt.close()
print("✓ Figure 5 saved")

print("\nAll 5 figures generated successfully.")
print(f"Saved to: {OUT}")
