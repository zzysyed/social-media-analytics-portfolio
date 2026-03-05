# src/dashboard.py
# Interactive HTML dashboard using Plotly

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

def build_dashboard(csv_path='../data/social_media_data.csv',
                    out_path='../reports/dashboard.html'):

    # ── load & clean ──────────────────────────────────────────────
    df = pd.read_csv(csv_path, parse_dates=['post_date'])
    for col in ['likes', 'comments', 'shares', 'hashtag_count']:
        df[col] = df.groupby('platform')[col].transform(lambda x: x.fillna(x.median()))
    df['total_engagement'] = df['likes'] + df['comments'] + df['shares']
    df['month'] = df['post_date'].dt.month
    df['month_name'] = df['post_date'].dt.strftime('%b')

    COLORS = px.colors.qualitative.Bold

    # ── aggregate data ────────────────────────────────────────────
    platform_stats = (df.groupby('platform')
                        .agg(Posts=('post_id','count'),
                             Avg_Eng=('engagement_rate','mean'),
                             Avg_Likes=('likes','mean'),
                             Total_Views=('views','sum'))
                        .round(4).reset_index()
                        .sort_values('Avg_Eng', ascending=False))

    content_stats = (df.groupby('content_type')
                       .agg(Avg_Eng=('engagement_rate','mean'),
                            Posts=('post_id','count'))
                       .round(4).reset_index()
                       .sort_values('Avg_Eng', ascending=False))

    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_stats = (df.groupby('day_of_week')['engagement_rate']
                   .mean().reindex(day_order).reset_index())
    day_stats.columns = ['day', 'avg_eng']

    monthly = (df.groupby(['month','month_name'])
                 .agg(Avg_Eng=('engagement_rate','mean'),
                      Posts=('post_id','count'))
                 .reset_index().sort_values('month'))

    category_stats = (df.groupby('category')
                        .agg(Avg_Eng=('engagement_rate','mean'),
                             Avg_Views=('views','mean'))
                        .round(4).reset_index()
                        .sort_values('Avg_Eng', ascending=False))

    # heatmap pivot
    heatmap_pivot = (df.groupby(['day_of_week','hour_of_day'])['engagement_rate']
                       .mean().unstack().reindex(day_order))

    # ── build 3×3 subplot grid ────────────────────────────────────
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[
            '📱 Avg Engagement Rate by Platform',
            '🎬 Content Type Performance',
            '📅 Best Days to Post',
            '📈 Monthly Engagement Trend',
            '⏰ Engagement Heatmap (Day × Hour)',
            '📂 Category Rankings',
            '🍩 Platform Post Share',
            '👁️ Total Views by Platform',
            '📊 Likes vs Comments vs Shares',
        ],
        specs=[
            [{'type': 'xy'},   {'type': 'xy'},   {'type': 'xy'}],
            [{'type': 'xy'},   {'type': 'xy'},   {'type': 'xy'}],
            [{'type': 'pie'},  {'type': 'xy'},   {'type': 'xy'}],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )

    # ── Chart 1: platform engagement bar ─────────────────────────
    fig.add_trace(go.Bar(
        x=platform_stats['platform'], y=platform_stats['Avg_Eng'],
        marker_color=COLORS[:len(platform_stats)],
        text=platform_stats['Avg_Eng'].apply(lambda v: f'{v:.4f}%'),
        textposition='outside', name='Avg Eng%',
        showlegend=False,
    ), row=1, col=1)

    # ── Chart 2: content type horizontal bar ─────────────────────
    fig.add_trace(go.Bar(
        x=content_stats['Avg_Eng'], y=content_stats['content_type'],
        orientation='h',
        marker_color=COLORS[:len(content_stats)],
        text=content_stats['Avg_Eng'].apply(lambda v: f'{v:.4f}%'),
        textposition='outside', name='Content Eng',
        showlegend=False,
    ), row=1, col=2)

    # ── Chart 3: best days bar ────────────────────────────────────
    bar_colors = ['#e74c3c' if v == day_stats['avg_eng'].max()
                  else '#3498db' for v in day_stats['avg_eng']]
    fig.add_trace(go.Bar(
        x=day_stats['day'].str[:3], y=day_stats['avg_eng'],
        marker_color=bar_colors, name='Day Eng',
        text=day_stats['avg_eng'].apply(lambda v: f'{v:.4f}%'),
        textposition='outside', showlegend=False,
    ), row=1, col=3)

    # ── Chart 4: monthly line ─────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=monthly['month_name'], y=monthly['Avg_Eng'],
        mode='lines+markers',
        line=dict(color='#e74c3c', width=2.5),
        marker=dict(size=8),
        fill='tozeroy', fillcolor='rgba(231,76,60,0.1)',
        name='Monthly Eng', showlegend=False,
    ), row=2, col=1)

    # ── Chart 5: heatmap ─────────────────────────────────────────
    fig.add_trace(go.Heatmap(
        z=heatmap_pivot.values,
        x=list(range(24)),
        y=day_order,
        colorscale='YlOrRd',
        showscale=True,
        colorbar=dict(len=0.28, y=0.5, x=0.65, thickness=10),
        name='Heatmap',
    ), row=2, col=2)

    # ── Chart 6: category horizontal bar ─────────────────────────
    fig.add_trace(go.Bar(
        x=category_stats['Avg_Eng'],
        y=category_stats['category'],
        orientation='h',
        marker_color=px.colors.sequential.Viridis_r[:len(category_stats)],
        name='Category Eng', showlegend=False,
    ), row=2, col=3)

    # ── Chart 7: donut — platform post share ─────────────────────
    fig.add_trace(go.Pie(
        labels=platform_stats['platform'],
        values=platform_stats['Posts'],
        hole=0.45,
        marker_colors=COLORS[:len(platform_stats)],
        textinfo='label+percent', name='Post Share',
        showlegend=False,
    ), row=3, col=1)

    # ── Chart 8: total views bar ──────────────────────────────────
    fig.add_trace(go.Bar(
        x=platform_stats['platform'],
        y=platform_stats['Total_Views'],
        marker_color=COLORS[:len(platform_stats)],
        text=(platform_stats['Total_Views'] / 1e6).apply(lambda v: f'{v:.1f}M'),
        textposition='outside', name='Views', showlegend=False,
    ), row=3, col=2)

    # ── Chart 9: stacked bar — likes / comments / shares ─────────
    platform_detail = (df.groupby('platform')
                         .agg(Likes=('likes','mean'),
                              Comments=('comments','mean'),
                              Shares=('shares','mean'))
                         .reset_index())
    for metric, color in zip(['Likes','Comments','Shares'],
                              ['#3498db','#e74c3c','#2ecc71']):
        fig.add_trace(go.Bar(
            name=metric, x=platform_detail['platform'],
            y=platform_detail[metric], marker_color=color,
        ), row=3, col=3)
    fig.update_layout(barmode='group')

    # ── global layout ─────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text='<b>📊 Social Media Analytics Dashboard — 2024</b>',
            font=dict(size=22),
            x=0.5,
        ),
        height=1300,
        width=1400,
        paper_bgcolor='#0f0f1a',
        plot_bgcolor='#1a1a2e',
        font=dict(color='white', family='Helvetica'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='white', borderwidth=1,
        ),
    )

    # fix subplot bg colours
    for i in range(1, 10):
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)',
                         row=(i-1)//3+1, col=(i-1)%3+1)
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)',
                         row=(i-1)//3+1, col=(i-1)%3+1)

    # ── save ──────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.write_html(out_path, include_plotlyjs='cdn')
    print(f'✅ Interactive dashboard saved → {out_path}')
    return out_path


if __name__ == '__main__':
    build_dashboard()