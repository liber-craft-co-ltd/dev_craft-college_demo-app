import numpy as np
import pandas as pd
import streamlit as st
import os

# 商品類似度の読み込み recommend_based_on_similarityで使用
def load_product_similarity():
    return pd.read_csv("product_data/product_similarity.csv")

# 購入履歴に基づいて関連商品をおすすめ
def recommend_based_on_similarity(user_data, product_data, user_id, top_n=10):
    # 商品類似度データを読み込み
    product_similarity = load_product_similarity()

    # ユーザーが購入した商品IDを取得
    purchased_products = user_data[user_data['ユーザーID'] == user_id]['商品ID'].unique()

    # ユーザーが購入していない関連商品を抽出
    related_products = product_similarity[product_similarity['商品名1'].isin(
        product_data[product_data['商品ID'].isin(purchased_products)]['商品名']
    )]

    # 商品IDを取得するためにマージ
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')

    # 既に購入された商品を除外
    related_products = related_products[~related_products['商品ID'].isin(purchased_products)]

    # 類似度スコアで並べ替えてTop Nを返す
    recommended = related_products[['商品ID', '商品名2', 'カテゴリ', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)

    return recommended.rename(columns={'商品名2': '商品名'})

# カテゴリ別のおすすめ商品を表示
def recommend_based_on_category(user_data, product_data, user_id, selected_category, top_n=5):
    # ユーザーが購入した商品を取得
    purchased_products = user_data[user_data['ユーザーID'] == user_id]['商品ID'].unique()

    # 選択されたカテゴリに基づいて、関連商品を抽出
    category_products = product_data[product_data['カテゴリ'] == selected_category]

    # 既に購入した商品を除外
    category_products = category_products[~category_products['商品ID'].isin(purchased_products)]

    # 商品類似度に基づいて関連商品を取得
    product_similarity = load_product_similarity()
    related_products = product_similarity[product_similarity['商品名1'].isin(category_products['商品名'])]

    # 商品IDを取得するためにマージ
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')

    # 同じカテゴリの商品のみを選択
    related_products = related_products[related_products['カテゴリ'] == selected_category]

    # 類似度スコアで並べ替えてTop Nを返す
    recommended = related_products[['商品ID', '商品名2', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)

    # 商品名2の列名を商品名に変更し、関連度を除外して返す
    return recommended.rename(columns={'商品名2': '商品名'}).drop(columns=['関連度'])


# ファイル名からユーザーIDを抽出
def extract_user_id_from_filename(filename):
    # ファイル名からユーザーIDを抽出 (例: "1.山田.csv" -> "1")
    user_id = os.path.basename(filename).split('.')[0]

    # '全体'の場合はNoneを返す
    if user_id == '全体':
        return '全体'
    
    # ユーザーIDを整数として返す
    return int(user_id)

def recommend_based_on_searched_product(product_data, search_product, top_n=5):
    # 商品類似度データを読み込み
    product_similarity = load_product_similarity()

    # 関連商品の取得
    related_products = product_similarity[product_similarity['商品名1'] == search_product]

    # 商品IDを取得するためにマージ
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')

    # 類似度スコアで並べ替えてTop Nを返す
    recommended = related_products[['商品ID', '商品名2', 'カテゴリ', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)

    return recommended.rename(columns={'商品名2': '商品名'})

# 商品おすすめページ
def recommend_page(product_data, user_data, filename):
    # ファイル名からユーザーIDを抽出
    user_id = extract_user_id_from_filename(filename)

    st.title("🛍️ 商品おすすめ")

    if user_id in [None, '全体']:
        st.subheader("🔄 全体のデータに基づくレコメンド")
        st.write("個別ユーザーのレコメンドはユーザーを選択してください。")
    else:
        st.subheader(f"👤 あなたの購入履歴に基づくレコメンド  \n(過去購入した商品を除く)")

        # 商品類似度に基づくレコメンド
        st.subheader("🔗 購入履歴からのおすすめ商品")
        recommended_products = recommend_based_on_similarity(user_data, product_data, user_id)

        if recommended_products.empty:
            st.write("商品が見つかりませんでした。")
        else:
            st.dataframe(recommended_products[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']].reset_index(drop=True))

        # カテゴリ選択
        st.subheader("🔗 カテゴリ別おすすめ商品 \n(過去購入した商品を除く)")

        # カテゴリのリストを取得
        available_categories = product_data['カテゴリ'].unique()

        # カテゴリ選択のドロップダウン
        selected_category = st.selectbox("カテゴリを選択してください", available_categories)

        if selected_category:
            st.write(f"🔗 「{selected_category}」カテゴリのおすすめ商品")

            # カテゴリ別おすすめを取得
            recommended_category_products = recommend_based_on_category(user_data, product_data, user_id, selected_category)

            if recommended_category_products.empty:
                st.write("カテゴリ別の商品が見つかりませんでした。")
            else:
                st.dataframe(recommended_category_products[['商品ID', '商品名', '価格']].reset_index(drop=True))

    # 購入商品の検索機能
    st.subheader("🔎 購入履歴からのおすすめ商品 \n（過去購入した商品を含む)")
    user_purchased_products = user_data[user_data['ユーザーID'] == user_id].merge(product_data, on='商品ID')['商品名'].unique()

    if len(user_purchased_products) > 0:
        selected_product = st.selectbox("購入した商品を検索", user_purchased_products)
        if selected_product:
            st.write(f"🔗 「{selected_product}」を購入者への商品のおすすめ (Top 5) ")
            recommended_searched = recommend_based_on_searched_product(product_data, selected_product)

            if recommended_searched.empty:
                st.write("関連商品が見つかりませんでした。")
            else:
                st.dataframe(recommended_searched[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']].reset_index(drop=True))
    else:
        st.write("過去の購入履歴がありません。")
