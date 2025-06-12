import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings('ignore')


@st.cache_data
def load_books_data():
    """書籍データを読み込み"""
    try:
        data_path = "data/input/books_recommendation.csv"
        # Shift-JISエンコーディングで読み込み
        df = pd.read_csv(data_path, encoding='shift-jis')
        return df, None
    except Exception as e:
        st.error(f"データ読み込みエラー: {str(e)}")
        return None, str(e)


@st.cache_data
def prepare_tfidf_matrix(df):
    """TF-IDF行列を事前計算してキャッシュ"""
    try:
        # コンテンツ特徴量を作成（著者とタイトルを結合）
        df_unique = df[['book_id', 'author', 'title', 'average_rating', 'ratings_count', 'image_url']].drop_duplicates()
        content_features = df_unique['author'].fillna('') + ' ' + df_unique['title'].fillna('')
        
        # TF-IDF ベクトル化
        vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_features=1000,
            ngram_range=(1, 2),  # 1-gramと2-gramを使用
            min_df=1  # 最小出現回数
        )
        tfidf_matrix = vectorizer.fit_transform(content_features)
        
        return df_unique, tfidf_matrix, vectorizer, None
    except Exception as e:
        return None, None, None, f"TF-IDF行列作成エラー: {str(e)}"


def display_data_overview(df_unique):
    """データ概要を表示"""
    st.subheader("📊 データについて")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("総書籍数", f"{len(df_unique):,}")
    
    with col2:
        if 'average_rating' in df_unique.columns and df_unique['average_rating'].notna().any():
            st.metric("平均評価", f"{df_unique['average_rating'].mean():.1f}")
        else:
            st.metric("平均評価", "N/A")


def create_book_selection_ui(df_unique):
    """書籍選択UIを作成し、選択された書籍IDを返す"""
    st.subheader("📚 レコメンド設定")
    
    # 書籍選択（人気順でソート）
    df_sorted = df_unique.copy()
    if 'ratings_count' in df_sorted.columns and df_sorted['ratings_count'].notna().any():
        df_sorted = df_sorted.sort_values('ratings_count', ascending=False)
    
    book_options = {}
    for _, row in df_sorted.iterrows():
        title = row['title'] if pd.notna(row['title']) else '不明なタイトル'
        author = row['author'] if pd.notna(row['author']) else '不明な著者'
        display_name = f"{title} - {author}"
        book_options[display_name] = row['book_id']
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_book_title = st.selectbox(
            "好きな書籍を選択してください:",
            options=["選択してください"] + list(book_options.keys()),
            help="人気順で表示されています"
        )
    
    with col2:
        n_recommendations = st.slider("レコメンド数:", 5, 20, 10)
    
    selected_book_id = book_options.get(selected_book_title, None) if selected_book_title != "選択してください" else None
    
    return selected_book_id, n_recommendations


def get_content_based_recommendations(df_unique, tfidf_matrix, selected_books, n_recommendations=10):
    """コンテンツベースレコメンデーション（高速化版）"""
    try:
        if len(selected_books) == 0:
            return pd.DataFrame()
        
        # 選択された本のインデックスを取得
        selected_indices = []
        for book_id in selected_books:
            book_idx = df_unique[df_unique['book_id'] == book_id].index
            if len(book_idx) > 0:
                # DataFrame のインデックスを配列のインデックスに変換
                array_idx = df_unique.index.get_loc(book_idx[0])
                selected_indices.append(array_idx)
        
        if len(selected_indices) == 0:
            return pd.DataFrame()
        
        # 選択された本を除外した候補本
        all_indices = set(range(len(df_unique)))
        candidate_indices = list(all_indices - set(selected_indices))
        
        if len(candidate_indices) == 0:
            return pd.DataFrame()
        
        # 選択された本の平均ベクトルを計算
        selected_vectors = tfidf_matrix[selected_indices]
        if len(selected_indices) > 1:
            avg_selected_vector = selected_vectors.mean(axis=0)
        else:
            avg_selected_vector = selected_vectors[0]
        
        # 候補本との類似度を計算
        candidate_vectors = tfidf_matrix[candidate_indices]
        similarities = cosine_similarity(avg_selected_vector, candidate_vectors).flatten()
        
        # 結果をデータフレームに整理
        candidate_books = df_unique.iloc[candidate_indices].copy()
        candidate_books['similarity'] = similarities
        
        # 類似度でソート
        recommendations = candidate_books.sort_values('similarity', ascending=False).head(n_recommendations)
        
        return recommendations
    except Exception as e:
        st.error(f"コンテンツベースレコメンデーションエラー: {str(e)}")
        return pd.DataFrame()


