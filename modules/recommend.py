import numpy as np
import pandas as pd
import streamlit as st

def load_product_similarity():
    return pd.read_csv("data/product_similarity.csv")

def recommend_based_on_similarity(user_data, product_data, user_id, top_n=10):
    # Load product similarity data
    product_similarity = load_product_similarity()

    # Get user's purchased product IDs
    purchased_products = user_data[user_data['ユーザーID'] == user_id]['商品ID'].unique()

    # Find related products the user hasn't purchased
    related_products = product_similarity[product_similarity['商品名1'].isin(
        product_data[product_data['商品ID'].isin(purchased_products)]['商品名']
    )]

    # Merge to get Product IDs
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')

    # Remove already purchased products
    related_products = related_products[~related_products['商品ID'].isin(purchased_products)]

    # Rank by similarity score and return top N
    recommended = related_products[['商品ID', '商品名2', 'カテゴリ', '価格', '関連度']]\
        .sort_values('関連度', ascending=False).head(top_n)

    return recommended.rename(columns={'商品名2': '商品名'})

def recommend_page(product_data, user_data, user_id):
    st.title("🛍️ 商品おすすめ")

    if user_id in [None, '全体']:
        st.subheader("🔄 全体のデータに基づくレコメンド")
        st.write("個別ユーザーのレコメンドはユーザーを選択してください。")
    else:
        st.subheader(f"👤 ユーザー {user_id} に基づくレコメンド")

        # 商品類似度に基づくレコメンド
        st.subheader("🔗 購入履歴からの関連商品おすすめ")
        recommended_products = recommend_based_on_similarity(user_data, product_data, user_id)
        
        if recommended_products.empty:
            st.write("関連商品が見つかりませんでした。")
        else:
            st.dataframe(recommended_products[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']].set_index('商品ID'))
