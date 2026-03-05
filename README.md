# 📊 Social Media Analytics Portfolio — 2024

> A complete data analysis project examining 2,000 social media posts across 5 platforms to uncover engagement patterns and actionable business insights.

---

## 🎯 Project Summary

| Item | Detail |
|------|--------|
| **Domain** | Social Media Analytics |
| **Dataset** | 2,000 posts · 18 features · Jan–Dec 2024 |
| **Platforms** | Instagram · Twitter · Facebook · YouTube · TikTok |
| **Tools** | Python · Pandas · Matplotlib · Seaborn · Plotly · ReportLab |

---

## 🏆 Key Findings

- **TikTok** achieves the highest average engagement rate across all platforms
- **Video** content outperforms all other content formats
- **Saturday at 17:00** is the optimal posting time for maximum reach
- Posts with **6–10 hashtags** hit the engagement sweet spot
- Including **emojis** boosts engagement by approximately 12%
- **Tech and Fitness** are the highest performing content categories

---

## 📁 Project Structure

```
social-media-analytics-portfolio/
│
├── data/
│   ├── generate_dataset.py        ← Generates 2,000-row dataset
│   └── social_media_data.csv      ← Main dataset (18 features)
│
├── notebooks/
│   └── social_media_analysis.ipynb ← Full analysis (12 cells)
│
├── src/
│   ├── analysis_helpers.py        ← Reusable analysis functions
│   ├── generate_report.py         ← PDF report generator
│   ├── dashboard.py               ← Interactive Plotly dashboard
│   └── __init__.py                ← Package initialiser
│
├── visualizations/
│   ├── 01_platform_performance.png
│   ├── 02_content_type_analysis.png
│   ├── 03_posting_time_heatmap.png
│   ├── 04_monthly_trends.png
│   ├── 05_hashtag_emoji_analysis.png
│   ├── 06_category_performance.png
│   ├── 07_correlation_matrix.png
│   └── 08_top_categories.png
│
├── reports/
│   ├── social_media_report.pdf    ← 11-page professional PDF
│   └── dashboard.html             ← Interactive Plotly dashboard
│
├── docs/
│   └── documentation.md           ← Full technical documentation
│
├── presentation/
│   └── social_media_presentation.pptx ← 10-slide deck
│
├── README.md
└── requirements.txt
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/social-media-analytics-portfolio.git
cd social-media-analytics-portfolio
```

### 2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the dataset
```bash
python data/generate_dataset.py
```

### 5. Run the analysis notebook
```bash
jupyter notebook notebooks/social_media_analysis.ipynb
```

### 6. Generate the PDF report
```bash
cd src
python generate_report.py
```

### 7. Launch the interactive dashboard
```bash
python dashboard.py
cd ..
start reports/dashboard.html   # Windows
open reports/dashboard.html    # Mac
```

---

## 📊 Visualisations

| # | Chart | Description |
|---|-------|-------------|
| 1 | Platform Performance | Engagement, views, likes by platform |
| 2 | Content Type Analysis | Performance by content format |
| 3 | Posting Time Heatmap | Day × Hour engagement matrix |
| 4 | Monthly Trends | Engagement over 12 months |
| 5 | Hashtag & Emoji Impact | Optimal hashtag count, emoji uplift |
| 6 | Category Performance | Rankings across 8 content categories |
| 7 | Correlation Matrix | Feature relationship analysis |
| 8 | Top Categories | Top 8 by engagement rate |

---

## 🛠️ Tech Stack

```python
pandas==2.x          # Data manipulation
numpy==1.x           # Numerical computing
matplotlib==3.x      # Static visualisations
seaborn==0.13.x      # Statistical charts
plotly==5.x          # Interactive dashboard
reportlab==4.x       # PDF generation
jupyter              # Notebook environment
```

---

## 📋 Deliverables Checklist

- [x] Dataset (2,000 rows, 18 features)
- [x] Jupyter Notebook (12 analysis cells)
- [x] 8 Professional visualisations
- [x] 11-page PDF report with executive summary
- [x] Interactive Plotly dashboard (9 charts)
- [x] Reusable helper function library
- [x] GitHub repository with full documentation
- [x] 10-slide presentation deck

---

## 💡 Strategic Recommendations

1. **Platform Focus** — Concentrate 40% of budget on TikTok
2. **Content Format** — Prioritise Video and Reel production
3. **Posting Schedule** — Saturday at 17:00 for peak engagement
4. **Hashtag Strategy** — Use 6–10 relevant hashtags per post
5. **Emoji Usage** — Include 1–3 emojis for ~12% engagement uplift
6. **Category Focus** — Invest in Tech and Fitness content

---

*Built as part of a Data Analysis Portfolio — Month 2 Project*