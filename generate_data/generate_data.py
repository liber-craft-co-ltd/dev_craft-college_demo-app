import pandas as pd
import random
from datetime import datetime, timedelta
import os

# 新しいカテゴリリスト（12種類）
base_product_names = {
    "プログラミング": [
        "Python入門", "Javaマスター", "C++徹底攻略", "Go言語実践", "Rustプログラミング", "Swift基礎",
        "Ruby基礎", "Perl活用", "C#実践", "Kotlin開発", "プログラム設計", "アルゴリズムとデータ構造",
        "システム開発", "ソフトウェアテスト", "オブジェクト指向プログラミング", "デザインパターン",
        "関数型プログラミング", "アセンブリ言語入門", "Webスクレイピング", "自動化スクリプト",
        "ゲームプログラミング", "競技プログラミング", "AIプログラミング", "低レイヤープログラミング",
        "プログラミング入門", "エラー処理", "コード最適化", "モダンJavaScript", "TypeScript入門",
        "プログラムデバッグ", "テスト駆動開発", "フレームワーク活用", "プログラミング言語の歴史"
    ],
    "データサイエンス": [
        "データ分析基礎", "統計学入門", "機械学習モデル構築", "Pythonでデータ処理", "SQLデータ分析",
        "データ可視化", "ビッグデータ解析", "データクレンジング", "R言語活用", "データエンジニアリング",
        "統計モデリング", "時系列分析", "データマイニング", "Pythonデータ分析", "データアナリスト入門",
        "回帰分析", "教師なし学習", "ディープラーニング基礎", "AIデータ分析", "データサイエンスとビジネス",
        "データパイプライン構築", "クラスタリング技術", "異常検知", "データウェアハウス入門",
        "データドリブン戦略", "データスクリーニング", "統計的仮説検定", "データ統計入門"
    ],
    "AI": [
        "深層学習入門", "強化学習実践", "AIモデル最適化", "自然言語処理", "画像認識技術", "音声認識AI",
        "GAN活用", "Transformer入門", "自動運転AI", "AI倫理", "AIの未来", "AIプログラム基礎",
        "AIとビジネス", "AIチャットボット開発", "AIアプリ開発", "AIとデータサイエンス",
        "ディープラーニング入門", "AIで株価予測", "AIによる画像分類", "AI技術の実践"
    ],
    "クラウドコンピューティング": [
        "AWS入門", "Azure実践", "GCP活用", "クラウドアーキテクチャ", "サーバーレス開発",
        "Kubernetes基礎", "Docker活用", "クラウドセキュリティ", "分散コンピューティング",
        "ハイブリッドクラウド戦略", "クラウド運用", "マイクロサービス", "DevOpsとCI/CD",
        "クラウドデータストレージ", "クラウドネイティブアプリ", "クラウドコスト最適化"
    ],
    "サイバーセキュリティ": [
        "ネットワークセキュリティ", "情報セキュリティ管理", "暗号技術", "ペネトレーションテスト",
        "脆弱性診断", "マルウェア解析", "エシカルハッキング", "セキュアコーディング",
        "ゼロトラストセキュリティ", "SOCとSIEM", "セキュリティオペレーション"
    ],
    "ブロックチェーン": [
        "ブロックチェーン基礎", "Ethereum開発", "スマートコントラクト", "NFTとメタバース",
        "暗号通貨技術", "分散型アプリ開発", "DeFiと金融革命", "ハッシュアルゴリズム"
    ],
    "データベース": [
        "SQL入門", "NoSQL活用", "データベース設計", "分散データベース", "データモデリング",
        "トランザクション管理", "データベースパフォーマンス最適化"
    ],
    "Web開発": [
        "HTML/CSS基礎", "JavaScriptフレームワーク", "React入門", "Vue.js開発", "フロントエンド最適化",
        "WebAPI設計", "バックエンド開発", "フルスタック開発", "Next.js活用", "GraphQL入門"
    ],
    "モバイルアプリ": [
        "Android開発", "iOSアプリ開発", "React Native入門", "Flutter実践", "SwiftUI開発"
    ],
    "ゲーム開発": [
        "Unityゲーム開発", "Unreal Engine活用", "ゲームデザイン理論", "3Dモデリング技術",
        "物理エンジン実装", "ゲームAI開発"
    ],
    "IoT": [
        "IoT基礎", "スマートデバイス開発", "エッジコンピューティング", "組み込みシステム",
        "センサーデータ処理", "IoTセキュリティ"
    ],
    "ロボティクス": [
        "ロボット制御", "ROSプログラミング", "自律移動ロボット", "ロボットアーム制御",
        "ヒューマノイド開発", "ロボティクスAI"
    ]
}

