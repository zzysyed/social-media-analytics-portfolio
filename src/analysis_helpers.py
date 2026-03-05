# src/analysis_helpers.py
# Reusable functions for any data analysis project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="darkgrid", palette="muted")


# ══════════════════════════════════════════════════════════════════
# 1.  DATA LOADING & EXPLORATION
# ══════════════════════════════════════════════════════════════════

def load_and_explore(filepath, parse_dates=None, verbose=True):
    """Load a CSV and print a compact exploration summary."""
    df = pd.read_csv(filepath, parse_dates=parse_dates)
    if verbose:
        print("=" * 55)
        print(f"📂 File     : {filepath}")
        print(f"📐 Shape    : {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"📋 Columns  : {df.columns.tolist()}")
        print(f"\n🔍 Data Types:\n{df.dtypes.to_string()}")
        print(f"\n❓ Missing Values:")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        print(missing.to_string() if len(missing) else "  None ✅")
        print(f"\n📊 Numeric Summary:")
        print(df.describe().round(2).to_string())
        print("=" * 55)
    return df


def data_quality_report(df):
    """Return a DataFrame summarising data quality for every column."""
    report = pd.DataFrame({
        'dtype':          df.dtypes,
        'null_count':     df.isnull().sum(),
        'null_pct':       (df.isnull().sum() / len(df) * 100).round(2),
        'unique_values':  df.nunique(),
        'sample_value':   [df[c].dropna().iloc[0] if df[c].dropna().shape[0] > 0 else None
                           for c in df.columns],
    })
    print("\n📋 Data Quality Report:")
    print(report.to_string())
    return report


# ══════════════════════════════════════════════════════════════════
# 2.  DATA CLEANING
# ══════════════════════════════════════════════════════════════════

def fill_missing_by_group(df, columns, group_col, strategy='median'):
    """
    Fill missing values in `columns` using group-level median or mean.

    Parameters
    ----------
    df         : DataFrame
    columns    : list of column names to fill
    group_col  : column to group by (e.g. 'platform')
    strategy   : 'median' or 'mean'
    """
    df = df.copy()
    for col in columns:
        before = df[col].isnull().sum()
        if strategy == 'median':
            df[col] = df.groupby(group_col)[col].transform(
                lambda x: x.fillna(x.median()))
        else:
            df[col] = df.groupby(group_col)[col].transform(
                lambda x: x.fillna(x.mean()))
        after = df[col].isnull().sum()
        print(f"  ✅ '{col}': filled {before - after} values using {strategy} of '{group_col}'")
    return df


def remove_outliers_iqr(df, column, multiplier=1.5):
    """Remove rows where column value is beyond IQR bounds."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - multiplier * IQR, Q3 + multiplier * IQR
    original = len(df)
    df_clean = df[(df[column] >= lower) & (df[column] <= upper)]
    print(f"  🧹 '{column}': removed {original - len(df_clean)} outliers "
          f"(bounds: {lower:.2f} – {upper:.2f})")
    return df_clean


def standardise_column_names(df):
    """Lowercase, strip spaces, replace spaces with underscores."""
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    print(f"  ✅ Column names standardised: {df.columns.tolist()}")
    return df


# ══════════════════════════════════════════════════════════════════
# 3.  STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════════════

def descriptive_stats(df, columns):
    """Return extended descriptive stats for the given columns."""
    stats = df[columns].agg(['mean', 'median', 'std', 'min', 'max',
                              lambda x: x.quantile(0.25),
                              lambda x: x.quantile(0.75)]).T
    stats.columns = ['mean', 'median', 'std', 'min', 'max', 'Q1', 'Q3']
    stats['IQR']  = stats['Q3'] - stats['Q1']
    stats['CV%']  = (stats['std'] / stats['mean'] * 100).round(2)
    print("\n📊 Descriptive Statistics:")
    print(stats.round(4).to_string())
    return stats.round(4)


def group_stats(df, group_col, value_col, funcs=None):
    """
    Aggregate value_col by group_col.

    Returns sorted DataFrame with count, mean, median, std, sum.
    """
    if funcs is None:
        funcs = ['count', 'mean', 'median', 'std', 'sum']
    result = df.groupby(group_col)[value_col].agg(funcs).round(4)
    result = result.sort_values('mean', ascending=False)
    print(f"\n📊 '{value_col}' grouped by '{group_col}':")
    print(result.to_string())
    return result


def correlation_summary(df, target_col, numeric_cols=None):
    """Print correlations of all numeric columns with target_col."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    corr = df[numeric_cols].corr()[target_col].drop(target_col).sort_values(
        key=abs, ascending=False)
    print(f"\n🔗 Correlations with '{target_col}':")
    for col, val in corr.items():
        bar  = '█' * int(abs(val) * 20)
        sign = '+' if val > 0 else '-'
        print(f"  {sign} {col:<25} {val:+.4f}  {bar}")
    return corr


