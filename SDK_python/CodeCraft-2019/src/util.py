#-*- coding: UTF-8 -*-
import pandas as  pd
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip('#?(?)?')
    data[data.columns[0]] = data[data.columns[0]].str.lstrip('(').apply(pd.to_numeric)
    data[data.columns[data.columns.size - 1]] = data[data.columns[data.columns.size - 1]].str.rstrip(')').apply(
        pd.to_numeric)
    return data
