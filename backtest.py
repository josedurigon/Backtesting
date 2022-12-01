import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import pandas_datareader as pdr
import mplfinance as mpf
import matplotlib.dates as mpl_dates
yf.pdr_override()
now = dt.datetime.now()

stock = input("Enter the ticker: ")
startyear = 2010
month = 1
day = 1

start = dt.datetime(startyear, month, day)

df = pdr.get_data_yahoo(stock,start, now)

ma = 50
smaString = f"SMA{ma}"

df[smaString] = df['Close'].rolling(window=ma).mean()
df = df.iloc[ma:]

countabove=0
countlower=0
'''
for i in df.index:
    #print(df["Close"][i],df[smaString][i])
    if(df["Close"][i]>df[smaString][i]):
        countabove+=1
    else:
        countlower+=1

print(f"Quantas vezes a ação fechou abaixo da média: {countlower}") 
print(f"Quantas vezes fechou acima da média: {countabove}")
'''

emasused=[3,8,20,200]
for x in emasused:
    ema=x
    df["ema_"+str(ema)] = df["Close"].ewm(span=ema, adjust=False).mean()

print(df)
for i in df.index:
    if((df["ema_3"][i]<df["ema_8"]).any() & (df["ema_8"][i]<df["ema_20"][i]).any()):
        print(f"Agulhada de compra acontecendo! {i}")
    
    elif((df["ema_3"][i] == df["ema_8"]).any() & (df["ema_20"][i]==df["ema_8"][i])).any():
        print(f"Agulhada prestes a acontecer! {i}")
    
    elif((df["ema_20"][i]<df["ema_8"][i]).any() & (df["ema_3"][i]>df["ema_8"][i])).any():
        print(f"Agulhada de venda ocorrendo! {i}")

    else:
        continue

    

mpf.plot(df, type='candle', mav=(3,8,20))
'''
fig, ax = plt.subplots()
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle(f'Daily Candlestick Chart of {stock}')

date_format = mpl_dates.DateFormatter('%d-%m-%y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

fig.tight_layout()

plt.show()
'''

