import pandas as pd
df = pd.read_csv('data/user_data/user_1.csv')
print(df.head(5))
# リピート購入がある商品の商品IDと購入日時
# st.subheader("リピート購入がある商品の商品IDと購入日時")
    
# 重複購入データの抽出
repeat_purchase = df.groupby(["商品ID"]).size().reset_index(name="購入回数")
print(repeat_purchase)
# # 購入回数が2回以上のデータを抽出
# repeat_purchase = repeat_purchase[repeat_purchase["購入回数"] > 1]
    
# # 商品IDと購入日時の表示
# repeat_purchase_info = repeat_purchase[["商品ID", "購入日時", "購入回数"]]
# st.dataframe(repeat_purchase_info)
