import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_eda_assets():
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#cccccc'
    plt.rcParams['axes.linewidth'] = 1.0

    figures_dir = os.path.join('reports', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join('data', 'raw', 'UCI_Credit_Card.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join('data', 'UCI_Credit_Card.csv')

    df = pd.read_csv(csv_path)
    target_col = 'default.payment.next.month'

    # Colors
    palette_target = {0: '#2ca02c', 1: '#d62728'}

    print("Generating EDA charts...")

    # 1. Target Distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    counts = df[target_col].value_counts()
    pcts = df[target_col].value_counts(normalize=True) * 100

    bars = axes[0].bar(['Không vỡ nợ (0)', 'Vỡ nợ (1)'], counts, color=['#2ca02c', '#d62728'], width=0.5, edgecolor='black', alpha=0.85)
    axes[0].set_title('Số lượng mẫu theo Biến Mục tiêu', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_ylabel('Số lượng khách hàng', fontsize=11)
    for bar, count, pct in zip(bars, counts, pcts):
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 300, f'{count:,}\n({pct:.2f}%)', ha='center', va='bottom', fontsize=10, fontweight='bold')
    axes[0].set_ylim(0, 27000)

    wedges, texts, autotexts = axes[1].pie(counts, labels=['Không vỡ nợ (0)', 'Vỡ nợ (1)'], autopct='%1.2f%%',
                                      startangle=90, colors=['#2ca02c', '#d62728'], explode=(0, 0.08),
                                      wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    axes[1].set_title('Tỷ lệ phần trăm Biến Mục tiêu (3.52 : 1)', fontsize=13, fontweight='bold', pad=12)
    plt.setp(autotexts, size=11, weight="bold", color="white")

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'target_distribution.png'), dpi=300)
    plt.close()

    # 2. Demographic Distributions
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # SEX
    sex_counts = df['SEX'].value_counts().sort_index()
    sex_labels = ['Nam (1)', 'Nữ (2)']
    axes[0, 0].bar(sex_labels, sex_counts, color=['#4c72b0', '#c44e52'], width=0.5, edgecolor='black', alpha=0.85)
    axes[0, 0].set_title('Phân bố Giới tính (SEX)', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Số lượng', fontsize=10)
    for i, v in enumerate(sex_counts):
        axes[0, 0].text(i, v + 200, f'{v:,} ({v/len(df)*100:.1f}%)', ha='center', fontweight='bold')

    # EDUCATION
    edu_counts = df['EDUCATION'].value_counts().sort_index()
    edu_labels = [f'Mã {k}' for k in edu_counts.index]
    axes[0, 1].bar(edu_labels, edu_counts.values, color='#55a868', edgecolor='black', alpha=0.85)
    axes[0, 1].set_title('Phân bố Trình độ Học vấn (EDUCATION)', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Số lượng', fontsize=10)
    for i, (k, v) in enumerate(edu_counts.items()):
        axes[0, 1].text(i, v + 200, f'{v:,}', ha='center', fontsize=9)

    # MARRIAGE
    marr_counts = df['MARRIAGE'].value_counts().sort_index()
    marr_labels = [f'Mã {k}' for k in marr_counts.index]
    axes[1, 0].bar(marr_labels, marr_counts.values, color='#8172b0', edgecolor='black', alpha=0.85)
    axes[1, 0].set_title('Phân bố Tình trạng Hôn nhân (MARRIAGE)', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Số lượng', fontsize=10)
    for i, (k, v) in enumerate(marr_counts.items()):
        axes[1, 0].text(i, v + 200, f'{v:,}', ha='center', fontsize=9)

    # AGE
    sns.histplot(df['AGE'], kde=True, ax=axes[1, 1], color='#ccb974', bins=30)
    axes[1, 1].set_title('Phân bố Độ tuổi (AGE)', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Tuổi', fontsize=10)
    axes[1, 1].set_ylabel('Tần suất', fontsize=10)
    axes[1, 1].axvline(df['AGE'].mean(), color='red', linestyle='--', label=f'Mean: {df["AGE"].mean():.1f}')
    axes[1, 1].axvline(df['AGE'].median(), color='green', linestyle='-', label=f'Median: {df["AGE"].median():.1f}')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'demographic_distribution.png'), dpi=300)
    plt.close()

    # 3. Default Rates across Groups
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Default rate by SEX
    sex_dr = df.groupby('SEX')[target_col].mean() * 100
    bars = axes[0, 0].bar(['Nam (1)', 'Nữ (2)'], sex_dr, color=['#4c72b0', '#c44e52'], width=0.4, edgecolor='black')
    axes[0, 0].set_title('Tỷ lệ Vỡ nợ (%) theo Giới tính', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Tỷ lệ Vỡ nợ (%)', fontsize=10)
    for bar in bars:
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.2f}%', ha='center', fontweight='bold')
    axes[0, 0].set_ylim(0, 30)

    # Default rate by EDUCATION
    edu_map = {0: '0: Undoc', 1: '1: Grad Sch', 2: '2: Univ', 3: '3: High Sch', 4: '4: Others', 5: '5: Undoc', 6: '6: Undoc'}
    df['EDU_LABEL'] = df['EDUCATION'].map(edu_map)
    edu_dr = df.groupby('EDU_LABEL')[target_col].mean() * 100
    bars = axes[0, 1].bar(edu_dr.index, edu_dr.values, color='#55a868', edgecolor='black')
    axes[0, 1].set_title('Tỷ lệ Vỡ nợ (%) theo Học vấn', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Tỷ lệ Vỡ nợ (%)', fontsize=10)
    axes[0, 1].tick_params(axis='x', rotation=30)
    for bar in bars:
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
    axes[0, 1].set_ylim(0, 32)

    # Default rate by MARRIAGE
    marr_map = {0: '0: Undoc', 1: '1: Married', 2: '2: Single', 3: '3: Others'}
    df['MARR_LABEL'] = df['MARRIAGE'].map(marr_map)
    marr_dr = df.groupby('MARR_LABEL')[target_col].mean() * 100
    bars = axes[1, 0].bar(marr_dr.index, marr_dr.values, color='#8172b0', edgecolor='black')
    axes[1, 0].set_title('Tỷ lệ Vỡ nợ (%) theo Hôn nhân', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Tỷ lệ Vỡ nợ (%)', fontsize=10)
    for bar in bars:
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
    axes[1, 0].set_ylim(0, 32)

    # Default rate by PAY_0
    p0_dr = df.groupby('PAY_0')[target_col].mean() * 100
    bars = axes[1, 1].bar([str(x) for x in p0_dr.index], p0_dr.values, color='#d62728', alpha=0.85, edgecolor='black')
    axes[1, 1].set_title('Tỷ lệ Vỡ nợ (%) theo Lịch sử Thanh toán Tháng 9/2005 (PAY_0)', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Giá trị PAY_0 (Trậm trả theo tháng)', fontsize=10)
    axes[1, 1].set_ylabel('Tỷ lệ Vỡ nợ (%)', fontsize=10)
    for bar in bars:
        y = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., y + 1.0, f'{y:.0f}%', ha='center', fontsize=8, fontweight='bold')
    axes[1, 1].set_ylim(0, 90)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'default_rates_by_groups.png'), dpi=300)
    plt.close()

    # 4. Boxplots by Target
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # LIMIT_BAL by Target
    sns.boxplot(x=target_col, y='LIMIT_BAL', hue=target_col, data=df, ax=axes[0, 0], palette=palette_target, legend=False)
    axes[0, 0].set_title('Hạn mức Tín dụng (LIMIT_BAL) theo Biến Mục tiêu', fontsize=12, fontweight='bold')
    axes[0, 0].set_xticks([0, 1])
    axes[0, 0].set_xticklabels(['Không vỡ nợ (0)', 'Vỡ nợ (1)'])
    axes[0, 0].set_ylabel('LIMIT_BAL (NTD)', fontsize=10)

    # AGE by Target
    sns.boxplot(x=target_col, y='AGE', hue=target_col, data=df, ax=axes[0, 1], palette=palette_target, legend=False)
    axes[0, 1].set_title('Độ tuổi (AGE) theo Biến Mục tiêu', fontsize=12, fontweight='bold')
    axes[0, 1].set_xticks([0, 1])
    axes[0, 1].set_xticklabels(['Không vỡ nợ (0)', 'Vỡ nợ (1)'])
    axes[0, 1].set_ylabel('AGE (Tuổi)', fontsize=10)

    # Log1p(PAY_AMT1) by Target
    df['log_PAY_AMT1'] = np.log1p(df['PAY_AMT1'])
    sns.boxplot(x=target_col, y='log_PAY_AMT1', hue=target_col, data=df, ax=axes[1, 0], palette=palette_target, legend=False)
    axes[1, 0].set_title('Log(PAY_AMT1 + 1) theo Biến Mục tiêu', fontsize=12, fontweight='bold')
    axes[1, 0].set_xticks([0, 1])
    axes[1, 0].set_xticklabels(['Không vỡ nợ (0)', 'Vỡ nợ (1)'])
    axes[1, 0].set_ylabel('Log1p(PAY_AMT1)', fontsize=10)

    # Log1p(BILL_AMT1) by Target (positive values)
    df['log_BILL_AMT1'] = np.log1p(df['BILL_AMT1'].clip(lower=0))
    sns.boxplot(x=target_col, y='log_BILL_AMT1', hue=target_col, data=df, ax=axes[1, 1], palette=palette_target, legend=False)
    axes[1, 1].set_title('Log(BILL_AMT1 + 1) theo Biến Mục tiêu', fontsize=12, fontweight='bold')
    axes[1, 1].set_xticks([0, 1])
    axes[1, 1].set_xticklabels(['Không vỡ nợ (0)', 'Vỡ nợ (1)'])
    axes[1, 1].set_ylabel('Log1p(BILL_AMT1 clipped >= 0)', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'boxplots_by_target.png'), dpi=300)
    plt.close()

    # 5. Correlation Heatmap Full
    plt.figure(figsize=(16, 12))
    feature_cols = [c for c in df.columns if c not in ['ID', 'EDU_LABEL', 'MARR_LABEL', 'log_PAY_AMT1', 'log_BILL_AMT1']]
    corr = df[feature_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.2, vmax=1.0,
                linewidths=0.5, cbar_kws={"shrink": .8}, annot_kws={"size": 7})
    plt.title('Ma trận Tương quan Pearson Toàn bộ Đặc trưng với Target', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'correlation_heatmap.png'), dpi=300)
    plt.close()

    # 6. Multicollinearity Detail Heatmap
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    bill_cols = [f'BILL_AMT{i}' for i in range(1, 7)]
    corr_bill = df[bill_cols].corr()
    sns.heatmap(corr_bill, annot=True, fmt='.2f', cmap='YlGnBu', ax=axes[0], cbar=False, annot_kws={"size": 10})
    axes[0].set_title('Tương quan giữa các biến Dư nợ (BILL_AMT1..6)', fontsize=12, fontweight='bold')

    pay_cols = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    corr_pay = df[pay_cols].corr()
    sns.heatmap(corr_pay, annot=True, fmt='.2f', cmap='YlOrRd', ax=axes[1], cbar=False, annot_kws={"size": 10})
    axes[1].set_title('Tương quan giữa các biến Lịch sử Thanh toán (PAY_0..6)', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'multicollinearity_heatmap.png'), dpi=300)
    plt.close()

    print("EDA charts generated successfully!")

if __name__ == '__main__':
    generate_eda_assets()
