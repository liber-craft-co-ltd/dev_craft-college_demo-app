import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pandas as pd
from difflib import get_close_matches

# 協調フィルタリングの実装
def collaborative_filtering(user_data, product_data, user_id):
    # ユーザーごとの購入商品データをピボットテーブル化
    user_product_matrix = user_data.pivot_table(index='ユーザーID', columns='商品ID', values='購入回数', fill_value=0)

    # ユーザー間のコサイン類似度を計算
    similarity_matrix = cosine_similarity(user_product_matrix)

    # ユーザーIDに基づいてそのユーザーのインデックスを取得
    user_index = user_product_matrix.index.get_loc(user_id)

    # 類似ユーザーを見つける
    similar_users = similarity_matrix[user_index]

    # 類似度が高い順に並べ替え（最初の1つは自分なので2番目以降を選択）
    similar_users_indices = similar_users.argsort()[-11:-1][::-1]

    # 類似ユーザーが購入した商品を推薦する
    recommended_products = user_product_matrix.iloc[similar_users_indices].sum(axis=0).sort_values(ascending=False)

    # 商品情報をマージして商品名を表示
    recommended_product_ids = recommended_products.index
    recommended_products_info = product_data[product_data['商品ID'].isin(recommended_product_ids)]

    return recommended_products_info[['商品ID', '商品名', 'カテゴリ', '価格']].head(10)

# レコメンドページの構築
def recommend_page(product_data, user_data, user_id=None):
    st.title("🛍️ 商品おすすめ")

    # 購入回数をカウント
    user_data['購入回数'] = user_data.groupby(['ユーザーID', '商品ID'])['購入日時'].transform('count')
    user_data = user_data.drop_duplicates(subset=['ユーザーID', '商品ID'])

    # 商品名をuser_dataにマージ
    user_data = user_data.merge(product_data[['商品ID', '商品名']], on='商品ID', how='left')

    # カテゴリ選択
    category_option = st.selectbox("表示する情報を選択してください", ["購入履歴からのおすすめ", "他の人がよく買った商品をおすすめ", "商品名検索", "購入回数の多い商品"])

    # 購入履歴からのレコメンド
    if category_option == "購入履歴からのおすすめ":
        st.subheader("🛒 購入履歴からのおすすめ")
        user_data["ID_商品名"] = user_data["商品ID"].astype(str) + " - " + user_data["商品名"]
        selected_product_id = st.selectbox("購入商品を選択", user_data["ID_商品名"].unique())
        if selected_product_id:
            selected_id = int(selected_product_id.split(" - ")[0])
            selected_product = product_data[product_data["商品ID"] == selected_id].iloc[0]
            st.write(f"**選択した商品:** {selected_product['商品名']} (カテゴリ: {selected_product['カテゴリ']}, 価格: {selected_product['価格']}円)")

            # 商品カテゴリを基に類似商品を推薦
            category_recommendations = product_data[product_data["カテゴリ"] == selected_product["カテゴリ"]]
            st.subheader("📌 類似商品")
            st.dataframe(category_recommendations[["商品名", "価格"]].head(10))

            # 価格帯を考慮したレコメンド
            price_range = (selected_product["価格"] - 1000, selected_product["価格"] + 1000)
            price_recommendations = product_data[(product_data["価格"] >= price_range[0]) & 
                                                 (product_data["価格"] <= price_range[1]) & 
                                                 (product_data["商品ID"] != selected_id)]
            st.subheader("💰 価格が近い商品")
            st.dataframe(price_recommendations[["商品名", "価格"]].head(10))

    # 商品名検索によるレコメンド
    elif category_option == "商品名検索":
        st.subheader("🔍 商品名でレコメンド")
        search_query = st.text_input("商品名を入力してください")
        if search_query:
            product_names = product_data["商品名"].tolist()
            
            # 部分一致を含む商品名の検索
            matches = get_close_matches(search_query, product_names, n=5, cutoff=0)
            
            # 商品名の部分一致に加え、カテゴリ一致もレコメンド
            matched_products = product_data[product_data['商品名'].isin(matches)]
            category_match_products = product_data[product_data['カテゴリ'].str.contains(search_query, na=False, case=False)]
            recommended_products = pd.concat([matched_products, category_match_products]).drop_duplicates()

            if not recommended_products.empty:
                st.write(f"**検索結果**: {len(recommended_products)}件の商品が見つかりました。")
                st.subheader("📌 類似商品")
                st.dataframe(recommended_products[["商品名", "価格", "カテゴリ"]].head(10))
            else:
                st.write("該当する商品が見つかりませんでした。")
    # elif category_option == "商品名検索でレコメンド":
    #     st.subheader("🔍 商品名検索")
    #     search_term = st.text_input("商品名またはカテゴリ名を入力してください")
        
    #     if search_term:
    #         # 商品名での検索
    #         product_search_results = product_data[product_data['商品名'].str.contains(search_term, case=False)]
    #         # カテゴリ名での検索（カテゴリ名に対しても部分一致検索）
    #         category_search_results = product_data[product_data['カテゴリ'].str.contains(search_term, case=False)]
        
    #         # 商品名とカテゴリの検索結果を結合
    #         search_results = pd.concat([product_search_results, category_search_results]).drop_duplicates()
        
    #         st.dataframe(search_results[["商品名", "カテゴリ", "価格"]].head(10))

    # 購入回数の多い商品
    elif category_option == "購入回数の多い商品":
        st.subheader("📈 購入回数が多い商品")
        popular_products = product_data.merge(user_data.groupby('商品ID').size().reset_index(name='購入回数'), on='商品ID')
        popular_products = popular_products.sort_values(by='購入回数', ascending=False)
        st.dataframe(popular_products[["商品名", "購入回数", "価格"]].head(10))


    # 他の人がよく買った商品をおすすめ
    elif category_option == "他の人がよく買った商品をおすすめ":
        st.subheader("🔮 他の人がよく買った商品")
        try:
            recommended_products = collaborative_filtering(user_data, product_data, user_id)
            st.dataframe(recommended_products)
        except Exception as e:
            st.error("「全体」ではこの機能は使えません。")



