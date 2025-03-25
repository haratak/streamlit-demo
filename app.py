import streamlit as st
from sales_analysis import show_sales_analysis_page

# ページ設定
st.set_page_config(
    page_title="店舗売上分析システム",
    page_icon="🏠",
    layout="wide"
)



pages = [
    st.Page("home.py", title="ホーム"),
    st.Page("daily_sales_analysys.py", title="日次実績"),
]

pg = st.navigation(pages)
pg.run()