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

# 表示するカラムの定義
columns = {
    "id": "ID",
    "name": "名称",
    "currentCustomers": "当日客数",
    "totalCustomers": "累計客数",
    "prevYearCustomers": "前年客数",
    "prevYearTotalCustomers": "前年累計客数",
    "prevYearSameDayCustomers": "前年同曜日客数",
    "prevYearSameDayTotalCustomers": "前年同曜日累計客数"
}

# フォーマット設定
format_dict = {
    "当日客数": "{:,.0f}",
    "累計客数": "{:,.0f}",
    "前年客数": "{:,.0f}",
    "前年累計客数": "{:,.0f}",
    "前年同曜日客数": "{:,.0f}",
    "前年同曜日累計客数": "{:,.0f}"
}

# ヘッダーの表示
st.header("店舗・部門別客数分析")

# 日付選択
selected_date = st.date_input(
    "日付を選択",
    value=datetime.now(),
    format="YYYY/MM/DD"
)

# 区切り線を追加
st.divider()

# 店舗選択
selected_store = st.selectbox(
    "店舗を選択",
    options=[store["id"] for store in STORES],
    format_func=lambda x: next((store["name"] for store in STORES if store["id"] == x), x),
)

def generate_sample_data(data_type="store", selected_store_id=None, target_date=None):
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

    if selected_store_id:
        items = departments
    else:
        items = stores if data_type == "store" else departments

    if target_date is None:
        target_date = datetime.now().date()
    
    data = []
    for item in items:
        if selected_store_id and data_type == "store" and item["id"] != selected_store_id:
            continue
            
        # 基準値の設定
        base_customers = np.random.randint(500, 1000)
        
        # 当日データの生成
        current_customers = base_customers + np.random.randint(-50, 50)
        
        # 前年データの生成
        prev_year_customers = current_customers * (1 + np.random.uniform(-0.2, 0.2))
        prev_year_same_day_customers = prev_year_customers * (1 + np.random.uniform(-0.1, 0.1))
        
        record = {
            "id": item["id"],
            "name": item["name"],
            "currentCustomers": current_customers,
            "totalCustomers": current_customers * 30,  # 仮の累計値
            "prevYearCustomers": prev_year_customers,
            "prevYearTotalCustomers": prev_year_customers * 30,  # 仮の累計値
            "prevYearSameDayCustomers": prev_year_same_day_customers,
            "prevYearSameDayTotalCustomers": prev_year_same_day_customers * 30  # 仮の累計値
        }
        data.append(record)
    
    return pd.DataFrame(data)

# データ表示
if selected_store == "ALL":
    st.subheader("全店舗実績")
    df_store = generate_sample_data(
        data_type="store",
        target_date=selected_date
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
    
    # 行数に応じて高さを計算
    height = min(len(df_department) * 35 + 50, 400)
    
    st.dataframe(
        df_department.style.format(format_dict),
        use_container_width=True,
        height=height
    )
