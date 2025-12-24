import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import os

def missingness_heatmap(df, path):
    plt.figure(figsize=(8,4))
    sns.heatmap(df.isnull(), cbar=False)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def before_after_hist(before, after, col, path):
    plt.figure(figsize=(6,4))
    plt.hist(before[col], alpha=0.5, label="Before")
    plt.hist(after[col], alpha=0.5, label="After")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
