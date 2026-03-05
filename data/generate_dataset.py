# data/generate_dataset.py
# Generates a realistic simulated social media dataset

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# --- CONFIG ---
NUM_POSTS = 2000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

PLATFORMS = ['Instagram', 'Twitter', 'Facebook', 'YouTube', 'TikTok']
CONTENT_TYPES = ['Video', 'Image', 'Text', 'Story', 'Reel', 'Poll']
CATEGORIES = ['Tech', 'Fashion', 'Food', 'Travel', 'Fitness', 'Education', 'Entertainment', 'Business']
ACCOUNTS = [f'@user_{i:03d}' for i in range(1, 51)]  # 50 fake accounts

# Platform-specific engagement multipliers
PLATFORM_MULTIPLIERS = {
    'TikTok':    {'likes': 3.5, 'comments': 1.2, 'shares': 2.8, 'views': 10.0},
    'Instagram': {'likes': 2.0, 'comments': 0.8, 'shares': 0.5, 'views': 3.0},
    'YouTube':   {'likes': 1.5, 'comments': 1.5, 'shares': 1.0, 'views': 8.0},
    'Twitter':   {'likes': 1.0, 'comments': 2.0, 'shares': 3.0, 'views': 2.0},
    'Facebook':  {'likes': 1.2, 'comments': 1.0, 'shares': 2.0, 'views': 1.5},
}

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

rows = []
for i in range(NUM_POSTS):
    platform = random.choice(PLATFORMS)
    content_type = random.choice(CONTENT_TYPES)
    category = random.choice(CATEGORIES)
    account = random.choice(ACCOUNTS)
    post_date = random_date(START_DATE, END_DATE)
    
    m = PLATFORM_MULTIPLIERS[platform]
    
    base = random.randint(100, 5000)
    likes    = int(base * m['likes']    * np.random.uniform(0.5, 2.5))
    comments = int(base * m['comments'] * np.random.uniform(0.3, 1.8))
    shares   = int(base * m['shares']   * np.random.uniform(0.2, 2.0))
    views    = int(base * m['views']    * np.random.uniform(1.0, 5.0))
    
    followers = random.randint(500, 500000)
    
    # Engagement rate = (likes + comments + shares) / followers * 100
    engagement_rate = round((likes + comments + shares) / followers * 100, 4)
    
    hashtag_count = random.randint(0, 30)
    has_emoji = random.choice([True, False])
    post_length = random.randint(10, 2200)
    
    rows.append({
        'post_id': f'POST_{i+1:04d}',
        'account': account,
        'platform': platform,
        'content_type': content_type,
        'category': category,
        'post_date': post_date.strftime('%Y-%m-%d %H:%M:%S'),
        'day_of_week': post_date.strftime('%A'),
        'hour_of_day': post_date.hour,
        'month': post_date.month,
        'likes': likes,
        'comments': comments,
        'shares': shares,
        'views': views,
        'followers': followers,
        'engagement_rate': engagement_rate,
        'hashtag_count': hashtag_count,
        'has_emoji': has_emoji,
        'post_length': post_length,
    })

df = pd.DataFrame(rows)

# Inject ~5% missing values to simulate real data
for col in ['likes', 'comments', 'shares', 'hashtag_count']:
    mask = np.random.rand(len(df)) < 0.05
    df.loc[mask, col] = np.nan

df.to_csv('data/social_media_data.csv', index=False)
print(f"✅ Dataset created: {len(df)} rows, {len(df.columns)} columns")
print(df.head())