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
def load_user_data(user_file):
    return pd.read_csv(user_file)

@st.cache_data
def load_similarity_data():
    return pd.read_csv("product_data/product_similarity.csv")

# ユーザー選択
def select_user():
    # ファイルリストを取得
    user_files = sorted([f for f in os.listdir("user_data/") if f.endswith('.csv')])
    user_labels = [f.replace('.csv', '') for f in user_files]
    user_labels.sort(key=lambda x: int(x.split('.')[0]))
    user_labels.insert(0, '全体')
    selected_user_label = st.sidebar.selectbox("ユーザーを選択", user_labels)
    if selected_user_label == '全体':
        user_data_all = pd.concat([load_user_data(f"user_data/{f}") for f in user_files], ignore_index=True)
        return user_data_all, '全体'
    else:
        user_file = f"user_data/{selected_user_label}.csv"
        return load_user_data(user_file), selected_user_label

# アプリの設定
product_data = load_product_data()
user_data, user_id = select_user()
similarity_data = load_similarity_data()  # similarity_data を読み込む

# ユーザーIDに基づく表示名設定
if user_id == '全体':
    user_name = '全体'
else:
    user_name = f"ユーザー{user_id}"

# サイドバーでページ選択
st.sidebar.title(f"🛒  メニュー")
page = st.sidebar.radio("ページを選択", ["個別レコメンド（全体では使用不可）", "利用分析", "過去購入商品検索"])

# ページ表示
if page == "個別レコメンド（全体では使用不可）":
    recommend_page(product_data, user_data, user_id)
elif page == "利用分析":
    analytics_page(product_data, user_data, similarity_data)  # similarity_data を渡す
elif page == "過去購入商品検索":
    search_page(product_data, user_data, user_id)
