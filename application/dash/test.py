import pandas as pd
import numpy as np
import os, glob
from mlxtend.frequent_patterns import apriori, association_rules

"""
def encode(x):
    if x <= 0.0:
        return 0
    else:
        return 1


data = pd.read_csv("Bakery.csv")

data["date"] = pd.to_datetime(data["DateTime"])
data.drop(columns=["Daypart", "DayType", "DateTime"], inplace=True)

data.dropna()
data.rename(
    {"TransactionNo": "id", "Items": "item", "DateTime": "date"}, axis=1, inplace=True,
)
data["date"] = data["date"].astype(str)

basket = data.groupby(["id", "item"])["item"].count().unstack().reset_index().fillna(0)
basket.drop("id", inplace=True, axis=1)

encoded_basket = basket.applymap(encode)
filtered_basket = encoded_basket[(encoded_basket > 0).sum(axis=1) >= 2]

frequent_itemsets = (
    apriori(filtered_basket, min_support=0.03, use_colnames=True, max_len=3)
    .sort_values("support", ascending=False)
    .reset_index(drop=True)
)

my_rules = (
    association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    .sort_values("lift", ascending=False)
    .reset_index(drop=True)
)

print(my_rules)


path = "/Users/gorelski/Documents/COMP3200-Project/Flask-MBA/application/static/uploads"
csv_files = glob.glob(os.path.join(path, "*.csv"))

for f in csv_files:
      
    # read the csv file
    df = pd.read_csv(f)
      
    # print the location and filename
    print('Location:', f)
    """

df = pd.read_csv("groceries_unpivot.csv")
df.drop(columns=["quantity"], inplace=True)

df_reorder = df[["PurchaseID", "Item", "Date"]]  # rearrange column here
df_reorder.to_csv("groceries_unpivot_reorder.csv", index=False)
print(df_reorder)
