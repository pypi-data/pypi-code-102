from base import Node,FIFOQueue
from helper import empty,initialize,run_simulation
import pandas as pd
from datetime import datetime

def run(data,date_column:str,sku_column:str,store_column:str,num_ordering_types:int,
        ordering_columns:list, demand_column:str,date_start:str,date_end:str,shelf_life:int,output_filepath:str):
    
    results=[]
    data[date_column] = data[date_column].apply(lambda x: datetime.strptime(x,"%Y-%m-%d"))
    data.sort_values(by=date_column,inplace=True)
    date_start = datetime.strptime(date_start,"%Y-%m-%d")
    date_end = datetime.strptime(date_end,"%Y-%m-%d")
    data = data[(data[date_column]>=date_start) & (date_end >= data[date_column] )]
    data.reset_index(inplace=True)

    for ord_type in range(num_ordering_types):
        ord_col = ordering_columns[ord_type]
        data_temp = data[[date_column,store_column,sku_column,ord_col,demand_column]]
        days = len(data)
        number = len(data_temp[store_column].unique())*len(data_temp[sku_column].unique())

        q = initialize(ord_col,shelf_life,data_temp,number)
        res = run_simulation(q,days,data_temp)
        res = empty(res,q)
        results.append(res)
    results_df = pd.concat(results,axis= 1, join="inner")
    return results_df

    

        



