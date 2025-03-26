import pandas as pd
import streamlit as st
from datetime import datetime

df = pd.read_csv("data/pos_data.csv")
stores = df["店舗名"].unique()
departments = df["部門名"].unique()

# ヘッダーの表示
st.header("ホーム")

# データ読み込み後に日付をdatetime型に変換
df["日付"] = pd.to_datetime(df["日付"])

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

# 日付範囲でフィルタリング（修正）
start_date, end_date = selected_dates
filtered_df = df[
    (df["日付"] >= pd.Timestamp(start_date)) & 
    (df["日付"] <= pd.Timestamp(end_date))
]

# 店舗・部門でフィルタリング
if selected_stores:
    filtered_df = filtered_df[filtered_df["店舗名"].isin(selected_stores)]
if selected_departments:
    filtered_df = filtered_df[filtered_df["部門名"].isin(selected_departments)]

# 前月の日付範囲を取得
prev_month_start = pd.Timestamp(start_date) - pd.DateOffset(months=1)
prev_month_end = pd.Timestamp(end_date) - pd.DateOffset(months=1)

# 前月データを取得
filtered_prev_month_df = df[
    (df["日付"] >= prev_month_start) & 
    (df["日付"] <= prev_month_end)
]

# 前月も同じフィルター条件を適用
if selected_stores:
    filtered_prev_month_df = filtered_prev_month_df[filtered_prev_month_df["店舗名"].isin(selected_stores)]
if selected_departments:
    filtered_prev_month_df = filtered_prev_month_df[filtered_prev_month_df["部門名"].isin(selected_departments)]

# 前月の日付を現在月に合わせる
filtered_prev_month_df = filtered_prev_month_df.copy()
filtered_prev_month_df["日付"] = filtered_prev_month_df["日付"] + pd.DateOffset(months=1)

# 当月と前月の日次売上を集計
daily_sales_current = filtered_df.groupby("日付")["売上金額"].sum().reset_index()
daily_sales_prev_month = filtered_prev_month_df.groupby("日付")["売上金額"].sum().reset_index()
daily_sales_prev_month.rename(columns={"売上金額": "前月売上金額"}, inplace=True)

# 当月と前月のデータを結合
daily_sales_combined = pd.merge(
    daily_sales_current,
    daily_sales_prev_month,
    on="日付",
    how="left"
).fillna(0)

# 前月比を計算
daily_sales_combined["前月比"] = (
    (daily_sales_combined["売上金額"] - daily_sales_combined["前月売上金額"])
    / daily_sales_combined["前月売上金額"].replace({0: pd.NA})
    * 100
).fillna(0)

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


st.subheader("期間推移（前月対比）")
st.line_chart(
    daily_sales_combined.set_index("日付")[["売上金額", "前月売上金額"]]
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
dept_store_sales = filtered_df.pivot_table(
    values="売上金額",
    index="部門名",
    columns="店舗名",
    aggfunc="sum"
).reset_index()
st.subheader("部門比較")
st.bar_chart(
    dept_store_sales,
    x="部門名",
)







