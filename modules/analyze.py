import streamlit as st
import pandas as pd
import altair as alt

def analytics_page(product_data, user_data):
    st.title("利用分析")

    # 購入カテゴリ分析
    st.subheader("カテゴリ別購入数")
    purchased_products = product_data[product_data["商品ID"].isin(user_data["商品ID"])]
    category_count = purchased_products["カテゴリ"].value_counts().reset_index()
    category_count.columns = ["カテゴリ", "購入数"]

    category_chart = alt.Chart(category_count).mark_bar().encode(
        x="カテゴリ",
        y="購入数",
        tooltip=["カテゴリ", "購入数"]
    )
    st.altair_chart(category_chart, use_container_width=True)

    # 購入金額の分布
    st.subheader("購入金額の分布")
    price_distribution = purchased_products["価格"]
    st.write(f"平均購入金額: {price_distribution.mean():.2f}円")
    st.write(f"最大購入金額: {price_distribution.max()}円")
    st.write(f"最小購入金額: {price_distribution.min()}円")
    
    price_chart = alt.Chart(purchased_products).mark_bar().encode(
        alt.X("価格", bin=True),
        alt.Y("count()", title="購入数"),
        tooltip=["count()", "sum(価格)"]
    )
    st.altair_chart(price_chart, use_container_width=True)

    # リピート購入がある商品の商品IDと購入回数
    st.subheader("リピート購入がある商品の商品IDと購入回数")
    # 商品IDごとにグループ化して購入回数をカウント
    repeat_purchase = user_data.groupby("商品ID").size().reset_index(name="購入回数")
    # 購入回数が2回以上の商品のみ抽出
    repeat_purchase = repeat_purchase[repeat_purchase["購入回数"] > 1]
    # 商品IDと購入回数の表示
    repeat_purchase_info = repeat_purchase[["商品ID", "購入回数"]]
    st.dataframe(repeat_purchase_info)

    # 購入サイクルの分析
    st.subheader("購入サイクル分析")

    # 日付を datetime 型に変換
    user_data["購入日時"] = pd.to_datetime(user_data["購入日時"])

    # ユーザーIDごとに購入日時でソート  
    user_data = user_data.sort_values(by=["ユーザーID", "購入日時"])

    # 購入間隔（前回購入との日数差）
    user_data["購入間隔"] = user_data.groupby("ユーザーID")["購入日時"].diff().dt.days

    # NaN（最初の購入データ）を除外
    user_data = user_data.dropna(subset=["購入間隔"])
    # 購入間隔の平均と中央値を計算
    avg_purchase_interval = user_data["購入間隔"].mean()
    median_purchase_interval = user_data["購入間隔"].median()

    # 結果を表示
    st.write(f"平均購入間隔: {avg_purchase_interval:.2f}日")
    st.write(f"中央値購入間隔: {median_purchase_interval}日")
    
    # 購入間隔のヒストグラム
    interval_chart = alt.Chart(user_data).mark_bar().encode(
        alt.X("購入間隔", bin=alt.Bin(maxbins=30), title="購入間隔（日）"),
        alt.Y("count()", title="購入間隔の頻度"),
        tooltip=["count()", "mean(購入間隔)"]
        )
    st.altair_chart(interval_chart, use_container_width=True)


    # 月別トレンド分析
    st.subheader("月別購入数分析")
    user_data["購入月"] = user_data["購入日時"].dt.month
    monthly_trends = user_data.groupby("購入月").size().reset_index(name="購入数")

    trend_chart = alt.Chart(monthly_trends).mark_line(point=True).encode(
        x="購入月:O",
        y="購入数",
        tooltip=["購入月", "購入数"]
    )
    st.altair_chart(trend_chart, use_container_width=True)
    
        # 購入回数の多い商品
    st.subheader("📈 購入回数が多い商品")
    popular_products = product_data.merge(user_data.groupby('商品ID').size().reset_index(name='購入回数'), on='商品ID')
    popular_products = popular_products.sort_values(by='購入回数', ascending=False)
    st.dataframe(popular_products[["商品名", "購入回数", "価格"]].head(10))

    
# 商品数はカテゴリによってことなるので、正規化する必要あるかも。。。