import streamlit as st
import pandas as pd
import os
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
    user_ids = [int(f.split("_")[1].split(".")[0]) for f in user_files if f.endswith('.csv')]  # .csvファイルだけを対象
    
    # 「全体」の選択肢を追加
    user_ids.append('全体')
    selected_user_id = st.sidebar.selectbox("ユーザーを選択", user_ids)
    
    # 「全体」の場合、全ユーザーデータを結合して返す
    if selected_user_id == '全体':
        # ユーザーデータを全て結合する
        user_data_all = pd.concat([load_user_data(f"data/user_data/user_{user_id}.csv") for user_id in user_ids[:-1]], ignore_index=True)
        return user_data_all, '全体'
    else:
        user_file = f"data/user_data/user_{selected_user_id}.csv"
        return load_user_data(user_file), selected_user_id

# カテゴリ別の人気商品ランキング
def category_popularity_ranking(product_data, user_data):
    st.subheader("📊 カテゴリごとの購入商品ランキング")
    
    # ユーザー全体のデータから購入回数を集計
    category_ranking = user_data.merge(product_data, on="商品ID")
    
    # カテゴリごとに商品IDの購入回数をカウント
    category_ranking = category_ranking.groupby(['カテゴリ', '商品ID']).size().reset_index(name="購入回数")
    
    # カテゴリ選択ボックス
    selected_category = st.selectbox("カテゴリを選択", category_ranking['カテゴリ'].unique())
    
    # 選択されたカテゴリのデータをフィルタリング
    category_data = category_ranking[category_ranking['カテゴリ'] == selected_category]
    
    # 人気順に並べ替え
    category_data = category_data.sort_values(by="購入回数", ascending=False).head(10)
    
    # 商品名を結合して表示
    category_data = category_data.merge(product_data[['商品ID', '商品名']], on='商品ID')
    
    st.dataframe(category_data[['商品名', '購入回数']])

# アプリの設定
product_data = load_product_data()
user_data, user_id = select_user()

# ユーザーIDに基づく表示名設定
if user_id == '全体':
    user_name = '全体'
else:
    user_name = f"ユーザー{user_id}"

# サイドバーのカスタマイズ
st.markdown("""
    <style>
        /* サイドバーの背景色 */
        .css-1d391kg {background-color: #ffffff; padding: 15px;}
        /* サイドバータイトル */
        .css-1d391kg h1 {font-family: 'Helvetica', sans-serif; color: #333; font-size: 24px; margin-top: 0;}
        /* サイドバーサブタイトル */
        .css-1d391kg h2 {font-family: 'Helvetica', sans-serif; color: #666; font-size: 18px;}
        /* サイドバー選択ボックスのデザイン */
        .stSelectbox {border-radius: 5px; border: 1px solid #ddd; padding: 10px;}
        .stRadio {border-radius: 5px; border: 1px solid #ddd; padding: 10px;}
        /* サイドバーのボタンデザイン */
        .stButton {background-color: #007BFF; color: white; border-radius: 5px; font-weight: 500;}
        
        /* ラジオボタン選択された項目に色を付ける */
        .stRadio label[data-baseweb="radio"] input:checked + div {
            background-color: #007BFF; /* 選択時の背景色 */
            color: white; /* 選択時の文字色 */
        }
    </style>
    """, unsafe_allow_html=True)

# サイドバーでページ選択
st.sidebar.title(f"🛒 {user_name} メニュー")
page = st.sidebar.radio("ページを選択", ["レコメンド", "利用分析", "カテゴリ別人気商品"])

# ページ表示
if page == "レコメンド":
    recommend_page(product_data, user_data, user_id)
elif page == "利用分析":
    analytics_page(product_data, user_data)
elif page == "カテゴリ別人気商品":
    category_popularity_ranking(product_data, user_data)
