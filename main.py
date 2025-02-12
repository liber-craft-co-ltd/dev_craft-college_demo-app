import streamlit as st
import pandas as pd
import os
from modules.recommend import recommend_page
from modules.analyze import analytics_page
from modules.search import search_page

# データ読み込み
@st.cache_data
def load_product_data():
    return pd.read_csv("data/product_data.csv")

@st.cache_data
def load_user_data(user_file):
    return pd.read_csv(user_file)

# ユーザー選択
def select_user():
    # ファイルリストを取得
    user_files = sorted([f for f in os.listdir("data/user_data") if f.endswith('.csv')])

    # ファイル名から番号と苗字を抽出してリストを作成
    user_labels = [f.replace('.csv', '') for f in user_files]  # 例: "1.山田"

    # 数字順に並べ替え
    user_labels.sort(key=lambda x: int(x.split('.')[0]))  # 「1.山田」のように数字を基準にソート
    
    # 「全体」の選択肢を追加
    user_labels.insert(0, '全体')  # '全体'をリストの一番上に挿入

    # ユーザーを選択
    selected_user_label = st.sidebar.selectbox("ユーザーを選択", user_labels)

    if selected_user_label == '全体':
        # 全ユーザーデータを結合して返す
        user_data_all = pd.concat([load_user_data(f"data/user_data/{f}") for f in user_files], ignore_index=True)
        return user_data_all, '全体'
    else:
        # 選択されたユーザーファイルを読み込む
        user_file = f"data/user_data/{selected_user_label}.csv"
        return load_user_data(user_file), selected_user_label


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
        /* ベースデザイン */
        body {
            font-family: 'Roboto', sans-serif;
            color: #333;
        }

        /* サイドバーのデザイン */
        .css-1d391kg {
            background-color: #ffffff;  /* ライトモード背景色 */
            padding: 20px;
            border-radius: 10px;
        }

        .css-1d391kg h1, .css-1d391kg h2 {
            font-family: 'Arial', sans-serif;
            color: #ff7f50;  /* オレンジ色 */
        }

        .css-1d391kg select {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #fff;
            color: #333;
        }

        .stButton {
            background-color: #ff7f50;  /* オレンジ */
            color: white;
            border-radius: 5px;
            font-weight: 500;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
        }

        .stButton:hover {
            background-color: #ff4500;  /* ホバー時 */
        }

        /* ダークモード用のCSS */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #121212;  /* ダークモード背景色 */
                color: #fff;
            }

            .css-1d391kg {
                background-color: #2c2f36;  /* ダークモードサイドバー */
            }

            .css-1d391kg h1, .css-1d391kg h2 {
                color: #ff7f50;  /* オレンジ色 */
            }

            .stButton {
                background-color: #ff7f50;  /* オレンジ */
                color: white;
                border-radius: 5px;
                font-weight: 500;
                padding: 12px 20px;
                font-size: 16px;
                border: none;
            }

            .stButton:hover {
                background-color: #ff4500;  /* ホバー時 */
            }

            .stSelectbox, .stRadio {
                background-color: #333;
                color: #fff;
                border-radius: 5px;
                padding: 10px;
            }

            .stDataFrame {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }

            .stDataFrame th, .stDataFrame td {
                padding: 12px;
                text-align: left;
                color: #fff;
            }

            .stDataFrame th {
                background-color: #ff7f50;  /* ヘッダーにオレンジ色 */
                font-weight: bold;
            }

            .stDataFrame tr:nth-child(even) {
                background-color: #333;
            }

            .stDataFrame tr:nth-child(odd) {
                background-color: #2a2a2a;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# サイドバーでページ選択
st.sidebar.title(f"🛒  メニュー")
page = st.sidebar.radio("ページを選択", ["個別レコメンド（全体では使用不可）", "利用分析", "過去購入商品検索"])

# ページ表示
if page == "個別レコメンド（全体では使用不可）":
    recommend_page(product_data, user_data, user_id)
elif page == "利用分析":
    analytics_page(product_data, user_data)
elif page == "過去購入商品検索":
    search_page(product_data, user_data, user_id)