def generate_product_data(file_path):
    data = []
    product_id = 1
    
    for category, products in base_product_names.items():
        for product in products:
            data.append({
                "商品ID": product_id,
                "商品名": product,
                "カテゴリ": category,
                "価格": random.randint(1000, 10000)
            })
            product_id += 1
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def generate_user_data(directory, product_file, num_users=100, max_purchases=50):
    os.makedirs(directory, exist_ok=True)
    product_data = pd.read_csv(product_file)
    product_ids = product_data["商品ID"].tolist()
    
    for user_id in range(1, num_users + 1):
        num_purchases = random.randint(10, max_purchases)
        data = []
        start_date = datetime(2024, 1, 1)
        
        for _ in range(num_purchases):
            purchase_date = start_date + timedelta(days=random.randint(1, 300))
            data.append({
                "ユーザーID": user_id,
                "商品ID": random.choice(product_ids),
                "購入日時": purchase_date.strftime("%Y-%m-%d")
            })
        
        df = pd.DataFrame(data).sort_values(by="購入日時")
        file_path = os.path.join(directory, f"user_{user_id}.csv")
        df.to_csv(file_path, index=False)

# 実行
generate_product_data("product_data/product_data.csv")
generate_user_data("user_data", "product_data/product_data.csv", num_users=100, max_purchases=50)

# 苗字リスト
names = [
    "山田", "佐藤", "鈴木", "田中", "高橋", "伊藤", "渡辺", "中村", "小林", "加藤",
    "吉田", "山本", "松本", "井上", "斉藤", "林", "清水", "山口", "田村", "藤田",
    "岡田", "松田", "石田", "原田", "中島", "石井", "近藤", "上田", "森", "野村",
    "大塚", "土屋", "桜井", "大久保", "川上", "坂本", "宮崎", "内田", "水野", "新井",
    "高田", "菅原", "西村", "大西", "福田", "村田", "木下", "星野", "中田", "岡本",
    "藤井", "中川", "武田", "安藤", "平野", "川口", "宮本", "島田", "堀", "野田",
    "本田", "片山", "杉山", "川崎", "森田", "竹内", "松井", "橋本", "和田", "今村",
    "吉川", "原", "服部", "村上", "大石", "横山", "堀内", "長谷川", "植田", "青木",
    "高木", "山下", "平田", "野口", "坂井", "宮田", "長尾", "石川", "中沢", "谷口",
    "金子", "伊東", "片岡", "神田", "宮川", "望月", "木村", "大野", "矢野", "小野"
]

def renane_csv_files(d):
    files = [f for f in os.listdir(d) if f.startswith('user_') and f.endswith('.csv')]
    
    for file in files:
        # 数字部分の抽出
        n = file.replace('user_', '').replace('.csv', '')
        
        if n.isdigit():
            index = int(n) - 1
            
            if 0 <= index < len(names):
                new_name = f'{n}.{names[index]}.csv'
                old_path = os.path.join(d, file)
                new_path = os.path.join(d, new_name)
                
                # ファイル名変更
                os.rename(old_path, new_path)

renane_csv_files('user_data/')