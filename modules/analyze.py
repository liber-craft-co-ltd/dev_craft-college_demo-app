import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import os

def load_user_data(file_path):
    return pd.read_csv(file_path)

def load_all_user_data():
    user_files = sorted([f for f in os.listdir("user_data/") if f.endswith('.csv')])
    user_data_frames = [load_user_data(f"user_data/{f}") for f in user_files]
    return pd.concat(user_data_frames, ignore_index=True)

def analytics_page(product_data, similarity_data):
    st.title("利用分析")

    # ユーザー選択
    user_files = sorted([f for f in os.listdir("user_data/") if f.endswith('.csv')])
    user_labels = [f.replace('.csv', '') for f in user_files]
    user_labels.sort(key=lambda x: int(x.split('.')[0]))
    user_labels.insert(0, '全体')
    selected_user_label = st.selectbox("ユーザーを選択", user_labels)

    if selected_user_label == '全体':
        user_data = load_all_user_data()  # 全ユーザーのデータを読み込む
    else:
        user_file = f"user_data/{selected_user_label}.csv"
        user_data = load_user_data(user_file)

    analysis_options = [
        "カテゴリ別購入数",
        "購入金額の分布",
        "購入サイクル分析",
        "月別購入数分析",
        "購入回数が多い商品",
        "関連度の高い商品",
        "商品購入トレンド予測",
    ]
    
    selected_analysis = st.selectbox("分析項目を選択", analysis_options)

    # 購入した商品のデータを取得
    purchased_products = product_data[product_data["商品ID"].isin(user_data["商品ID"])]

    # カテゴリ別購入数
    if selected_analysis == "カテゴリ別購入数":
        st.subheader("カテゴリ別購入数")
        
        # 購入数の集計
        category_count = purchased_products["カテゴリ"].value_counts().reset_index()
        category_count.columns = ["カテゴリ", "購入数"]

        # 全カテゴリを表示するために全カテゴリリストを統合
        all_categories = product_data["カテゴリ"].unique()
        category_count = pd.DataFrame({"カテゴリ": all_categories}).merge(
            category_count, on="カテゴリ", how="left"
        ).fillna(0)

        category_chart = alt.Chart(category_count).mark_bar().encode(
            x=alt.X("カテゴリ", axis=alt.Axis(labelAngle=90, labelFontSize=10)),
            y=alt.Y("購入数"),
            tooltip=["カテゴリ", "購入数"]
        )
        st.altair_chart(category_chart, use_container_width=True)

        # 説明テキスト
        st.write("""このグラフは、各カテゴリごとの購入数を示しています。カテゴリごとに購入数がどのように分布しているかを視覚化しており、どのカテゴリがよく購入されているかを把握することができます。
        購入数の多いカテゴリは、需要の高い商品群やトレンドを示唆している可能性があります。
        """)

    # 購入金額の分布
    elif selected_analysis == "購入金額の分布":
        st.subheader("購入金額の分布")
        price_distribution = purchased_products["価格"]
        st.write(f"平均購入金額: {price_distribution.mean():.2f}円")
        st.write(f"最大購入金額: {price_distribution.max()}円")
        st.write(f"最小購入金額: {price_distribution.min()}円")

        price_chart = alt.Chart(purchased_products).mark_bar().encode(
            alt.X("価格", bin=True, axis=alt.Axis(labelFontSize=10)),
            alt.Y("count()", title="購入数"),
            tooltip=["count()", "sum(価格)"]
        )
        st.altair_chart(price_chart, use_container_width=True)

        # 説明テキスト
        st.write("""このグラフは購入金額の分布を示しています。購入金額がどの範囲で分布しているかを把握することができます。
        平均購入金額や最大・最小金額をもとに、顧客の購買傾向を分析できます。
        """)

    # 購入サイクル分析
    elif selected_analysis == "購入サイクル分析":
        st.subheader("購入サイクル分析")

        user_data["購入日時"] = pd.to_datetime(user_data["購入日時"], errors='coerce')
        user_data = user_data.sort_values(by=["ユーザーID", "購入日時"])
        user_data["購入間隔"] = user_data.groupby("ユーザーID")["購入日時"].diff().dt.days

        user_data = user_data.dropna(subset=["購入間隔"])
        avg_purchase_interval = user_data["購入間隔"].mean()
        median_purchase_interval = user_data["購入間隔"].median()

        st.write(f"平均購入間隔: {avg_purchase_interval:.2f}日")
        st.write(f"中央値購入間隔: {median_purchase_interval}日")

        interval_chart = alt.Chart(user_data).mark_bar().encode(
            alt.X("購入間隔", bin=alt.Bin(maxbins=30), title="購入間隔（日）", axis=alt.Axis(labelFontSize=10)),
            alt.Y("count()", title="購入間隔の頻度"),
            tooltip=["count()", "mean(購入間隔)"]
        )
        st.altair_chart(interval_chart, use_container_width=True)

        # 説明テキスト
        st.write("""このグラフは顧客の購入サイクル（購入間隔）を分析した結果です。顧客がどれくらいの間隔で商品を購入するかを視覚化しており、購買頻度を把握することができます。
        平均購入間隔や中央値購入間隔は、顧客の購買行動を理解するために役立ちます。
        """)

    # 月別購入数分析
    elif selected_analysis == "月別購入数分析":
        st.subheader("月別購入数分析")
        user_data["購入月"] = pd.to_datetime(user_data["購入日時"], errors='coerce').dt.month
        monthly_trends = user_data.groupby("購入月").size().reset_index(name="購入数")

        trend_chart = alt.Chart(monthly_trends).mark_line(point=True).encode(
            x=alt.X("購入月:O", axis=alt.Axis(labelFontSize=10)),
            y=alt.Y("購入数"),
            tooltip=["購入月", "購入数"]
        )
        st.altair_chart(trend_chart, use_container_width=True)

        # 説明テキスト
        st.write("""このグラフは月別の購入数を示しています。各月における購入数の変動を把握することができ、シーズンごとのトレンドや需要の変化を確認できます。
        売れ行きの強い月や低い月の傾向をもとに販売戦略を立てることができます。
        """)

    # 購入回数が多い商品
    elif selected_analysis == "購入回数が多い商品":
        st.subheader("購入回数が多い商品")
        popular_products = product_data.merge(
            user_data.groupby('商品ID').size().reset_index(name='購入回数'),
            on='商品ID'
        )
        popular_products = popular_products.sort_values(by='購入回数', ascending=False)
        st.dataframe(popular_products[["商品名", "購入回数", "価格"]].reset_index(drop=True).head(10))

        # 説明テキスト
        st.write("""この表は購入回数が多い商品をリストアップしています。購入回数の多い商品は、人気のある商品やよく購入される商品群を示しています。
        これらの商品をターゲットにしたマーケティング戦略やプロモーションを行うことで、売上向上に繋がる可能性があります。
        """)

    # 関連度の高い商品
    elif selected_analysis == "関連度の高い商品":
        st.subheader("関連度の高い商品")
        product_name = st.selectbox("商品を選択", product_data["商品名"].unique())

        related_products = similarity_data[similarity_data["商品名1"] == product_name].sort_values(
            by="関連度", ascending=False
        )
        st.dataframe(related_products[["商品名2", "関連度"]].rename(columns={"商品名2": "商品名"}).reset_index(drop=True).head(10))

        # 説明テキスト
        st.write("""この表は選択した商品に関連性の高い商品を示しています。関連度の高い商品は、顧客が一緒に購入する可能性が高い商品群を示しています。
        クロスセルやアップセルの戦略を考える際に有効な情報となります。
        """)
        
    # 商品購入トレンド予測
    elif selected_analysis == "商品購入トレンド予測":
        st.subheader("商品購入トレンド予測")

        # 月別購入数を使った時系列予測
        user_data["購入月"] = pd.to_datetime(user_data["購入日時"]).dt.to_period("M")
        monthly_data = user_data.groupby("購入月").size().reset_index(name="購入数")

        # Period型をTimestamp型に変換
        last_period = monthly_data["購入月"].max().to_timestamp()

        # ARIMAモデルの適用
        model = ARIMA(monthly_data["購入数"], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=3)

        # 予測結果の整形
        forecast_data = pd.DataFrame({
            "購入月": pd.date_range(start=last_period, periods=4, freq="M")[1:].strftime('%Y-%m'),  # 月のみ表示
            "購入数": forecast.astype(int),  # 整数に変換
            "データタイプ": "予測"
        })

        # 過去データの整形
        past_data = monthly_data.copy()
        past_data["購入月"] = past_data["購入月"].dt.strftime('%Y-%m')  # 月のフォーマットを合わせる
        past_data["データタイプ"] = "実績"

        # 実績データと予測データを結合
        combined_data = pd.concat([past_data, forecast_data], ignore_index=True)

        # 実績データと予測データを描画
        actual_chart = alt.Chart(combined_data[combined_data["データタイプ"] == "実績"]).mark_line().encode(
            x=alt.X("購入月:T", title="購入月", axis=alt.Axis(format="%Y-%m", labelAngle=90)),  # 月のみ表示
            y=alt.Y("購入数:Q", title="購入数"),
            color=alt.value("blue"),  # 実績データの色
            tooltip=["購入月", "購入数"]
        )

        predicted_chart = alt.Chart(combined_data[combined_data["データタイプ"] == "予測"]).mark_line(strokeDash=[5, 5]).encode(
            x=alt.X("購入月:T", title="購入月", axis=alt.Axis(format="%Y-%m", labelAngle=90)),  # 月のみ表示
            y=alt.Y("購入数:Q", title="購入数"),
            color=alt.value("orange"),  # 予測データの色
            tooltip=["購入月", "購入数"]
        )

        # 実績と予測のチャートを結合
        final_chart = actual_chart + predicted_chart

        # 実績データの最後のポイントと予測データの最初のポイントをつなぐための追加のポイントを作成
        if not forecast_data.empty:
            last_actual = past_data.iloc[-1]
            next_forecast = forecast_data.iloc[0]
            
            connecting_data = pd.DataFrame({
                "購入月": [last_actual["購入月"], next_forecast["購入月"]],
                "購入数": [last_actual["購入数"], next_forecast["購入数"]],
                "データタイプ": ["実績", "予測"]
            })

            connecting_chart = alt.Chart(connecting_data).mark_line(strokeDash=[5, 5], color="orange").encode(
                x=alt.X("購入月:T"),
                y=alt.Y("購入数:Q")
            )

            final_chart += connecting_chart

        st.altair_chart(final_chart, use_container_width=True)
