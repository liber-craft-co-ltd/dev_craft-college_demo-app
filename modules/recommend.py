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
    recommended = related_products[['商品ID', '商品名2', 'カテゴリ', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)

    return recommended.rename(columns={'商品名2': '商品名'})

def recommend_based_on_searched_product(product_data, search_product, top_n=5):
    # Load product similarity data
    product_similarity = load_product_similarity()

    # Get related products
    related_products = product_similarity[product_similarity['商品名1'] == search_product]

    # Merge to get Product IDs
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')

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
            st.dataframe(recommended_products[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']])

    # 🔍 **購入商品の検索機能**
    st.subheader("🔎 購入商品の検索 & 関連商品のおすすめ")
    user_purchased_products = user_data[user_data['ユーザーID'] == user_id].merge(product_data, on='商品ID')['商品名'].unique()

    if len(user_purchased_products) > 0:
        selected_product = st.selectbox("購入した商品を検索", user_purchased_products)
        if selected_product:
            st.write(f"**🔗 関連商品のおすすめ (Top 5) for 「{selected_product}」**")
            recommended_searched = recommend_based_on_searched_product(product_data, selected_product)

            if recommended_searched.empty:
                st.write("関連商品が見つかりませんでした。")
            else:
                st.dataframe(recommended_searched[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']])
    else:
        st.write("過去の購入履歴がありません。")