def display_book_cards(recommendations, recommendation_type):
    """書籍カードを表示（Netflix風横スクロール）"""
    if len(recommendations) == 0:
        st.info("レコメンデーション結果がありません。")
        return
    
    st.subheader(f"📚 {recommendation_type}レコメンデーション結果")
    
    # Netflix風の横スクロール可能なカードレイアウト
    st.markdown("""
    <style>
    .book-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 20px 0;
        scrollbar-width: thin;
    }
    .book-container::-webkit-scrollbar {
        height: 8px;
    }
    .book-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    .book-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    .book-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    .book-card {
        min-width: 200px;
        max-width: 200px;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
        flex-shrink: 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .book-image {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .book-title {
        font-size: 14px;
        font-weight: bold;
        margin: 10px 0 5px 0;
        height: 40px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .book-info {
        font-size: 12px;
        color: #666;
        margin: 5px 0;
    }
    .book-rating {
        font-size: 12px;
        color: #1f77b4;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # カードHTML生成
    cards_html = '<div class="book-container">'
    
    for _, book in recommendations.iterrows():
        cards_html += f'''
        <div class="book-card">
            <img src="{book['image_url']}" class="book-image" alt="{book['title']}">
            <div class="book-title">{book['title']}</div>
            <div class="book-info"><strong>著者:</strong> {book['author']}</div>
        '''
        
        # 平均評価がある場合のみ表示
        if 'average_rating' in book and pd.notna(book['average_rating']):
            cards_html += f'<div class="book-info"><strong>平均評価:</strong> {book["average_rating"]:.1f}⭐</div>'
        
        # 類似度を表示
        if 'similarity' in book:
            cards_html += f'<div class="book-rating"><strong>類似度:</strong> {book["similarity"]:.3f}</div>'
        
        cards_html += '</div>'
    
    cards_html += '</div>'
    
    # HTML表示
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # スクロールヒント
    st.markdown(
        '<p style="font-size: 12px; color: #888; text-align: center; margin-top: 10px;">← 横にスクロールして他のおすすめ書籍を見る →</p>',
        unsafe_allow_html=True
    )


def execute_recommendation(df_unique, tfidf_matrix, selected_book_id, n_recommendations):
    """レコメンデーションを実行して結果を表示"""
    if not selected_book_id:
        st.info("好きな書籍を選択してください。")
        return
    
    if st.button("🚀 レコメンド実行", type="primary"):
        with st.spinner("レコメンデーションを生成中..."):
            # コンテンツベースレコメンデーション
            recommendations = get_content_based_recommendations(
                df_unique, tfidf_matrix, [selected_book_id], n_recommendations
            )
            
            if len(recommendations) > 0:
                display_book_cards(recommendations, "コンテンツベース")
            else:
                st.warning("コンテンツベースレコメンデーションの結果がありません。")


def display_selected_book_card(book_info):
    """選択された書籍を横長カードで表示"""
    st.markdown(f"""
    <div style="
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f0f8ff;
        display: flex;
        align-items: center;
        gap: 20px;
    ">
        <img src="{book_info['image_url']}" style="
            width: 120px; 
            height: 160px; 
            object-fit: cover; 
            border-radius: 5px;
            flex-shrink: 0;
        ">
        <div style="flex: 1;">
            <h3 style="margin: 0 0 10px 0; color: #1f77b4; font-size: 24px;">{book_info['title']}</h3>
            <p style="margin: 5px 0; color: #666; font-size: 18px;"><strong>著者:</strong> {book_info['author']}</p>
            <div style="display: flex; gap: 30px; margin-top: 15px;">
    """, unsafe_allow_html=True)
    
    # 平均評価がある場合のみ表示
    if 'average_rating' in book_info and pd.notna(book_info['average_rating']):
        st.markdown(f'<p style="margin: 0; color: #666; font-size: 16px;"><strong>平均評価:</strong> {book_info["average_rating"]:.1f}⭐</p>', unsafe_allow_html=True)
    
    # 評価数がある場合のみ表示
    if 'ratings_count' in book_info and pd.notna(book_info['ratings_count']):
        st.markdown(f'<p style="margin: 0; color: #666; font-size: 16px;"><strong>評価数:</strong> {book_info["ratings_count"]:,}</p>', unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """メイン関数"""
    # ページヘッダー
    st.markdown('<h1 class="main-header">📚 書籍レコメンド</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">あなたの好みに基づいて新しい書籍をおすすめします</p>', unsafe_allow_html=True)
    
    # データ読み込み
    df, warning_message = load_books_data()
    if warning_message:
        st.warning(warning_message)
    
    # TF-IDF行列を事前計算
    with st.spinner("TF-IDF行列を準備中..."):
        df_unique, tfidf_matrix, _, error_message = prepare_tfidf_matrix(df)
    
    if error_message:
        st.error(error_message)
        return
    
    # データ概要表示
    display_data_overview(df_unique)
    
    # 書籍選択UI
    selected_book_id, n_recommendations = create_book_selection_ui(df_unique)
    
    # 選択された書籍の表示
    if selected_book_id:
        st.subheader("📖 選択された書籍")
        selected_book_info = df_unique[df_unique['book_id'] == selected_book_id].iloc[0]
        display_selected_book_card(selected_book_info)
    
    # レコメンド実行
    execute_recommendation(df_unique, tfidf_matrix, selected_book_id, n_recommendations)

if __name__ == "__main__":
    main()