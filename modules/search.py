import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pandas as pd
from difflib import get_close_matches

# レコメンドページの構築
def search_page(product_data, user_data, user_id=None):
    st.title("🔍 商品名検索")
    # 商品名検索によるレコメンド
    # if category_option == "商品名検索":
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