# def recommend_page(product_data, user_data, user_id=None):
#     # ユーザーIDが指定された場合、フィルタリング
#     if user_id != '全体' and user_id is not None:
#         user_data = user_data[user_data['ユーザーID'] == int(user_id)]

#     st.markdown("""
#         <style>
#             .main { background-color: #f8f9fa; }
#             .stTitle { font-size: 24px; font-weight: bold; color: #333366; }
#             .stSubtitle { font-size: 20px; font-weight: bold; color: #666688; }
#             .stDataFrame { border-radius: 10px; }
#         </style>
#     """, unsafe_allow_html=True)

#     st.title("🛍️ 商品おすすめ")

#     # 購入回数をカウント
#     user_data['購入回数'] = user_data.groupby(['ユーザーID', '商品ID'])['購入日時'].transform('count')
#     user_data = user_data.drop_duplicates(subset=['ユーザーID', '商品ID'])

#     # 商品名をuser_dataにマージ
#     user_data = user_data.merge(product_data[['商品ID', '商品名']], on='商品ID', how='left')

#     # カテゴリ選択
#     category_option = st.selectbox("表示する情報を選択してください", ["購入履歴からのおすすめ", "商品名検索でレコメンド", "購入回数の多い商品"])

#     # 購入履歴からのレコメンド
#     if category_option == "購入履歴からのおすすめ":
#         st.subheader("🛒 購入履歴からのおすすめ")
#         user_data["ID_商品名"] = user_data["商品ID"].astype(str) + " - " + user_data["商品名"]
#         selected_product_id = st.selectbox("購入商品を選択", user_data["ID_商品名"].unique())
#         if selected_product_id:
#             selected_id = int(selected_product_id.split(" - ")[0])
#             selected_product = product_data[product_data["商品ID"] == selected_id].iloc[0]
#             st.write(f"**選択した商品:** {selected_product['商品名']} (カテゴリ: {selected_product['カテゴリ']}, 価格: {selected_product['価格']}円)")

#             # 商品カテゴリを基に類似商品を推薦
#             category_recommendations = product_data[product_data["カテゴリ"] == selected_product["カテゴリ"]]
#             st.subheader("📌 類似商品")
#             st.dataframe(category_recommendations[["商品名", "価格"]].head(10))

#             # 価格帯を考慮したレコメンド
#             price_range = (selected_product["価格"] - 1000, selected_product["価格"] + 1000)
#             price_recommendations = product_data[(product_data["価格"] >= price_range[0]) & 
#                                                  (product_data["価格"] <= price_range[1]) & 
#                                                  (product_data["商品ID"] != selected_id)]
#             st.subheader("💰 価格が近い商品")
#             st.dataframe(price_recommendations[["商品名", "価格"]].head(10))
            
#     # 商品名検索でのレコメンド
#     elif category_option == "商品名検索でレコメンド":
#         st.subheader("🔍 商品名でレコメンド")
#         search_query = st.text_input("商品名を入力してください")
#         if search_query:
#             product_names = product_data["商品名"].tolist()
            
#             # 部分一致を含む商品名の検索
#             matches = get_close_matches(search_query, product_names, n=5, cutoff=0)
            
#             # 商品名の部分一致に加え、カテゴリ一致もレコメンド
#             matched_products = product_data[product_data['商品名'].isin(matches)]
#             category_match_products = product_data[product_data['カテゴリ'].str.contains(search_query, na=False, case=False)]
#             recommended_products = pd.concat([matched_products, category_match_products]).drop_duplicates()

#             if not recommended_products.empty:
#                 st.write(f"**検索結果**: {len(recommended_products)}件の商品が見つかりました。")
#                 st.subheader("📌 類似商品")
#                 st.dataframe(recommended_products[["商品名", "価格", "カテゴリ"]].head(10))
#             else:
#                 st.write("該当する商品が見つかりませんでした。")

#     elif category_option == "購入回数の多い商品":
#         st.subheader("🔥 購入回数の多い商品")
#         popular_products = user_data["商品ID"].value_counts().reset_index()
#         popular_products.columns = ["商品ID", "購入回数"]
#         popular_products = popular_products.merge(product_data, on="商品ID").head(10)
#         st.dataframe(popular_products[["商品名", "価格", "購入回数"]])
