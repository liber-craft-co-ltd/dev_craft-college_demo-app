import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import pandas as pd

# 日本語フォント設定
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


@st.cache_data
def load_supermarket_data():
    """スーパーマーケットデータを読み込み"""
    try:
        data_path = "data/input/supermarket_analysis.csv"
        df = pd.read_csv(data_path)
        return df, None
    except Exception as e:
        st.error(f"データ読み込みエラー: {str(e)}")
        return None, str(e)


def create_histogram(df, column):
    """ヒストグラムを作成"""
    fig = px.histogram(
        df, 
        x=column, 
        title=f'{column}のヒストグラム',
        nbins=30,
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        xaxis_title=column,
        yaxis_title='頻度',
        showlegend=False
    )
    return fig


def create_bar_chart(df, column):
    """棒グラフを作成"""
    if df[column].dtype == 'object':
        value_counts = df[column].value_counts()
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=f'{column}の分布',
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='件数',
            showlegend=False
        )
    else:
        # 数値データの場合はビン分割
        bins = pd.cut(df[column], bins=10)
        value_counts = bins.value_counts().sort_index()
        fig = px.bar(
            x=[str(interval) for interval in value_counts.index],
            y=value_counts.values,
            title=f'{column}の分布（ビン分割）',
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='件数',
            showlegend=False,
            xaxis_tickangle=45
        )
    return fig


def create_scatter_plot(df, x_col, y_col):
    """散布図を作成"""
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col,
        title=f'{x_col} vs {y_col}の散布図',
        color_discrete_sequence=['#1f77b4'],
        opacity=0.6
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    return fig


def create_correlation_heatmap(df):
    """相関ヒートマップを作成"""
    # 数値列のみを選択
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        title='相関ヒートマップ',
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig.update_layout(
        width=800,
        height=600
    )
    return fig


def create_rich_histogram(df, column):
    """カーネル密度を含むリッチなヒストグラムを作成"""
    fig = go.Figure()
    
    # ヒストグラム
    fig.add_trace(go.Histogram(
        x=df[column].dropna(),
        nbinsx=30,
        name='度数分布',
        opacity=0.7,
        marker_color='lightblue',
        yaxis='y'
    ))
    
    # カーネル密度推定
    from scipy.stats import gaussian_kde
    data = df[column].dropna()
    if len(data) > 1:
        kde = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 200)
        kde_values = kde(x_range)
        
        # 密度をヒストグラムのスケールに合わせる
        hist_max = len(data) / 30  # 大体のヒストグラムの最大値
        kde_scaled = kde_values * hist_max * 0.8 / kde_values.max()
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=kde_scaled,
            mode='lines',
            name='カーネル密度推定',
            line=dict(color='red', width=3),
            yaxis='y'
        ))
    
    fig.update_layout(
        title=f'{column}の分布（ヒストグラム + カーネル密度推定）',
        xaxis_title=column,
        yaxis_title='度数',
        height=500,
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def create_scatter_with_regression(df, x_col, y_col):
    """回帰直線付きの散布図を作成"""
    # 欠損値を除去
    clean_df = df[[x_col, y_col]].dropna()
    
    if len(clean_df) < 2:
        return None
    
    fig = px.scatter(
        clean_df,
        x=x_col,
        y=y_col,
        title=f'{x_col} vs {y_col}の関係（回帰直線付き）',
        opacity=0.6,
        color_discrete_sequence=['#1f77b4']
    )
    
    # 回帰直線を追加
    from sklearn.linear_model import LinearRegression
    X = clean_df[x_col].values.reshape(-1, 1)
    y = clean_df[y_col].values
    
    reg = LinearRegression().fit(X, y)
    x_range = np.linspace(clean_df[x_col].min(), clean_df[x_col].max(), 100)
    y_pred = reg.predict(x_range.reshape(-1, 1))
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_pred,
        mode='lines',
        name=f'回帰直線 (R²={reg.score(X, y):.3f})',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        showlegend=True
    )
    
    return fig


