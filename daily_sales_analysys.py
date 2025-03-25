import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

# 定数の定義
STORES = [{"id": "ALL", "name": "全店舗"}] + [
    {"id": "S001", "name": "店舗A"},
    {"id": "S002", "name": "店舗B"},
    {"id": "S003", "name": "店舗C"},
    {"id": "S004", "name": "店舗D"}
]

def generate_sample_data(data_type="store", selected_store_id=None, target_date=None):
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
            
        # 選択された日付のデータのみ生成
        # 基準値の設定
        base_sales = np.random.randint(800000, 1200000)
        base_customers = np.random.randint(500, 1000)
        base_sku = np.random.randint(300, 500)
        
        # 当日データの生成
        current_sales = base_sales + np.random.randint(-100000, 100000)
        budget = base_sales * 1.1
        current_customers = base_customers + np.random.randint(-50, 50)
        current_sku = base_sku + np.random.randint(-30, 30)
        
        # 前年データの生成
        last_year_sales = current_sales * (1 + np.random.uniform(-0.2, 0.2))
        last_year_same_day_sales = last_year_sales * (1 + np.random.uniform(-0.1, 0.1))
        
        record = {
            "id": item["id"],
            "name": item["name"],
            # 売上関連
            "currentSales": current_sales,
            "totalSales": current_sales,
            "budgetRatio": (current_sales / budget) * 100,
            "totalBudgetRatio": (current_sales / budget) * 100,
            # 前年比較
            "lastYearSales": last_year_sales,
            "totalLastYearSales": last_year_sales,
            "lastYearSalesRatio": (current_sales / last_year_sales) * 100,
            "totalLastYearSalesRatio": (current_sales / last_year_sales) * 100,
            # 前年同曜日比較
            "lastYearSameDaySales": last_year_same_day_sales,
            "totalLastYearSameDaySales": last_year_same_day_sales,
            "lastYearSameDaySalesRatio": (current_sales / last_year_same_day_sales) * 100,
            "totalLastYearSameDaySalesRatio": (current_sales / last_year_same_day_sales) * 100,
            # 客数関連
            "currentCustomers": current_customers,
            "totalCustomers": current_customers,
            "averageSalePerCustomer": current_sales / current_customers,
            "averageTotalSalePerCustomer": current_sales / current_customers,
            # 商品関連
            "currentStockKeepingUnit": current_sku,
            "totalStockKeepingUnit": current_sku,
            "currentStockKeepingUnitPrice": current_sales / current_sku,
            "totalStockKeepingUnitPrice": current_sales / current_sku
        }
        data.append(record)
    
    return pd.DataFrame(data)

# ヘッダーの表示
st.header("日次実績")

# 期間選択タブ
tab_daily, tab_weekly, tab_monthly = st.tabs(["日次", "週次", "月次"])

with tab_daily:
    selected_date = st.date_input(
            "日付を選択",
            value=datetime.now(),
            format="YYYY/MM/DD"
    )

# ... 既存の期間選択タブの内容 ...

# 区切り線を追加
st.divider()

# 店舗選択
selected_store = st.selectbox(
    "店舗を選択",
    options=[store["id"] for store in STORES],
    format_func=lambda x: next((store["name"] for store in STORES if store["id"] == x), x),
)

# 表示するカラムの定義
columns = {
    # 基本情報
    "id": "ID",
    "name": "名称",
    # 売上関連
    "currentSales": "当日売上",
    "totalSales": "累計売上",
    "budgetRatio": "予算比",
    "totalBudgetRatio": "累計予算比",
    # 前年比較
    "lastYearSales": "前年売上",
    "totalLastYearSales": "累計前年売上",
    "lastYearSalesRatio": "前年比",
    "totalLastYearSalesRatio": "累計前年比",
    # 前年同曜日比較
    "lastYearSameDaySales": "前年同曜日売上",
    "totalLastYearSameDaySales": "累計前年同曜日売上",
    "lastYearSameDaySalesRatio": "前年同曜日比",
    "totalLastYearSameDaySalesRatio": "累計前年同曜日比",
    # 客数関連
    "currentCustomers": "当日客数",
    "totalCustomers": "累計客数",
    "averageSalePerCustomer": "客単価",
    "averageTotalSalePerCustomer": "累計客単価",
    # 商品関連
    "currentStockKeepingUnit": "当日商品点数",
    "totalStockKeepingUnit": "累計商品点数",
    "currentStockKeepingUnitPrice": "当日一品単価",
    "totalStockKeepingUnitPrice": "累計一品単価"
}

# フォーマット設定の更新
format_dict = {
    "当日売上": "¥{:,.0f}",
    "累計売上": "¥{:,.0f}",
    "予算比": "{:.1f}%",
    "累計予算比": "{:.1f}%",
    "前年売上": "¥{:,.0f}",
    "累計前年売上": "¥{:,.0f}",
    "前年比": "{:.1f}%",
    "累計前年比": "{:.1f}%",
    "前年同曜日売上": "¥{:,.0f}",
    "累計前年同曜日売上": "¥{:,.0f}",
    "前年同曜日比": "{:.1f}%",
    "累計前年同曜日比": "{:.1f}%",
    "当日客数": "{:,.0f}",
    "累計客数": "{:,.0f}",
    "客単価": "¥{:,.0f}",
    "累計客単価": "¥{:,.0f}",
    "当日商品点数": "{:,.0f}",
    "累計商品点数": "{:,.0f}",
    "当日一品単価": "¥{:,.0f}",
    "累計一品単価": "¥{:,.0f}"
}

# データ表示
if selected_store == "ALL":
    st.subheader("全店舗実績")
    df_store = generate_sample_data(
        data_type="store",
        target_date=selected_date
    )
    
    # カラム名を日本語に変換
    df_store = df_store.rename(columns=columns)
    
    # 行数に応じて高さを計算（1行あたり35px + ヘッダー用の50px）
    height = min(len(df_store) * 35 + 50, 400)  # 最大400pxまで
    
    st.dataframe(
        df_store.style.format(format_dict),
        use_container_width=True,
        height=height
    )
else:
    store_name = next((store["name"] for store in STORES if store["id"] == selected_store), "")
    st.subheader(f"{store_name}の部門別実績")
    
    df_department = generate_sample_data(
        data_type="department", 
        selected_store_id=selected_store,
        target_date=selected_date
    )
    
    # カラム名を日本語に変換
    df_department = df_department.rename(columns=columns)
    
    # 行数に応じて高さを計算（1行あたり35px + ヘッダー用の50px）
    height = min(len(df_department) * 35 + 50, 400)  # 最大400pxまで
    
    st.dataframe(
        df_department.style.format(format_dict),
        use_container_width=True,
        height=height
    )

# 補足情報の表示
st.markdown("""
* 売上金額は税込み表示です
* 予算比、前年比は100%を基準として評価されます
* 客単価は売上÷客数で算出されています
* 一品単価は売上÷商品点数で算出されています
""")