# ══════════════════════════════════════════════════════════════════
# 4.  VISUALISATION HELPERS
# ══════════════════════════════════════════════════════════════════

def save_fig(fig, filename, viz_dir='../visualizations', dpi=150):
    """Save a matplotlib figure and print confirmation."""
    os.makedirs(viz_dir, exist_ok=True)
    path = os.path.join(viz_dir, filename)
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    print(f"  💾 Saved → {path}")
    return path


def plot_bar(df, x_col, y_col, title='', color='#4ECDC4',
             rotate_x=0, save_as=None, viz_dir='../visualizations'):
    """Quick horizontal or vertical bar chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df[x_col], df[y_col], color=color, edgecolor='white')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.tick_params(axis='x', rotation=rotate_x)
    plt.tight_layout()
    if save_as:
        save_fig(fig, save_as, viz_dir)
    plt.show()
    return fig


def plot_line(df, x_col, y_col, title='', color='#FF6B6B',
              fill=True, save_as=None, viz_dir='../visualizations'):
    """Quick line chart with optional fill."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df[x_col], df[y_col], marker='o', color=color,
            linewidth=2.5, markersize=7)
    if fill:
        ax.fill_between(df[x_col], df[y_col], alpha=0.15, color=color)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.tight_layout()
    if save_as:
        save_fig(fig, save_as, viz_dir)
    plt.show()
    return fig


def plot_correlation_heatmap(df, columns=None, title='Correlation Matrix',
                              save_as=None, viz_dir='../visualizations'):
    """Triangular correlation heatmap."""
    if columns:
        df = df[columns]
    corr = df.select_dtypes(include=np.number).corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', center=0, ax=ax,
                linewidths=0.5, square=True)
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_as:
        save_fig(fig, save_as, viz_dir)
    plt.show()
    return fig


def plot_top_n(df, group_col, value_col, n=10, title='',
               horizontal=True, save_as=None, viz_dir='../visualizations'):
    """Bar chart of top-N groups by value_col mean."""
    top = (df.groupby(group_col)[value_col]
             .mean()
             .sort_values(ascending=horizontal)
             .tail(n))
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, n))
    if horizontal:
        ax.barh(top.index, top.values, color=colors)
        ax.set_xlabel(value_col)
    else:
        ax.bar(top.index, top.values, color=colors)
        ax.set_ylabel(value_col)
        ax.tick_params(axis='x', rotation=30)
    ax.set_title(title or f'Top {n} {group_col} by {value_col}',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_as:
        save_fig(fig, save_as, viz_dir)
    plt.show()
    return fig


# ══════════════════════════════════════════════════════════════════
# 5.  REPORTING HELPERS
# ══════════════════════════════════════════════════════════════════

def print_summary(title, stats_dict):
    """Pretty-print a dictionary of stats."""
    width = 55
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)
    for key, val in stats_dict.items():
        print(f"  {key:<30} {val}")
    print("=" * width)


def top_n_values(df, group_col, value_col, n=5, agg='mean'):
    """Return top-N values as a formatted string for reports."""
    top = (df.groupby(group_col)[value_col]
             .agg(agg)
             .sort_values(ascending=False)
             .head(n))
    lines = [f"  {i+1}. {k}: {v:.4f}" for i, (k, v) in enumerate(top.items())]
    return '\n'.join(lines)