import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')


@st.cache_data
def load_demand_data():
    """需要予測データを読み込み"""
    try:
        data_path = "data/input/store_item_demand_forecast.csv"
        # Shift-JISエンコーディングで読み込み
        df = pd.read_csv(data_path, encoding='shift-jis')
        # 日付列の処理
        if '日付' in df.columns:
            df['日付'] = pd.to_datetime(df['日付'])
        
        # 商品名を日本語名に変更
        product_mapping = {
            '1': 'りんご',
            '2': 'みかん', 
            '3': 'バナナ',
            '4': 'ぶどう',
            '5': 'いちご'
        }
        
        # 商品列が数字の場合は日本語名に変換
        if '商品' in df.columns:
            df['商品'] = df['商品'].astype(str).map(product_mapping).fillna(df['商品'])
        
        return df, None
    except Exception as e:
        st.error(f"データ読み込みエラー: {str(e)}")
        return None, str(e)


@st.cache_resource
def train_sarimax_model(df_train, store, item):
    """SARIMAX モデルを学習"""
    try:
        # SARIMAX モデル作成・学習
        model = SARIMAX(df_train['販売個数'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
        fitted_model = model.fit(disp=False)
        
        return fitted_model, None
    except Exception as e:
        return None, f"SARIMAX モデル学習エラー: {str(e)}"


def create_forecast_plot(df_train, df_test, forecast_df, store, item):
    """予測結果のプロットを作成"""
    fig = go.Figure()
    
    # 訓練データ（実測と同じ色系）
    fig.add_trace(go.Scatter(
        x=df_train['日付'],
        y=df_train['販売個数'],
        mode='lines',
        name='訓練データ',
        line=dict(color='#636EFA', width=2)  # plotlyのデフォルト青色
    ))
    
    # 予測データ（実測と同色系の破線）
    if forecast_df is not None:
        fig.add_trace(go.Scatter(
            x=forecast_df['日付'],
            y=forecast_df['予測値'],
            mode='lines',
            name='予測値',
            line=dict(color='#636EFA', dash='5px,2px', width=2)
        ))
    
    # テストデータ（実績）- デフォルト非表示
    fig.add_trace(go.Scatter(
        x=df_test['日付'],
        y=df_test['販売個数'],
        mode='lines',
        name='実績',
        line=dict(color='#EF553B', width=2),  # plotlyのデフォルト赤色
        visible='legendonly'  # 凡例クリックで表示可能だが、デフォルトは非表示
    ))
    
    fig.update_layout(
        title=f'{item} の需要予測',
        xaxis_title='日付',
        yaxis_title='販売個数',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def calculate_metrics(y_true, y_pred):
    """予測精度の指標を計算"""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape
    }


def display_data_overview(df_filtered):
    """データ概要を表示"""
    st.subheader("📊 データ概要")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("データ期間", f"{len(df_filtered)}日")
    with col2:
        st.metric("平均売上", f"{df_filtered['販売個数'].mean():.1f}")
    with col3:
        st.metric("最大売上", f"{df_filtered['販売個数'].max()}")
    with col4:
        st.metric("最小売上", f"{df_filtered['販売個数'].min()}")


def display_sales_trend(df_item, selected_item):
    """売上推移グラフを表示"""
    st.subheader("📈 売上推移")
    
    # 時系列プロット
    fig_overview = px.line(
        df_item, 
        x='日付', 
        y='販売個数',
        title=f'{selected_item} の売上推移'
    )
    fig_overview.update_layout(
        xaxis_title='日付',
        yaxis_title='販売個数',
        height=400
    )
    st.plotly_chart(fig_overview, use_container_width=True)


def display_statistics(df_item):
    """統計情報を表示"""
    # 基本統計量
    st.subheader("📈 基本統計量")
    st.dataframe(df_item[['販売個数']].describe().T, use_container_width=True)
    
    # データ期間
    st.subheader("📅 データ期間")
    period_df = pd.DataFrame({
        '開始日': [df_item['日付'].min().strftime('%Y-%m-%d')],
        '終了日': [df_item['日付'].max().strftime('%Y-%m-%d')],
        'データ数': [f"{len(df_item)}日"]
    })
    st.dataframe(period_df, use_container_width=True, hide_index=True)


def get_forecast_settings(df_item):
    """予測設定を取得"""
    st.subheader("⚙️ 予測設定")
    
    # データ期間の取得
    min_date = df_item['日付'].min()
    max_date = df_item['日付'].max()
    
    # デフォルトの分割点（全期間の80%地点）
    total_days = (max_date - min_date).days
    default_split_days = int(total_days * 0.8)
    default_split_date = min_date + pd.Timedelta(days=default_split_days)
    
    # 分割点の設定
    split_date = st.date_input(
        "学習・予測期間の分割点",
        value=default_split_date,
        min_value=min_date + pd.Timedelta(days=30),
        max_value=max_date - pd.Timedelta(days=7),
        help="この日付以前が学習期間、以降が予測期間になります"
    )
    
    # 分割点をdatetimeに変換
    split_datetime = pd.to_datetime(split_date)
    
    # 期間の表示
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**学習期間:** {min_date.strftime('%Y-%m-%d')} 〜 {split_datetime.strftime('%Y-%m-%d')}")
    with col2:
        st.info(f"**予測期間:** {(split_datetime + pd.Timedelta(days=1)).strftime('%Y-%m-%d')} 〜 {max_date.strftime('%Y-%m-%d')}")
    
    return split_datetime


def execute_forecast(df_item, split_datetime, selected_item):
    """予測を実行し、結果を表示"""
    with st.spinner("予測モデルを学習中..."):
        # データ分割
        df_train = df_item[df_item['日付'] <= split_datetime].copy()
        df_test = df_item[df_item['日付'] > split_datetime].copy()
        
        if len(df_train) < 20 or len(df_test) < 5:
            st.error("学習または予測期間のデータが不足しています。")
            return
        
        try:
            # SARIMAX モデル
            model, error = train_sarimax_model(df_train, df_item['店舗'].iloc[0] if '店舗' in df_item.columns else '店舗1', selected_item)
            
            if model is not None:
                # 予測実行
                forecast_result = model.forecast(steps=len(df_test))
                
                forecast_df = pd.DataFrame({
                    '日付': df_test['日付'].values,
                    '予測値': forecast_result.values
                })
                
                # 精度計算
                metrics = calculate_metrics(df_test['販売個数'].values, forecast_result.values)
                
                # 結果表示
                display_forecast_results(df_train, df_test, forecast_df, metrics, selected_item, df_item)
            else:
                st.error(error)
                
        except Exception as e:
            st.error(f"予測実行エラー: {str(e)}")


def display_forecast_results(df_train, df_test, forecast_df, metrics, selected_item, df_item):
    """予測結果を表示"""
    st.subheader("📈 予測結果")
    
    # グラフ表示
    fig = create_forecast_plot(df_train, df_test, forecast_df, df_item['店舗'].iloc[0] if '店舗' in df_item.columns else '店舗1', selected_item)
    st.plotly_chart(fig, use_container_width=True)
    
    # 精度指標表示
    if metrics:
        st.subheader("📊 予測精度")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("MAE", f"{metrics['MAE']:.2f}")
        with col2:
            st.metric("RMSE", f"{metrics['RMSE']:.2f}")
        with col3:
            st.metric("MAPE", f"{metrics['MAPE']:.1f}%")
        with col4:
            st.metric("MSE", f"{metrics['MSE']:.2f}")
    
    # 予測結果テーブル
    st.subheader("📋 予測結果詳細")
    result_df = df_test[['日付', '販売個数']].copy()
    result_df['予測値'] = forecast_df['予測値'].values
    result_df['誤差'] = result_df['販売個数'] - result_df['予測値']
    result_df['誤差率(%)'] = (result_df['誤差'] / result_df['販売個数'] * 100).round(1)
    
    st.dataframe(
        result_df.rename(columns={
            '日付': '日付',
            '販売個数': '実績',
            '予測値': '予測値',
            '誤差': '誤差',
            '誤差率(%)': '誤差率(%)'
        }),
        use_container_width=True
    )


def main():
    """メイン関数"""
    st.markdown('<h1 class="main-header">📈 需要予測</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">時系列データを使用して将来の需要を予測します</p>', unsafe_allow_html=True)
    
    # データ読み込み
    df, warning_message = load_demand_data()
    
    if df is None:
        st.error("データを読み込めませんでした。")
        return
    
    if warning_message:
        st.warning(warning_message)
    
    # データフィルタリング（1店舗のみを想定）
    if '店舗' in df.columns:
        store_name = df['店舗'].iloc[0]
        df_filtered = df[df['店舗'] == store_name].copy()
    else:
        df_filtered = df.copy()
    
    df_filtered = df_filtered.sort_values('日付').reset_index(drop=True)
    
    # データ概要表示
    display_data_overview(df_filtered)
    
    # 商品選択
    available_items = sorted(df_filtered['商品'].unique())
    selected_item = st.selectbox("商品を選択:", available_items)
    
    # 選択された商品でさらにフィルタリング
    df_item = df_filtered[df_filtered['商品'] == selected_item].copy()
    
    # 売上推移表示
    display_sales_trend(df_item, selected_item)
    
    # 統計情報表示
    display_statistics(df_item)
    
    # 予測設定取得
    split_datetime = get_forecast_settings(df_item)
    
    # 予測実行ボタン
    if st.button("🚀 予測実行", type="primary"):
        execute_forecast(df_item, split_datetime, selected_item)

if __name__ == "__main__":
    main() 