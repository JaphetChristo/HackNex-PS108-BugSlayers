import pandas as pd


def total(column):
    return column.sum()


def average(column):
    return column.mean()


def count(column):
    return column.count()


def minimum(column):
    return column.min()


def maximum(column):
    return column.max()


def percentage_change(old_value, new_value):
    if old_value == 0:
        return None

    return ((new_value - old_value) / old_value) * 100


def group_sum(df, group_column, value_column):
    return df.groupby(group_column)[value_column].sum()


def sort_descending(df, column):
    return df.sort_values(by=column, ascending=False)