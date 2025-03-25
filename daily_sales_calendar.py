import streamlit as st
import streamlit_calendar as st_calendar
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

# フォーマット設定
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

# ヘッダーの表示
st.header("店舗・部門別売上分析")

# 月選択用のセレクトボックスを追加
current_date = datetime.now()
months = pd.date_range(
    start=current_date - timedelta(days=365),
    end=current_date,
    freq='MS'  # Month Start
).strftime("%Y-%m")

selected_month = st.selectbox(
    "月を選択",
    options=months,
    index=len(months)-1
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

# カレンダーデータの生成
@st.cache_data
def generate_calendar_data(year_month, store_id):
    year, month = map(int, year_month.split('-'))
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    calendar_events = []
    current_date = start_date
    
    while current_date <= end_date:
        # サンプルデータの生成
        df = generate_sample_data(
            data_type="store" if store_id == "ALL" else "department",
            selected_store_id=None if store_id == "ALL" else store_id,
            target_date=current_date
        )
        
        # 売上データの取得（英語カラム名でアクセス）
        total_sales = df['currentSales'].sum() if not df.empty else 0
        
        # イベントの作成
        event = {
            'id': current_date.strftime('%Y-%m-%d'),
            'title': f'¥{total_sales:,.0f}',
            'start': current_date.strftime('%Y-%m-%d'),
            'end': current_date.strftime('%Y-%m-%d'),
            'backgroundColor': '#e6f3ff',
            'textColor': '#333333',
        }
        calendar_events.append(event)
        current_date += timedelta(days=1)
    
    return calendar_events

# カレンダーの設定
calendar_options = {
    "headerToolbar": {
        "left": "",
        "center": "title",
        "right": ""
    },
    "initialView": "dayGridMonth",
    "selectable": True,
    "editable": False,
    "locale": "ja",
    "height": "auto",
    "initialDate": f"{selected_month}-01",  # 選択された月の1日を初期日として設定
}

# カレンダーデータの取得と表示
events = generate_calendar_data(selected_month, selected_store)

# キーに選択された月を含めることで、月が変更されたときに確実に再描画される
calendar = st_calendar.calendar(
    events=events,
    options=calendar_options,
    key=f"sales_calendar_{selected_month}_{selected_store}"
) 