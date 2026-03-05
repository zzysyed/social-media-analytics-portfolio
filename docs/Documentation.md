# Technical Documentation
## Social Media Analytics Portfolio — 2024

---

## 1. Project Overview

This project performs a full data analysis on 2,000 simulated social media posts across five major platforms (Instagram, Twitter, Facebook, YouTube, TikTok) covering January to December 2024.

The goal is to identify engagement patterns, optimal posting strategies, and actionable business insights using Python-based data analysis tools.

---

## 2. Dataset Description

### Source
Simulated dataset generated via `data/generate_dataset.py` using realistic platform-specific engagement multipliers.

### Features (18 columns)

| Column | Type | Description |
|--------|------|-------------|
| post_id | string | Unique post identifier |
| account | string | Account handle (@user_001 etc.) |
| platform | string | Instagram / Twitter / Facebook / YouTube / TikTok |
| content_type | string | Video / Image / Text / Story / Reel / Poll |
| category | string | Tech / Fashion / Food / Travel / Fitness / Education / Entertainment / Business |
| post_date | datetime | Full timestamp of post |
| day_of_week | string | Monday through Sunday |
| hour_of_day | int | 0–23 |
| month | int | 1–12 |
| likes | int | Number of likes (5% missing injected) |
| comments | int | Number of comments (5% missing injected) |
| shares | int | Number of shares (5% missing injected) |
| views | int | Number of views |
| followers | int | Account follower count |
| engagement_rate | float | (likes+comments+shares) / followers × 100 |
| hashtag_count | int | Number of hashtags used (5% missing injected) |
| has_emoji | bool | Whether post contains emoji |
| post_length | int | Character length of post caption |

### Missing Values
Approximately 5% of values in `likes`, `comments`, `shares`, and `hashtag_count` are randomly set to NaN to simulate real-world data quality issues. These are imputed using per-platform median values during cleaning.

---

## 3. Analysis Pipeline

### Step 1 — Data Generation
```bash
python data/generate_dataset.py
```
Generates `data/social_media_data.csv` with 2,000 rows.

### Step 2 — Notebook Analysis
Run `notebooks/social_media_analysis.ipynb` cell by cell:

| Cell | Purpose |
|------|---------|
| 1 | Imports and configuration |
| 2 | Load and explore dataset |
| 3 | Data cleaning and feature engineering |
| 4 | Platform performance analysis |
| 5 | Content type analysis |
| 6 | Posting time heatmap |
| 7 | Monthly trends |
| 8 | Hashtag and emoji impact |
| 9 | Category performance |
| 10 | Correlation analysis |
| 11 | Executive summary |
| 12 | Reusable helper functions demo |

### Step 3 — PDF Report
```bash
cd src && python generate_report.py
```
Outputs `reports/social_media_report.pdf` (11 pages).

### Step 4 — Interactive Dashboard
```bash
cd src && python dashboard.py
```
Outputs `reports/dashboard.html` with 9 interactive charts.

---

## 4. Reusable Helper Functions (`src/analysis_helpers.py`)

### Data Loading
```python
load_and_explore(filepath, parse_dates=None)
data_quality_report(df)
```

### Data Cleaning
```python
fill_missing_by_group(df, columns, group_col, strategy='median')
remove_outliers_iqr(df, column, multiplier=1.5)
standardise_column_names(df)
```

### Statistical Analysis
```python
descriptive_stats(df, columns)
group_stats(df, group_col, value_col)
correlation_summary(df, target_col)
```

### Visualisation
```python
save_fig(fig, filename)
plot_bar(df, x_col, y_col, title)
plot_line(df, x_col, y_col, title)
plot_correlation_heatmap(df, columns)
plot_top_n(df, group_col, value_col, n=10)
```

### Reporting
```python
print_summary(title, stats_dict)
top_n_values(df, group_col, value_col, n=5)
```

---

## 5. Key Formulas

### Engagement Rate
```
Engagement Rate (%) = (Likes + Comments + Shares) / Followers × 100
```

### Total Engagement
```
Total Engagement = Likes + Comments + Shares
```

### IQR Outlier Bounds
```
Lower = Q1 - 1.5 × IQR
Upper = Q3 + 1.5 × IQR
```

---

## 6. Platform-Specific Multipliers (Dataset Generation)

| Platform | Likes | Comments | Shares | Views |
|----------|-------|----------|--------|-------|
| TikTok | 3.5× | 1.2× | 2.8× | 10.0× |
| Instagram | 2.0× | 0.8× | 0.5× | 3.0× |
| YouTube | 1.5× | 1.5× | 1.0× | 8.0× |
| Twitter | 1.0× | 2.0× | 3.0× | 2.0× |
| Facebook | 1.2× | 1.0× | 2.0× | 1.5× |

---

## 7. Dependencies

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.13
plotly>=5.15
reportlab>=4.0
jupyter>=1.0
ipykernel>=6.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 8. Quality Standards Met

- [x] Missing value handling (median imputation by group)
- [x] Feature engineering (total_engagement, post_hour_category, month_name)
- [x] Statistical analysis (mean, median, correlation, IQR)
- [x] 8 professional visualisations (3+ types)
- [x] PDF report with executive summary
- [x] Interactive dashboard
- [x] Reusable code in src/ module
- [x] GitHub repository with documentation
- [x] Business insights and recommendations

---
## 9. Screenshots

<img width="1913" height="736" alt="image" src="https://github.com/user-attachments/assets/35d9ad61-83a8-4ee5-9264-df6021de72b6" />

<img width="1919" height="735" alt="image" src="https://github.com/user-attachments/assets/53f53726-7960-41c1-9494-08d4a83bf9f8" />

<img width="1919" height="713" alt="image" src="https://github.com/user-attachments/assets/6dd4bc71-911a-48ae-ad8d-ec4cefe9afba" />


*Documentation version 1.0 — March 2026*
