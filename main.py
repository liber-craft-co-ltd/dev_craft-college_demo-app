import streamlit as st
import pandas as pd
import os
from modules.recommend import recommend_page
from modules.analyze import analytics_page
from modules.search import search_page

# データ読み込み
@st.cache_data
def load_product_data():
    return pd.read_csv("product_data/product_data.csv")

@st.cache_data
def load_similarity_data():
    return pd.read_csv("product_data/product_similarity.csv")

# アプリの設定
product_data = load_product_data()
similarity_data = load_similarity_data()

# アプリ名を表示
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Recommend & Analyze App</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; color: #4CAF50;'>Recommend & Analyze App</h1>", unsafe_allow_html=True)

# サイドバーでページ選択
st.sidebar.title("🛒 メニュー")
page = st.sidebar.radio("ページを選択", ["個別レコメンド", "利用分析", "商品検索"])

# ページ表示
if page == "個別レコメンド":
    recommend_page(product_data)  
elif page == "利用分析":
    analytics_page(product_data, similarity_data)  
elif page == "商品検索":
    search_page(product_data)

# カスタム CSS を適用
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0;  /* サイドバーの背景色 */
    }
    .stButton > button {
        background-color: #4CAF50;  /* ボタンの背景色 */
        color: white;  /* ボタンのテキスト色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
