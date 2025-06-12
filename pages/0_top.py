import streamlit as st

def main():
    """メイン関数"""
    st.markdown('<h1 class="main-header">🎓 Craft College デモアプリへようこそ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">AI・データサイエンスの世界を体験してみましょう</p>', unsafe_allow_html=True)
    
    # イントロダクション
    st.markdown("""
    ## 🌟 このデモアプリについて
    
    Craft College では、実践的なAI・データサイエンス教育を提供しています。
    このデモアプリでは、実際に講座の中で学べる内容・技術を体験していただけます。
    
    各ページでは異なるデータサイエンスの手法を学ぶことができます。
    """)
    
    st.markdown("---")
    
    # 各ページの説明
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
    
    st.markdown("---")
    
    # 学習の流れ
    st.markdown("## 🚀 おすすめの学習順序")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #1f77b4;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                margin: 0 auto 10px;
            ">1</div>
            <h4>データ分析</h4>
            <p style="font-size: 14px;">まずはデータを理解しよう</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #2ca02c;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                margin: 0 auto 10px;
            ">2</div>
            <h4>需要予測</h4>
            <p style="font-size: 14px;">未来を予測してみよう</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #ff7f0e;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                margin: 0 auto 10px;
            ">3</div>
            <h4>レコメンド</h4>
            <p style="font-size: 14px;">おすすめを作ってみよう</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #d62728;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                margin: 0 auto 10px;
            ">4</div>
            <h4>AIチャット</h4>
            <p style="font-size: 14px;">AIと対話してみよう</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 始め方
    st.markdown("## 🎯 さあ、始めましょう！")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
            margin: 20px 0;
        ">
            <h3 style="margin-top: 0; color: white;">👈 サイドバーからページを選択</h3>
            <p style="font-size: 18px; margin-bottom: 0;">
                左側のメニューから興味のあるページを選んで<br>
                データサイエンスの世界を体験してください！
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 追加情報
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💡 このデモアプリの特徴
        
        - **実データ対応**: 実際のCSVファイルを読み込み可能
        - **サンプルデータ**: データがない場合は自動生成
        - **インタラクティブ**: パラメータを変更して結果を確認
        - **高速処理**: キャッシュ機能で快適な操作
        - **エラー対応**: 丁寧なエラーハンドリング
        """)
    
    with col2:
        st.markdown("""
        ### 🎓 Craft College について
        
        - **実践重視**: 現場で使える技術を習得
        - **個別指導**: 一人ひとりに合わせたサポート
        - **キャリア支援**: 転職・スキルアップを全面バックアップ
        - **最新技術**: 業界トレンドに対応したカリキュラム
        - **コミュニティ**: 同じ目標を持つ仲間との交流
        """)
    
    # フッター
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎓 <strong>Craft College</strong> - 実践的なAI・データサイエンス教育</p>
        <p>質問やご相談がございましたら、お気軽にお声がけください。</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 