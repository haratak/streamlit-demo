import streamlit as st

# ページ設定
st.set_page_config(
    page_title="店舗売上分析システム",
    page_icon="🏠",
    layout="wide"
)



pages = [
    st.Page("home.py", title="ホーム"),
    st.Page("hourly_sales_analysis.py", title="時間帯別売上実績"),
    st.Page("daily_sales_analysis.py", title="日次売上実績"),
    st.Page("daily_customer_analysis.py", title="日次客数実績"),
    st.Page("daily_sales_calendar.py", title="日次売上カレンダー"),
]

pg = st.navigation(pages)
pg.run()