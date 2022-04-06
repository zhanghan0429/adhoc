# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:19:21 2022

@author: Eve
"""

import pandas as pd
import numpy as np
import datetime as dt

######### Read input and calculate additional columns based on raw input (input_df) ########
input_df = pd.read_csv("C:\Users\87145\my_project\mirana\Assignment2\input.csv",
                       names=["TimeStamp", "Symbol", "Quantity", "Price"])

# calculate the time gap between each trade partitioned over symbol
input_df = input_df.sort_values(['Symbol','TimeStamp'])
input_df['timegap'] = input_df.groupby('Symbol')['TimeStamp'].diff().fillna(0) #fillna with 0 to make time gap at the start of each new trade 0

#compute total $amount to facilitate the calc of weighted avg price
input_df['Amount']  = input_df['Quantity'] * input_df['Price']


######### group data by symbol (df2) ########

df2 = input_df.groupby('Symbol',as_index=False).agg({'timegap':[('Maxgap','max')],
                       'Quantity':[('Volume','sum')],
                       'Amount':[('Amount','sum')],
                       'Price':[('MaxPrice','max')]})
df2.columns = ['_'.join(col).strip() for col in df2.columns.values] 
df2['WeightedAveragePrice'] = df2['Amount_Amount']/df2['Quantity_Volume']


######### organise output table: renaming and formatting (op)########

cols        = ['Symbol_','timegap_Maxgap','Quantity_Volume','WeightedAveragePrice','Price_MaxPrice']
rename_cols = ['Symbol','MaxTimeGap','Volume','WeightedAveragePrice','MaxPrice']
op          = df2[cols]
op.columns  = rename_cols 

#round non-int columns to int
op = op.applymap(lambda x: int(round(x, 0)) if isinstance(x, (int, float)) else x)

op.to_csv("C:\Users\87145\my_project\mirana\Assignment2\output.csv", index=False, header=False)

#################################################################################################





