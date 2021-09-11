from pandas.core.indexes.base import Index
import requests
import pandas as pd
from secrets import token
import numpy as np
import streamlit as st 

st.title('S&P500 List for Equal Portion')

symbolCsv=pd.read_csv('symbols.csv')


symbol=symbolCsv['Symbol']

my_columns=['Ticker', 'Price','Market Capitalization', 'Number Of Shares to Buy']

final_dataframe=pd.DataFrame(columns=my_columns)

ls2=[]

def chunks(lst):
    for i in range(0,len(lst),100):
        ls2.append(lst[i:i+100])

chunks(list(symbol))

zzls=[]

for i in ls2:
    zzls.append(','.join(i))

final_dataframe = pd.DataFrame(columns = my_columns)


for i in zzls:

    batch_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={i}&token={token}'
    data = requests.get(batch_url).json()
    for symbol in i.split(','):
        final_dataframe = final_dataframe.append(
                                        pd.Series([symbol, 
                                                   data[symbol]['quote']['latestPrice'], 
                                                   data[symbol]['quote']['marketCap'], 
                                                   'N/A'], 
                                                  index = my_columns), 
                                        ignore_index = True)


portfolio_size=st.number_input('Enter the size of your portfolio\n',10000000)

try:
    val=float(portfolio_size)
except ValueError:
    print('Not a Valid Number\n Try Again:')
    portfolio_size=input('Enter the size of your portfolio')


portion_size=float(portfolio_size)/len(final_dataframe.index)

final_dataframe['Number Of Shares to Buy']=portion_size/final_dataframe['Price']

final_dataframe['Number Of Shares to Buy']=final_dataframe['Number Of Shares to Buy'].apply(np.floor)

final_dataframe.index = [""] * len(final_dataframe)

st.table(final_dataframe)

#final_dataframe.to_excel('FinalOutput.xlsx',index=False)





