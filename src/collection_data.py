import networkx as nx
import numpy as np
import openpyxl
import pandas as pd
import glob as g
import re
import csv
import matplotlib.pyplot as plt
from pandas_datareader import data as sdw
import time
import tqdm


root = "../files/"

filename = "nikkei225.csv"

tickerdata=pd.read_csv(root+'nikkei.csv',header=None)
stockname = pd.read_csv(root+'data_j.csv',encoding="UTF-8")
df = pd.DataFrame()

ticker = [str(tck) for tck in list(tickerdata[0])]
count = 0
for t in ticker:
    tj = t+".T"
    try:
        df[t] = sdw.DataReader(tj,data_source='yahoo',start='2022-01-01',end='2022-06-01')['Adj Close']
    except:
        print("error")
    count += 1
    if count % 5 == 0:
        time.sleep(10)

df.to_csv(root+filename)
print(df.head())

df = pd.read_csv(root+filename,index_col=0)



stock_returns = (df-df.shift(1))/df.shift(1)
# print(df_col,df_row,col,row)
df_stock_returns = stock_returns.drop(index='2022-01-04')

stock_std = pd.DataFrame(df_stock_returns.var(), columns=['variance'])
stock_mean = pd.DataFrame(df_stock_returns.mean(),columns=['mean'])
stock_sharp = pd.DataFrame(df_stock_returns.mean()/df_stock_returns.std(),columns=['sharpe_ratio'])
stock_median = pd.DataFrame(df_stock_returns.median(), columns=['median'])
stock_max = pd.DataFrame(df_stock_returns.max(),columns=['max'])
stock_min = pd.DataFrame(df_stock_returns.min(),columns=['min'])
# print(df.iloc[1,1],df_col[1],df_row[0])
# stock_increse = 
# print(df_stock_returns.head(),len(df_stock_returns.index),len(df_stock_returns.columns))
# print(stock_std.head(),len(stock_std.index),len(stock_std.columns))
# print(stock_mean.head())
# print(stock_median.head())
# print(df_stock_returns.describe())

df_stock = pd.concat([stock_mean,stock_median,stock_min,stock_max,stock_std],axis=1)

print(df_stock)
print(stockname)
brand = []
df_col = df_stock.columns
df_row = df_stock.index
col = len(df_col)
row = len(df_row)
# print(col,row)
# print(stockname.iloc[1,2])
for i in range(row):
    for j in range(len(stockname)):
        if int(df_row[i]) == int(stockname.iloc[j,2]):
            brand.append(stockname.iloc[j,3])
            # print("ticker : {} stock code : {} stock brand : {}".format(df_row[i],stockname.iloc[j,2],stockname.iloc[j,3]))
            
# print(brand)
df = df_stock.assign(brand=brand)
print(df)
df.to_csv(root+"nikkei225_returns.csv",encoding="UTF-8")