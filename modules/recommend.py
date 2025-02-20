import streamlit as st
import pandas as pd
import os

# データ読み込み
@st.cache_data
def load_user_data(user_file):
    return pd.read_csv(user_file)

def load_all_user_data():
    user_files = sorted([f for f in os.listdir("user_data/") if f.endswith('.csv')])
    user_data_all = pd.concat([load_user_data(f"user_data/{f}") for f in user_files], ignore_index=True)
    return user_data_all

# 商品類似度の読み込み
def load_product_similarity():
    return pd.read_csv("product_data/product_similarity.csv")

# 購入履歴に基づいて関連商品をおすすめ
def recommend_based_on_similarity(user_data, product_data, user_id, top_n=10):
    product_similarity = load_product_similarity()
    purchased_products = user_data[user_data['ユーザーID'] == user_id]['商品ID'].unique()
    related_products = product_similarity[product_similarity['商品名1'].isin(
        product_data[product_data['商品ID'].isin(purchased_products)]['商品名']
    )]

    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')
    related_products = related_products[~related_products['商品ID'].isin(purchased_products)]
    
    recommended = related_products[['商品ID', '商品名2', 'カテゴリ', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)
    return recommended.rename(columns={'商品名2': '商品名'})

# 選択した商品に基づいて関連商品を取得
def recommend_based_on_similarity_from_product(selected_product, top_n=10):
    product_similarity = load_product_similarity()
    related_products = product_similarity[product_similarity['商品名1'] == selected_product]

    recommended = related_products.sort_values('関連度', ascending=False).head(top_n)
    return recommended[['商品名2', '関連度']].rename(columns={'商品名2': '商品名'})

# カテゴリ別のおすすめ商品を表示
def recommend_based_on_category(user_data, product_data, user_id, selected_category, top_n=5):
    purchased_products = user_data[user_data['ユーザーID'] == user_id]['商品ID'].unique()
    category_products = product_data[product_data['カテゴリ'] == selected_category]
    category_products = category_products[~category_products['商品ID'].isin(purchased_products)]

    product_similarity = load_product_similarity()
    related_products = product_similarity[product_similarity['商品名1'].isin(category_products['商品名'])]
    related_products = related_products.merge(product_data, left_on='商品名2', right_on='商品名')
    related_products = related_products[related_products['カテゴリ'] == selected_category]

    recommended = related_products[['商品ID', '商品名2', '価格', '関連度']].sort_values('関連度', ascending=False).head(top_n)
    return recommended.rename(columns={'商品名2': '商品名'}).drop(columns=['関連度'])

def recommend_page(product_data):
    st.title("🛍️ 商品おすすめ")

    # ユーザー選択のドロップダウン
    user_data = load_all_user_data()  # 全ユーザーデータを取得
    user_ids = user_data['ユーザーID'].unique()

    # ユーザー名をファイル名から取得し、数字順でソート
    user_files = sorted([f for f in os.listdir("user_data/") if f.endswith('.csv')],
                        key=lambda x: int(x.split('.')[0]))
    user_labels = [f.replace('.csv', '') for f in user_files]  # 「1.山田」の形式

    selected_user_id = st.selectbox("ユーザーを選択してください", user_labels)

    # ユーザーIDの取得
    selected_user_id_value = int(selected_user_id.split('.')[0])

    if selected_user_id_value in [None, '全体']:
        st.subheader("🔄 全体のデータに基づくレコメンド")
        st.write("個別ユーザーのレコメンドはユーザーを選択してください。")
    else:
        st.subheader(f"👤 あなたの購入履歴に基づくレコメンド  \n(過去購入した商品を除く)")

        # 商品類似度に基づくレコメンド
        st.subheader("🔗 購入履歴からのおすすめ商品")
        recommended_products = recommend_based_on_similarity(user_data, product_data, selected_user_id_value)

        if recommended_products.empty:
            st.write("商品が見つかりませんでした。")
        else:
            st.dataframe(recommended_products[['商品ID', '商品名', 'カテゴリ', '価格', '関連度']].reset_index(drop=True))

        # カテゴリ選択
        st.subheader("🔗 カテゴリ別おすすめ商品 \n(過去購入した商品を除く)")

        available_categories = product_data['カテゴリ'].unique()
        selected_category = st.selectbox("カテゴリを選択してください", available_categories)

        if selected_category:
            st.write(f"🔗 「{selected_category}」カテゴリのおすすめ商品")
            recommended_category_products = recommend_based_on_category(user_data, product_data, selected_user_id_value, selected_category)

            if recommended_category_products.empty:
                st.write("カテゴリ別の商品が見つかりませんでした。")
            else:
                st.dataframe(recommended_category_products[['商品ID', '商品名', '価格']].reset_index(drop=True))

    # 購入商品の検索機能
    st.subheader("🔎 購入履歴からのおすすめ商品 \n（過去購入した商品を含む)")

    user_purchased_products = user_data[user_data['ユーザーID'] == selected_user_id_value].merge(product_data, on='商品ID')['商品名'].unique()

    if len(user_purchased_products) > 0:
        selected_product = st.selectbox("購入した商品を検索", user_purchased_products)
        if selected_product:
            st.write(f"🔗 「{selected_product}」を購入者への商品のおすすめ (Top 10)")

            # 選択した商品に基づいて関連商品をおすすめ
            recommended_searched = recommend_based_on_similarity_from_product(selected_product)

            if recommended_searched.empty:
                st.write("関連商品が見つかりませんでした。")
            else:
                st.dataframe(recommended_searched.reset_index(drop=True))
    else:
        st.write("過去の購入履歴がありません。")
