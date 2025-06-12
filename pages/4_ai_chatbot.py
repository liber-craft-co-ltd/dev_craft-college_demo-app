import streamlit as st
from datetime import datetime
import json
import os
from openai import OpenAI

# 環境変数ファイルの読み込み（ローカル開発用）
try:
    from dotenv import load_dotenv
    load_dotenv()  # .envファイルから環境変数を読み込み
except ImportError:
    pass  # python-dotenvがない場合はスキップ


def get_openai_api_key():
    """OpenAI API キーを取得（Streamlit Cloud と ローカル開発に対応）"""
    # 1. Streamlit Secrets から取得を試行
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if api_key:
            return api_key, "Streamlit Secrets"
    except (KeyError, FileNotFoundError):
        pass
    
    # 2. 環境変数から取得を試行
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key, "環境変数"
    
    # 3. どちらからも取得できない場合
    return None, None


def initialize_openai_client():
    """OpenAI クライアントを初期化"""
    api_key, source = get_openai_api_key()
    if not api_key:
        return None, "OPENAI_API_KEY が設定されていません。"
    
    try:
        client = OpenAI(api_key=api_key)
        return client, f"OpenAI API に接続しました（取得元: {source}）"
    except Exception as e:
        return None, f"OpenAI クライアント初期化エラー: {str(e)}"


def get_system_prompt():
    """システムプロンプトを取得"""
    return """あなたはオンラインスクール「Craft College」の学習アドバイザーです。
AI・データサイエンス、機械学習、プログラミングに関する質問に対して、
初心者にも分かりやすく、実践的なアドバイスを提供してください。

以下の点を心がけてください：
1. 専門用語は分かりやすく説明する
2. 具体例を交えて説明する
3. 学習のステップを明確に示す
4. 実際のプロジェクトや業務での活用方法を提案する
5. 日本語で回答する

Craft College は実践的なデータサイエンス教育を提供するスクールです。
受講生の学習をサポートし、キャリア形成を支援することが目標です。"""


def get_chat_response(client, messages):
    """ChatGPT からの応答を取得"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.1,
            stream=False
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"ChatGPT API エラー: {str(e)}"


def initialize_session_state():
    """セッション状態を初期化"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """
                こんにちは！Craft College の学習アドバイザーです。
                データサイエンス、機械学習、プログラミングに関するご質問がございましたら、お気軽にお聞かせください。初心者の方から上級者の方まで、レベルに応じてサポートいたします。
                何かご質問はありますか？
                """
            }
        ]
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def get_sample_questions():
    """サンプル質問を取得"""
    return [
        "データサイエンスを学び始めるには何から始めればよいですか？",
        "PythonとRのどちらを学ぶべきでしょうか？",
        "機械学習の基本的なアルゴリズムを教えてください",
        "データ分析のプロジェクトの進め方を教えてください",
        "統計学の知識はどの程度必要ですか？",
        "データサイエンティストになるためのスキルセットは？",
        "実際の業務でよく使われるツールを教えてください",
        "データの前処理で重要なポイントは何ですか？",
        "機械学習モデルの評価方法について教えてください",
        "データ可視化のベストプラクティスは？"
    ]


def display_chat_message(role, content, timestamp=None):
    """チャットメッセージを表示"""
    with st.chat_message(role):
        st.write(content)
        if timestamp:
            st.caption(f"送信時刻: {timestamp}")


def save_chat_history(user_message, assistant_response):
    """チャット履歴を保存"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chat_entry = {
        "timestamp": timestamp,
        "user_message": user_message,
        "assistant_response": assistant_response
    }
    
    st.session_state.chat_history.append(chat_entry)


def get_usage_guide_content():
    """使用方法ガイドのコンテンツを取得"""
    return """
    ### AIチャットボットの使い方
    
    1. **質問入力**: 下部の入力欄にご質問を入力してください
    2. **サンプル質問**: 質問例から選択できます
    3. **履歴管理**: サイドバーからチャット履歴のクリアが可能です
    
    ### 質問のコツ
    
    - **具体的に**: 「Pythonの基礎を学びたい」より「Python初心者がデータ分析を始めるための学習順序を教えて」
    - **背景を含める**: 現在のスキルレベルや目標を教えてください
    - **実践的に**: 「理論だけでなく、実際のプロジェクトでの活用方法も知りたい」
    
    ### 対応分野
    
    - データサイエンス基礎
    - Python/R プログラミング
    - 機械学習・深層学習
    - データ可視化
    - 統計学
    - キャリア相談
    """


