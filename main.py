import streamlit as st
import streamlit_constants as st_const

def apply_page_style():
    """ページスタイルとロゴを設定"""
    st.set_page_config(
        page_title="Craft College デモアプリ（無料相談会用）",
        page_icon="./data/assets/craft-college_favicon.ico",
        layout="wide"
    )
    st.logo(
        "./data/assets/craft-college_logo.png",
        size="large"
    )
    st.markdown(st_const.HIDE_ST_STYLE, unsafe_allow_html=True)


def main():
    """メイン関数"""
    apply_page_style()
    
    # ページ定義
    top_page = st.Page(
        page="pages/0_top.py", 
        title="TOP", 
        icon="🏠",
        default=True
    )
    analytics_page = st.Page(
        page="pages/1_analytics.py", 
        title="データ分析", 
        icon="📊"
    )
    demand_forecast_page = st.Page(
        page="pages/2_demand_forecast.py", 
        title="需要予測", 
        icon="📈"
    )
    recommendation_page = st.Page(
        page="pages/3_recommendation.py", 
        title="レコメンド", 
        icon="📚"
    )
    ai_chatbot_page = st.Page(
        page="pages/4_ai_chatbot.py", 
        title="AIチャットボット", 
        icon="🤖"
    )
    
    # ナビゲーション設定
    pg = st.navigation({
        "メニュー": [
            top_page,
            analytics_page,
            demand_forecast_page,
            recommendation_page,
            ai_chatbot_page
        ]
    })
    
    # ページ実行
    pg.run()


if __name__ == "__main__":
    main() 
