import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 店舗マスタ
STORES = {
    'S001': '東京本店',
    'S002': '大阪支店',
    'S003': '名古屋支店',
    'S004': '福岡支店',
    'S005': '札幌支店'
}

# 部門マスタ（全店舗共通）
DEPARTMENTS = {
    'D001': '食品',
    'D002': '飲料',
    'D003': '菓子',
    'D004': '日用品',
    'D005': '衣類',
    'D006': '化粧品',
    'D007': '文具',
    'D008': '家電',
    'D009': '玩具',
    'D010': '雑貨'
}

def generate_daily_sales(date, store_id, dept_id):
    """1日分の売上データを生成"""
    # 休日（土日）は売上が1.5倍
    weekend_multiplier = 1.5 if date.weekday() >= 5 else 1.0
    
    # 基本値を設定
    customers = int(np.random.normal(100, 20) * weekend_multiplier)
    quantity = int(np.random.normal(300, 50) * weekend_multiplier)
    amount = int(quantity * np.random.normal(500, 100) * weekend_multiplier)
    
    return {
        '店舗ID': store_id,
        '店舗名': STORES[store_id],
        '部門ID': dept_id,
        '部門名': DEPARTMENTS[dept_id],
        '日付': date.strftime('%Y-%m-%d'),
        '売上金額': amount,
        '客数': customers,
        '個数': quantity
    }

def generate_pos_data(start_date, end_date):
    """指定期間のPOSデータを生成"""
    # 文字列を日付オブジェクトに変換
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    data = []
    current = start
    
    # 指定期間分のデータを生成
    while current <= end:
        for store_id in STORES:
            for dept_id in DEPARTMENTS:
                data.append(generate_daily_sales(current, store_id, dept_id))
        current += timedelta(days=1)
    
    # DataFrameに変換
    df = pd.DataFrame(data)
    
    # データディレクトリが存在しない場合は作成
    os.makedirs('data', exist_ok=True)
    
    # CSVとして出力
    output_file = f'data/pos_data.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f'データを {output_file} に出力しました。')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('使用方法: python generate_mock_data.py 開始日 終了日')
        print('日付形式: YYYY-MM-DD')
        sys.exit(1)
    
    generate_pos_data(sys.argv[1], sys.argv[2])
