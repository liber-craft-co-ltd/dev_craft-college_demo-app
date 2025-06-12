# 🎓 Craft College デモアプリ

[Craft College 無料相談会用デモアプリケーション](https://dev-craft-college-demo-app.streamlit.app/)

---

本リポジトリは、AI・データサイエンスの実践的な技術を体験できるStreamlitデモアプリケーションです。実際の講座で学べる内容を体験していただけます。

## 📋 機能一覧

### 📊 データ分析
- **学習内容**: データの可視化技術、統計分析の基礎、グラフの作成と解釈
- **使用技術**: Python, Pandas, Plotly, 統計学
- **実務活用**: 売上分析、顧客分析、KPI監視
- **データセット**: スーパーマーケットの売上データ

### 📈 需要予測
- **学習内容**: 時系列データ分析、予測モデルの構築、季節性・トレンドの把握
- **使用技術**: Prophet, SARIMAX, 時系列分析
- **実務活用**: 在庫管理、売上予測、需要計画
- **データセット**: 店舗・商品別の需要予測データ

### 📚 レコメンド
- **学習内容**: 推薦システムの仕組み、コンテンツベースフィルタリング、協調フィルタリング
- **使用技術**: scikit-learn, TF-IDF, SVD
- **実務活用**: ECサイト、動画配信、音楽配信
- **データセット**: 書籍推薦データ

### 🤖 AIチャットボット
- **学習内容**: 生成AIの活用方法、プロンプトエンジニアリング、対話システムの構築
- **使用技術**: OpenAI GPT-4, API連携
- **実務活用**: カスタマーサポート、FAQ、相談窓口

## 🚀 セットアップ手順

### 前提条件
- Python 3.13
- pip パッケージマネージャー

### インストール

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd dev_craft-college_demo-app
```

2. **仮想環境の作成（推奨）**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **環境変数の設定（AIチャットボット機能を使用する場合）**
```bash
# .envファイルを作成してOpenAI APIキーを設定
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 実行方法

```bash
streamlit run main.py
```

ブラウザで `http://localhost:8501` にアクセスしてアプリを表示します。

## 🛠️ 技術スタック

### フロントエンド
- **Streamlit**: Webアプリケーションフレームワーク
- **Plotly**: インタラクティブなデータ可視化
- **Altair**: 宣言的統計可視化

### データサイエンス・機械学習
- **Pandas**: データ操作・分析
- **NumPy**: 数値計算
- **scikit-learn**: 機械学習ライブラリ
- **Prophet**: 時系列予測
- **Statsmodels**: 統計モデリング

### AI・自然言語処理
- **OpenAI API**: 生成AI・チャットボット機能
- **python-dotenv**: 環境変数管理

### データ可視化
- **Matplotlib**: 基本的なグラフ作成
- **Seaborn**: 統計的データ可視化
- **japanize-matplotlib**: 日本語フォント対応

## 📁 プロジェクト構造

```
dev_craft-college_demo-app/
├── main.py                    # メインアプリケーション
├── requirements.txt           # 依存関係
├── pages/                     # 各機能のページ
│   ├── 0_top.py               # トップページ
│   ├── 1_analytics.py         # データ分析
│   ├── 2_demand_forecast.py   # 需要予測
│   ├── 3_recommendation.py    # レコメンド
│   └── 4_ai_chatbot.py        # AIチャットボット
├── data/                      # データファイル
│   ├── input/                 # 入力データセット
│   │   ├── supermarket_analysis.csv
│   │   ├── store_item_demand_forecast.csv
│   │   └── books_recommendation.csv
│   └── assets/                # 画像・アイコン
```

## 🎯 学習の進め方

1. **データ分析**: まずはデータを理解し、可視化の基礎を学ぶ
2. **需要予測**: 時系列データの特性と予測手法を体験
3. **レコメンド**: 機械学習による推薦システムを構築
4. **AIチャットボット**: 最新のAI技術を活用した対話システム

## 📞 お問い合わせ

Craft College の講座内容や無料相談会については、デモアプリ内のお問い合わせフォームまたは公式サイトをご確認ください。

---

**Craft College** - AI・データサイエンスの実践的な学習を提供
