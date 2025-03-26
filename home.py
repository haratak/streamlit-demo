import pandas as pd
import streamlit as st
from datetime import datetime

df = pd.read_csv("data/pos_data.csv")
stores = df["店舗名"].unique()
departments = df["部門名"].unique()

# ヘッダーの表示
st.header("ホーム")

# 期間選択

selected_dates = st.date_input(
    "期間を選択",
    value=(datetime.now().replace(day=1), datetime.now()),
    min_value=None,
    max_value=None,
    format="YYYY/MM/DD"
)

# 2カラムレイアウトの作成
col1, col2 = st.columns(2)

# 左カラム: 店舗選択
with col1:
    selected_stores = st.multiselect(
        "店舗を選択",
        placeholder="未選択時は全店舗となります",
        options=stores,
        format_func=lambda x: x
    )

# 右カラム: 部門選択 
with col2:
    selected_departments = st.multiselect(
        "部門を選択",
        placeholder="未選択時は全部門となります",
        options=departments,
        format_func=lambda x: x
    )


# 区切り線を追加
st.divider()

# 日付範囲でフィルタリング
start_date = selected_dates[0].strftime("%Y-%m-%d")
end_date = selected_dates[1].strftime("%Y-%m-%d")
filtered_df = df[(df["日付"] >= start_date) & (df["日付"] <= end_date)]

# 店舗・部門でフィルタリング
if selected_stores:
    filtered_df = filtered_df[filtered_df["店舗名"].isin(selected_stores)]
if selected_departments:
    filtered_df = filtered_df[filtered_df["部門名"].isin(selected_departments)]

# 日付ごとの売上集計
daily_sales_by_date = filtered_df.groupby("日付")["売上金額"].sum().reset_index()

daily_sales_by_store = filtered_df.groupby(["店舗名"])["売上金額"].sum().reset_index()

daily_sales_by_department = filtered_df.groupby(["部門名"])["売上金額"].sum().reset_index()

# 折れ線グラフの描画

col1,col2,col3 = st.columns(3)
# KPI集計値の計算
total_sales = filtered_df["売上金額"].sum()
total_customers = filtered_df["客数"].sum() 
total_quantity = filtered_df["個数"].sum()

# KPIカードの表示
with col1:
    st.metric(
        label="売上金額",
        value=f"¥{total_sales:,.0f}"
    )

with col2:
    st.metric(
        label="客数",
        value=f"{total_customers:,.0f}人"
    )

with col3:
    st.metric(
        label="販売個数", 
        value=f"{total_quantity:,.0f}個"
    )


st.subheader("期間推移")
st.bar_chart(
    daily_sales_by_date,
    x="日付",
    y="売上金額"
)

st.subheader("店舗比較")
# 店舗×部門のクロス集計
store_dept_sales = filtered_df.pivot_table(
    values="売上金額",
    index="店舗名",
    columns="部門名",
    aggfunc="sum"
).reset_index()

st.bar_chart(
    store_dept_sales,
    x="店舗名"
)
st.subheader("部門比較")
st.bar_chart(
    daily_sales_by_department,
    x="部門名",
    y="売上金額"
)







