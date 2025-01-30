import pandas as pd
import random
from datetime import datetime, timedelta

# 全データ生成
def generate_product_data(file_path, num_products=500):
    categories = ["プログラミング", "データサイエンス", "AI", "Web開発", "ネットワーク", "セキュリティ"]
    data = []
    for i in range(1, num_products + 1):
        data.append({
            "商品ID": i,
            "商品名": f"商品{i}",
            "カテゴリ": random.choice(categories),
            "価格": random.randint(1000, 10000),
        })
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    
# 各ユーザーの購入履歴生成
def generate_user_data(directory, product_file, num_users=100, max_purchases=50):
    product_data = pd.read_csv(product_file)
    product_ids = product_data["商品ID"].tolist()

    for user_id in range(1, num_users + 1):
        num_purchases = random.randint(50, max_purchases)  
        data = []
        start_date = datetime(2024, 1, 1)

        for _ in range(num_purchases):
            purchase_date = start_date + timedelta(days=random.randint(1, 300))
            data.append({
                "ユーザーID": user_id,
                "商品ID": random.choice(product_ids),
                "購入日時": purchase_date.strftime("%Y-%m-%d"),
            })

        df = pd.DataFrame(data).sort_values(by="購入日時")
        file_path = f"{directory}/user_{user_id}.csv"
        df.to_csv(file_path, index=False)

# 実行
generate_product_data("data/product_data.csv", num_products=500)  
generate_user_data("data/user_data", "data/product_data.csv", num_users=100, max_purchases=50)  