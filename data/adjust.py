import pandas as pd

# 商品類似度のデータを読み込み
product_similarity = pd.read_csv("data/product_similarity.csv")

# 1. 商品名1と商品名2が同じ場合に関連度を1に設定
product_similarity['関連度'] = product_similarity.apply(
    lambda row: 1.0 if row['商品名1'] == row['商品名2'] else row['関連度'], axis=1)

# 2. 商品名が異なる場合に関連度を0〜1の範囲に正規化
# まずは商品名が異なるペアのみを対象に最小値と最大値を取得
min_value = product_similarity[product_similarity['商品名1'] != product_similarity['商品名2']]['関連度'].min()
max_value = product_similarity[product_similarity['商品名1'] != product_similarity['商品名2']]['関連度'].max()

# 正規化（商品名が異なる場合のみ適用）
product_similarity['関連度'] = product_similarity.apply(
    lambda row: (row['関連度'] - min_value) / (max_value - min_value)
    if row['商品名1'] != row['商品名2'] else 1.0, axis=1)

# 修正後のデータを保存
product_similarity.to_csv("data/product_similarity_adjusted.csv", index=False)