def create_beautiful_correlation_heatmap(df):
    """美しい相関ヒートマップを作成（seaborn使用）"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    
    # 欠損値を除去してから相関行列を計算
    clean_df = df[numeric_cols].dropna()
    if len(clean_df) < 2:
        return None
    
    corr_matrix = clean_df.corr()
    
    # 適度なサイズに固定（Streamlitに最適化）
    fig_width = 8  # 幅を8インチに固定
    fig_height = 6  # 高さを6インチに固定
    
    # matplotlib figureを作成
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # seabornでヒートマップを作成
    sns.heatmap(
        corr_matrix,
        annot=True,  # 相関係数を表示
        fmt='.3f',   # 小数点以下3桁
        cmap='Blues',  # 青色グラデーション
        center=0,
        square=True,
        ax=ax,
        cbar_kws={'label': '相関係数'},
        annot_kws={'size': 10, 'weight': 'bold'},  # フォントサイズを小さく
        linewidths=0.5,
        linecolor='white',
        vmin=-1,
        vmax=1
    )
    
    # ラベルの回転とサイズ調整
    plt.xticks(rotation=0, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    
    # レイアウト調整
    plt.tight_layout()
    
    return fig


def display_fixed_analysis(df):
    """固定的な分析結果を表示"""
    st.subheader("📈 データ分析")
    
    # 1. 合計金額のヒストグラム（カーネル密度付き）
    total_columns = [col for col in df.columns if 'total' in col.lower() or '合計' in col]
    if total_columns:
        st.markdown("### 1. 💰 合計金額の分布")
        total_col = total_columns[0]
        fig = create_rich_histogram(df, total_col)
        st.plotly_chart(fig, use_container_width=True)
        
        # 統計サマリー
        col_data = df[total_col].dropna()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("平均", f"{col_data.mean():.2f}")
        with col2:
            st.metric("中央値", f"{col_data.median():.2f}")
        with col3:
            st.metric("最大", f"{col_data.max():.2f}")
        with col4:
            st.metric("最小", f"{col_data.min():.2f}")
        
        st.markdown("---")
    
    # 2. 性別の棒グラフ
    gender_columns = [col for col in df.columns if 'gender' in col.lower() or '性別' in col]
    if gender_columns:
        st.markdown("### 2. 👥 性別分布")
        gender_col = gender_columns[0]
        fig = create_bar_chart(df, gender_col)
        st.plotly_chart(fig, use_container_width=True)
        
        # カテゴリ分布
        value_counts = df[gender_col].value_counts()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("カテゴリ数", len(value_counts))
        with col2:
            st.metric("最多カテゴリ", f"{value_counts.index[0]} ({value_counts.iloc[0]}件)")
        
        st.markdown("---")
    
    # 3. 散布図（単価 vs 合計金額、回帰直線付き）
    price_columns = [col for col in df.columns if 'price' in col.lower() or '単価' in col or '価格' in col]
    if total_columns and price_columns:
        st.markdown("### 3. 💹 単価と合計金額の関係")
        price_col = price_columns[0]
        total_col = total_columns[0]
        
        fig = create_scatter_with_regression(df, price_col, total_col)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # 相関係数
            corr = df[price_col].corr(df[total_col])
            st.metric("相関係数", f"{corr:.3f}")
        else:
            st.warning("散布図を作成できませんでした。")
        
        st.markdown("---")
    
    # 4. 相関ヒートマップ
    st.markdown("### 4. 📊 相関ヒートマップ")
    fig = create_beautiful_correlation_heatmap(df)
    if fig:
        # サイズを制御するためにカラムレイアウトを使用
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.pyplot(fig, clear_figure=True)
        plt.close(fig)  # メモリリークを防ぐ
    else:
        st.info("相関ヒートマップを作成するには2つ以上の数値列が必要です。")


def main():
    """メイン関数"""
    st.markdown('<h1 class="main-header">📊 データ分析</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">スーパーマーケットの売上データを分析してみましょう</p>', unsafe_allow_html=True)
    
    # データ読み込み
    df, warning_message = load_supermarket_data()
    
    if df is None:
        st.error("データを読み込めませんでした。")
        return
    
    if warning_message:
        st.warning(warning_message)
    
    # データ型情報を取得
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    # データ概要
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("データ件数", f"{len(df):,}件")
    with col2:
        st.metric("列数", f"{len(df.columns)}列")
    with col3:
        st.metric("数値列", f"{len(numeric_columns)}列")
    with col4:
        st.metric("カテゴリ列", f"{len(categorical_columns)}列")
    
    # データプレビュー
    st.subheader("🔍 データプレビュー")
    st.dataframe(df.head(10), use_container_width=True)
    
    # 基本統計量
    st.subheader("📊 基本統計量")
    if numeric_columns:
        stats_df = df[numeric_columns].describe().T
        # 列名を日本語に変更
        stats_df.columns = ['件数', '平均値', '標準偏差', '最小値', '25%点', '中央値', '75%点', '最大値']
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.info("数値列が存在しません。")
    
    # 固定的な分析を実行
    display_fixed_analysis(df)


if __name__ == "__main__":
    main() 