def get_api_setup_instructions():
    """API設定手順のコンテンツを取得"""
    return """
    **OpenAI API キーの設定方法:**
    
    ### Streamlit Cloud の場合:
    1. 「Settings」→「Secrets」に移動
    2. `OPENAI_API_KEY = "your_api_key_here"` を設定
    
    ### ローカル開発の場合:
    1. `.env`ファイルを作成: `OPENAI_API_KEY=your_api_key_here`
    2. または環境変数で設定: `export OPENAI_API_KEY=your_api_key_here`
    
    API キーは [OpenAI Platform](https://platform.openai.com/api-keys) で取得できます。
    """


def get_demo_response(user_input):
    """デモモード用の応答を生成"""
    return f"""申し訳ございませんが、現在デモモードで動作しているため、実際のAI応答を提供できません。

**あなたの質問:** {user_input}

実際の環境では、この質問に対してCraft Collegeの学習アドバイザーとして詳細で実践的なアドバイスを提供いたします。
OpenAI API キーを設定すると、本格的なAIチャットボット機能をご利用いただけます。"""


def render_page_header():
    """ページヘッダーを表示"""
    st.markdown('<h1 class="main-header">🤖 AIチャットボット</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Craft College の学習アドバイザーがあなたの質問にお答えします</p>', unsafe_allow_html=True)


def render_api_status(client, message):
    """API接続状況を表示"""
    if client is None:
        st.error(f"⚠️ {message}")
        st.info(get_api_setup_instructions())
        st.warning("デモモードで動作しています。実際のAI応答は利用できません。")
        return False
    else:
        st.success(f"✅ {message}")
        return True


def render_chat_settings():
    """チャット設定セクションを表示"""
    st.header("🤖 チャット設定")

    # 使用方法の説明
    with st.expander("📖 使用方法"):
        st.markdown(get_usage_guide_content())
    
    # サンプル質問
    st.subheader("💡 質問例")
    sample_questions = get_sample_questions()
    
    selected_question = st.selectbox(
        "質問を選択（任意）:",
        [""] + sample_questions,
        help="質問を選択して送信ボタンを押してください"
    )
    
    return selected_question


def render_sidebar():
    """サイドバーを表示"""
    st.sidebar.header("📋 チャット管理")
    if st.sidebar.button("🗑️ 履歴クリア"):
        st.session_state.messages = [st.session_state.messages[0]]  # 初期メッセージのみ残す
        st.session_state.chat_history = []
        st.rerun()


def render_chat_area():
    """チャットエリアを表示"""
    st.subheader("💬 チャット")
    
    # チャット履歴表示
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])


def handle_question_selection(selected_question):
    """選択された質問の処理"""
    if selected_question:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("📝 この質問を送信", use_container_width=True):
                return selected_question
        with col2:
            if st.button("❌ クリア"):
                st.rerun()
        
        # 通常の入力欄も表示
        return st.chat_input("または、ここに直接入力してください...")
    else:
        return st.chat_input("メッセージを入力してください...")


def process_user_input(user_input, client):
    """ユーザー入力を処理"""
    # ユーザーメッセージを表示・保存
    st.session_state.messages.append({"role": "user", "content": user_input})
    display_chat_message("user", user_input)
    
    # AI応答生成
    with st.spinner("回答を生成中..."):
        if client is not None:
            # OpenAI API を使用
            messages_for_api = [{"role": "system", "content": get_system_prompt()}]
            messages_for_api.extend(st.session_state.messages)
            
            response, error = get_chat_response(client, messages_for_api)
            
            if response:
                # AI応答を表示・保存
                st.session_state.messages.append({"role": "assistant", "content": response})
                display_chat_message("assistant", response)
                
                # チャット履歴に保存
                save_chat_history(user_input, response)
            else:
                st.error(f"応答生成エラー: {error}")
        else:
            # デモモード応答
            demo_response = get_demo_response(user_input)
            
            st.session_state.messages.append({"role": "assistant", "content": demo_response})
            display_chat_message("assistant", demo_response)
            
            # デモ履歴も保存
            save_chat_history(user_input, demo_response)
    
    st.rerun()


def main():
    """メイン関数"""
    # ページヘッダー
    render_page_header()
    
    # セッション状態初期化
    initialize_session_state()
    
    # OpenAI クライアント初期化
    client, message = initialize_openai_client()
    
    # API接続状況表示
    api_available = render_api_status(client, message)
    
    # チャット設定
    selected_question = render_chat_settings()
    
    # サイドバー
    render_sidebar()
    
    # チャットエリア
    render_chat_area()
    
    # ユーザー入力処理
    user_input = handle_question_selection(selected_question)
    
    if user_input:
        process_user_input(user_input, client)


if __name__ == "__main__":
    main() 