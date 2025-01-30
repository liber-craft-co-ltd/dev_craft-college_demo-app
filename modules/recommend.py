import streamlit as st

def recommend_page(product_data, user_data):
    st.title("レコメンドページ")

    # ユーザーの購入履歴
    st.subheader("購入履歴")
    st.write(user_data)

    # 購入商品の選択
    st.subheader("購入商品を選択")
    selected_product_id = st.selectbox("購入商品を選択", user_data["商品ID"].unique())

    if selected_product_id:
        # 選択した商品の情報
        selected_product = product_data[product_data["商品ID"] == selected_product_id].iloc[0]
        st.write(f"選択した商品: {selected_product['商品名']} (カテゴリ: {selected_product['カテゴリ']}, 価格: {selected_product['価格']}円)")

        # レコメンドロジック
        category = selected_product["カテゴリ"]
        price_range = (selected_product["価格"] - 1000, selected_product["価格"] + 1000)

        recommendations = product_data[
            (product_data["カテゴリ"] == category) &
            (product_data["価格"] >= price_range[0]) &
            (product_data["価格"] <= price_range[1]) &
            (product_data["商品ID"] != selected_product_id)
        ]

        st.subheader("おすすめ商品")
        st.dataframe(recommendations[["商品名", "カテゴリ", "価格"]].head(10))