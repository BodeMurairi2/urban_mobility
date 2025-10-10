#!/usr/bin/env python3

"""This script does quick data cleaning and analyzes"""

import pandas as pd

def get_clean_shape(data:pd.DataFrame):
    """get shape of the dataset"""
    return data.shape()

def get_dataset_info(data:pd.DataFrame):
    """Get general info"""
    return data.info()

def get_dataset_statistical_info(data:pd.DataFrame):
    """return statistical info"""
    return data.describe()

def clean_dataset(data:pd.DataFrame):
    """Get clean data"""
    if data.isna().any().any:
        clean_data = data.drop_duplicates()
        clean_data = clean_data.dropna()
    return clean_data

if __name__ == "__main__":
    get_clean_shape(data=data)
    get_dataset_info(data=data)
    get_dataset_statistical_info(data=data)
    clean_dataset(data=data)
