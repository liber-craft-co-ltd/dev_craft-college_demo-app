# modules/category_popularity.py

import pandas as pd
import streamlit as st

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
