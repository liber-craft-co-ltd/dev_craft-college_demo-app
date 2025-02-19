import pandas as pd
import os
from itertools import combinations
from collections import defaultdict

# ファイルパス
user_data_path = "user_data/"  # ユーザーデータが格納されているフォルダ
product_data_path = "product_data/product_data.csv"  # 商品データのパス
output_path = "product_data/product_similarity.csv"  # 結果の保存先

# すべてのユーザーデータを統合
user_files = [os.path.join(user_data_path, f) for f in os.listdir(user_data_path) if f.endswith(".csv")]
user_data = pd.concat([pd.read_csv(f) for f in user_files])

# 商品データを読み込み（商品ID → 商品名 の対応）
product_data = pd.read_csv(product_data_path)
product_dict = dict(zip(product_data["商品ID"], product_data["商品名"]))  # 商品ID → 商品名 の辞書

# 共起行列を作成（商品ペアの共起回数を記録）
co_occurrence = defaultdict(int)

# ユーザーごとに処理
for _, group in user_data.groupby("ユーザーID"):
    product_ids = group["商品ID"].unique()  # ユーザーが購入した商品のユニークなリスト
    for pair in combinations(product_ids, 2):
        co_occurrence[pair] += 1
        co_occurrence[(pair[1], pair[0])] += 1  # 対称性を確保

# 各商品の購入回数をカウント
product_counts = user_data["商品ID"].value_counts().to_dict()

# Jaccard類似度を計算
jaccard_results = []
for (p1, p2), count in co_occurrence.items():
    total_purchases = product_counts[p1] + product_counts[p2] - count
    jaccard_similarity = count / total_purchases  # Jaccard係数
    jaccard_results.append({
        "商品名1": product_dict[p1],
        "商品名2": product_dict[p2],
        "関連度": round(jaccard_similarity, 4)  # 小数点4桁
    })

# データフレーム化
jaccard_df = pd.DataFrame(jaccard_results)

# 1. 商品名1と商品名2が同じ場合に関連度を1に設定
jaccard_df['関連度'] = jaccard_df.apply(
    lambda row: 1.0 if row['商品名1'] == row['商品名2'] else row['関連度'], axis=1)

# 2. 商品名が異なる場合に関連度を0〜1の範囲に正規化
min_value = jaccard_df[jaccard_df['商品名1'] != jaccard_df['商品名2']]['関連度'].min()
max_value = jaccard_df[jaccard_df['商品名1'] != jaccard_df['商品名2']]['関連度'].max()

# 正規化（商品名が異なる場合のみ適用）
jaccard_df['関連度'] = jaccard_df.apply(
    lambda row: (row['関連度'] - min_value) / (max_value - min_value)
    if row['商品名1'] != row['商品名2'] else 1.0, axis=1)

# 結果をCSVに保存
jaccard_df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"商品関連度データを {output_path} に保存しました。")
