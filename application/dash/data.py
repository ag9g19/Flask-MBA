"""Prepare data for Plotly Dash."""
import os
import glob
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def create_dataframe():
    """Create Pandas DataFrame from local CSV."""
    df = pd.read_csv("Bakery.csv")
    df["date"] = pd.to_datetime(df["DateTime"])
    df.drop(columns=["Daypart", "DayType", "DateTime"], inplace=True)
    return df


def pre_processing(data, metric, trsh):
    data.dropna()
    data.rename(
        {data.columns[0]: "id", data.columns[1]: "item", data.columns[2]: "date"},
        axis=1,
        inplace=True,
    )
    data["date"] = data["date"].astype(str)

    basket = (
        data.groupby(["id", "item"])["item"].count().unstack().reset_index().fillna(0)
    )
    basket.drop("id", inplace=True, axis=1)

    encoded_basket = basket.applymap(encode)
    filtered_basket = encoded_basket[(encoded_basket > 0).sum(axis=1) >= 2]

    frequent_itemsets = (
        apriori(filtered_basket, min_support=0.03, use_colnames=True, max_len=3)
        .sort_values("support", ascending=False)
        .reset_index(drop=True)
    )

    my_rules = (
        association_rules(frequent_itemsets, metric=metric, min_threshold=trsh)
        .sort_values(metric, ascending=False)
        .reset_index(drop=True)
    )

    my_rules["antecedents"] = my_rules["antecedents"].apply(set)
    my_rules["consequents"] = my_rules["consequents"].apply(set)

    my_rules["antecedents"] = my_rules["antecedents"].astype(str)
    my_rules["consequents"] = my_rules["consequents"].astype(str)

    my_rules.drop(["leverage", "conviction"], inplace=True, axis=1)

    return my_rules


def process_bakery(data):
    data.dropna()
    data.rename(
        {data.columns[0]: "id", data.columns[1]: "item", data.columns[2]: "date"},
        axis=1,
        inplace=True,
    )
    data["date"] = pd.to_datetime(data["date"])
    items_count = data.item.value_counts().sort_values(ascending=False)

    return items_count


def process_time(data):
    data["day"] = data["date"].dt.day_name()
    data["month"] = data["date"].dt.month_name()
    data["year"] = data["date"].dt.year

    return data


def items_by_day(data):
    data = process_time(data)
    items_per_day = data.groupby("day")["item"].count().sort_values(ascending=False)

    return items_per_day


def items_by_month(data):
    data = process_time(data)
    items_per_month = data.groupby("month")["item"].count().sort_values(ascending=False)

    return items_per_month


def encode(x):
    if x <= 0.0:
        return 0
    else:
        return 1
