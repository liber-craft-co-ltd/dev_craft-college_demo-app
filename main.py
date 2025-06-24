import streamlit as st
import streamlit_constants as st_const
import importlib.util
import sys

def apply_page_style():
    """ページスタイルとロゴを設定"""
    st.set_page_config(
        page_title="Craft College デモアプリ（無料相談会用）",
        page_icon="./data/assets/craft-college_favicon.ico",
        layout="wide"
    )
    # st.logo(
    #     "./data/assets/craft-college_logo.png",
    #     size="large"
    # )
    st.markdown(st_const.HIDE_ST_STYLE, unsafe_allow_html=True)


def load_page_module(page_path, module_name):
    """ページモジュールを動的に読み込み"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, page_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"ページ読み込みエラー ({page_path}): {str(e)}")
        return None


def show_top_page():
    """TOPページの内容を表示"""
    # イントロダクション
    st.markdown("""
    ## 🌟 このデモアプリについて
    
    Craft College では、実践的なAI・データサイエンス教育を提供しています。
    このデモアプリでは、実際に講座の中で学べる内容・技術を体験していただけます。
    
    各タブでは異なるデータサイエンスの手法を学ぶことができます。
    """)
    
    st.markdown("---")
    
    # 各機能の説明
    st.markdown("## 📋 体験できる内容")
    
    # 4つのカードを2x2で配置
    col1, col2 = st.columns(2)
    
    with col1:
        # データ分析カード
        st.markdown("""
        <div style="
            border: 2px solid #1f77b4;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #1f77b4; margin-top: 0;">📊 データ分析</h3>
            <p><strong>学べること:</strong></p>
            <ul>
                <li>データの可視化技術</li>
                <li>統計分析の基礎</li>
                <li>グラフの作成と解釈</li>
                <li>データの傾向把握</li>
            </ul>
            <p><strong>使用技術:</strong> Python, Pandas, Plotly, 統計学</p>
            <p><strong>実務での活用:</strong> 売上分析、顧客分析、KPI監視</p>
        </div>
        """, unsafe_allow_html=True)
        
        # レコメンドカード
        st.markdown("""
        <div style="
            border: 2px solid #ff7f0e;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #fff8f0 0%, #ffe6cc 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #ff7f0e; margin-top: 0;">📚 レコメンド</h3>
            <p><strong>学べること:</strong></p>
            <ul>
                <li>推薦システムの仕組み</li>
                <li>コンテンツベースフィルタリング</li>
                <li>協調フィルタリング</li>
                <li>機械学習による予測</li>
            </ul>
            <p><strong>使用技術:</strong> scikit-learn, TF-IDF, SVD</p>
            <p><strong>実務での活用:</strong> ECサイト、動画配信、音楽配信</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 需要予測カード
        st.markdown("""
        <div style="
            border: 2px solid #2ca02c;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f0fff0 0%, #e6ffe6 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #2ca02c; margin-top: 0;">📈 需要予測</h3>
            <p><strong>学べること:</strong></p>
            <ul>
                <li>時系列データ分析</li>
                <li>予測モデルの構築</li>
                <li>季節性・トレンドの把握</li>
                <li>予測精度の評価</li>
            </ul>
            <p><strong>使用技術:</strong> Prophet, SARIMAX, 時系列分析</p>
            <p><strong>実務での活用:</strong> 在庫管理、売上予測、需要計画</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AIチャットボットカード
        st.markdown("""
        <div style="
            border: 2px solid #d62728;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #fff0f0 0%, #ffe6e6 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #d62728; margin-top: 0;">🤖 AIチャットボット</h3>
            <p><strong>学べること:</strong></p>
            <ul>
                <li>生成AIの活用方法</li>
                <li>プロンプトエンジニアリング</li>
                <li>対話システムの構築</li>
                <li>AI技術の実装</li>
            </ul>
            <p><strong>使用技術:</strong> OpenAI GPT-4, API連携</p>
            <p><strong>実務での活用:</strong> カスタマーサポート、FAQ、相談窓口</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """メイン関数"""
    apply_page_style()

    st.markdown('<h1 class="main-header">🎓 Craft College デモアプリへようこそ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">AI・データサイエンスの世界を体験してみましょう</p>', unsafe_allow_html=True)
    
    # タブの設定
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 TOP", 
        "📊 データ分析", 
        "📈 需要予測", 
        "📚 レコメンド", 
        "🤖 AIチャットボット"
    ])
    
    # 各タブの内容
    with tab1:
        show_top_page()
    
    with tab2:
        # データ分析ページを動的に読み込み
        analytics_module = load_page_module("pages/1_analytics.py", "analytics_page")
        if analytics_module and hasattr(analytics_module, 'main'):
            analytics_module.main()
        else:
            st.error("データ分析ページの読み込みに失敗しました。")
    
    with tab3:
        # 需要予測ページを動的に読み込み
        demand_forecast_module = load_page_module("pages/2_demand_forecast.py", "demand_forecast_page")
        if demand_forecast_module and hasattr(demand_forecast_module, 'main'):
            demand_forecast_module.main()
        else:
            st.error("需要予測ページの読み込みに失敗しました。")
    
    with tab4:
        # レコメンドページを動的に読み込み
        recommendation_module = load_page_module("pages/3_recommendation.py", "recommendation_page")
        if recommendation_module and hasattr(recommendation_module, 'main'):
            recommendation_module.main()
        else:
            st.error("レコメンドページの読み込みに失敗しました。")
    
    with tab5:
        # AIチャットボットページを動的に読み込み
        ai_chatbot_module = load_page_module("pages/4_ai_chatbot.py", "ai_chatbot_page")
        if ai_chatbot_module and hasattr(ai_chatbot_module, 'main'):
            ai_chatbot_module.main()
        else:
            st.error("AIチャットボットページの読み込みに失敗しました。")


if __name__ == "__main__":
    main() 
