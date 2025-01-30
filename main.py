import streamlit as st
import os
import pandas as pd
from modules.recommend import recommend_page
from modules.analyze import analytics_page

# データ読み込み
@st.cache_data
def load_product_data():
    return pd.read_csv("data/product_data.csv")

@st.cache_data
def load_user_data(user_file):
    return pd.read_csv(user_file)

# ユーザー選択
def select_user():
    user_files = sorted(os.listdir("data/user_data"))
    user_ids = [int(f.split("_")[1].split(".")[0]) for f in user_files]
    selected_user_id = st.sidebar.selectbox("ユーザーを選択", user_ids)
    user_file = f"data/user_data/user_{selected_user_id}.csv"
    return load_user_data(user_file), selected_user_id

product_data = load_product_data()
user_data, user_id = select_user()

# サイドバーでページ選択
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページを選択", ["レコメンド", "利用分析"])

if page == "レコメンド":
    recommend_page(product_data, user_data)
elif page == "利用分析":
    analytics_page(product_data, user_data)