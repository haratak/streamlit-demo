import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 定数の定義
STORES = [{"id": "ALL", "name": "全店舗"}] + [
    {"id": "S001", "name": "店舗A"},
    {"id": "S002", "name": "店舗B"},
    {"id": "S003", "name": "店舗C"},
    {"id": "S004", "name": "店舗D"}
]

# 表示するカラムの定義を更新
columns = {
    # 基本情報
    "id": "店舗ID",
    "name": "店舗名",
    # 売上関連
    "currentSales": "売上",
    "lastWeekSales": "前週売上",
    "lastWeekRatio": "前週比率",
    "totalSales": "累計売上",
    "totalLastWeekSales": "累計前週売上",
    "totalLastWeekRatio": "累計前週比率",
    # 客数関連
    "currentCustomers": "客数",
    "totalCustomers": "累計客数",
    "averageSalePerCustomer": "客単価",
    # 商品関連
    "currentStockKeepingUnit": "商品点数",
    "totalStockKeepingUnit": "累計商品点数",
    "currentStockKeepingUnitPrice": "一品単価",
    # 予算関連
    "budgetRatio": "予算消化率"
}

# フォーマット設定を更新
format_dict = {
    "売上": "¥{:,.0f}",
    "前週売上": "¥{:,.0f}",
    "前週比率": "{:.1f}%",
    "累計売上": "¥{:,.0f}",
    "累計前週売上": "¥{:,.0f}",
    "累計前週比率": "{:.1f}%",
    "客数": "{:,.0f}",
    "累計客数": "{:,.0f}",
    "客単価": "¥{:,.0f}",
    "商品点数": "{:,.0f}",
    "累計商品点数": "{:,.0f}",
    "一品単価": "¥{:,.0f}",
    "予算消化率": "{:.1f}%"
}

# ヘッダーの表示
st.header("店舗・部門別売上分析")

# 日付選択
selected_date = st.date_input(
    "日付を選択",
    value=datetime.now(),
    format="YYYY/MM/DD"
)

# 時間帯選択スライダーを修正
st.subheader("時間帯選択")
selected_hours = st.select_slider(
    "時間帯を選択",
    options=list(range(10, 23)),
    value=10,
    format_func=lambda x: f"{x:02d}:00",
)

# 区切り線を追加
st.divider()

# 店舗選択
selected_store = st.selectbox(
    "店舗を選択",
    options=[store["id"] for store in STORES],
    format_func=lambda x: next((store["name"] for store in STORES if store["id"] == x), x),
)

# generate_sample_data関数を修正
def generate_sample_data(data_type="store", selected_store_id=None, target_date=None, hour=10):
    # 店舗/部門の定義
    stores = [
        {"id": "S001", "name": "店舗A"},
        {"id": "S002", "name": "店舗B"},
        {"id": "S003", "name": "店舗C"},
        {"id": "S004", "name": "店舗D"}
    ]
    
    departments = [
        {"id": "D001", "name": "食品"},
        {"id": "D002", "name": "鮮魚"},
        {"id": "D003", "name": "精肉"},
        {"id": "D004", "name": "青果"},
        {"id": "D005", "name": "惣菜"},
        {"id": "D006", "name": "ベーカリー"}
    ]

    # 選択されたアイテムの決定
    if selected_store_id:
        items = departments  # 店舗が選択された場合は部門データを表示
    else:
        items = stores if data_type == "store" else departments

    # データ生成の期間設定を修正
    if target_date is None:
        target_date = datetime.now().date()
    
    data = []
    for item in items:
        if selected_store_id and data_type == "store" and item["id"] != selected_store_id:
            continue
            
        # 時間帯による変動を考慮した基準値の設定
        time_factor = 1.0
        if 11 <= hour <= 14:  # ランチタイム
            time_factor = 1.5
        elif 17 <= hour <= 20:  # ディナータイム
            time_factor = 1.8
            
        # 基準値の設定
        base_sales = np.random.randint(800000, 1200000) * time_factor
        base_customers = np.random.randint(500, 1000) * time_factor
        base_sku = np.random.randint(300, 500) * time_factor
        
        # 当日データの生成
        current_sales = base_sales + np.random.randint(-100000, 100000)
        last_week_sales = current_sales * (1 + np.random.uniform(-0.2, 0.2))
        budget = base_sales * 1.1
        
        record = {
            "id": item["id"],
            "name": item["name"],
            # 売上関連
            "currentSales": current_sales,
            "lastWeekSales": last_week_sales,
            "lastWeekRatio": (current_sales / last_week_sales) * 100,
            "totalSales": current_sales * 1.5,
            "totalLastWeekSales": last_week_sales * 1.5,
            "totalLastWeekRatio": (current_sales * 1.5) / (last_week_sales * 1.5) * 100,
            # 客数関連
            "currentCustomers": base_customers,
            "totalCustomers": base_customers * 1.5,
            "averageSalePerCustomer": current_sales / base_customers,
            # 商品関連
            "currentStockKeepingUnit": base_sku,
            "totalStockKeepingUnit": base_sku * 1.5,
            "currentStockKeepingUnitPrice": current_sales / base_sku,
            # 予算関連
            "budgetRatio": (current_sales / budget) * 100
        }
        data.append(record)
    
    return pd.DataFrame(data)

# データ表示
if selected_store == "ALL":
    st.subheader(f"全店舗実績 ({selected_hours}時台)")
    df_store = generate_sample_data(
        data_type="store",
        target_date=selected_date,
        hour=selected_hours
    )
    
    # カラム名を日本語に変換
    df_store = df_store.rename(columns=columns)
    
    # 行数に応じて高さを計算
    height = min(len(df_store) * 35 + 50, 400)
    
    st.dataframe(
        df_store.style.format(format_dict),
        use_container_width=True,
        height=height
    )
    
    # 棒グラフの追加
    st.subheader("時間帯別売上推移")
    
    # 全時間帯のデータを生成
    hourly_data = []
    for hour in range(10, 23):
        df = generate_sample_data(
            data_type="store",
            target_date=selected_date,
            hour=hour
        )
        total_sales = df['currentSales'].sum()
        hourly_data.append({
            'hour': f"{hour:02d}:00",
            'sales': total_sales
        })
    
    df_hourly = pd.DataFrame(hourly_data)
    
    # 棒グラフの描画
    st.bar_chart(
        df_hourly.set_index('hour'),
        use_container_width=True,
        height=400
    )

else:
    store_name = next((store["name"] for store in STORES if store["id"] == selected_store), "")
    st.subheader(f"{store_name}の部門別実績 ({selected_hours}時台)")
    
    df_department = generate_sample_data(
        data_type="department", 
        selected_store_id=selected_store,
        target_date=selected_date,
        hour=selected_hours
    )
    
    # グラフ用のデータを先に作成
    df_department_chart = df_department.set_index('name')[['currentSales']]
    df_department_chart = df_department_chart.rename(columns={'currentSales': '売上'})
    
    # カラム名を日本語に変換（データフレーム表示用）
    df_department = df_department.rename(columns=columns)
    
    # 行数に応じて高さを計算
    height = min(len(df_department) * 35 + 50, 400)
    
    # データフレーム表示
    st.dataframe(
        df_department.style.format(format_dict),
        use_container_width=True,
        height=height
    )
    
    # 部門別の棒グラフ
    st.subheader(f"{store_name} 部門別売上比較 ({selected_hours}時台)")
    
    # 棒グラフの描画
    st.bar_chart(
        df_department_chart,
        use_container_width=True,
        height=400
    ) 
    