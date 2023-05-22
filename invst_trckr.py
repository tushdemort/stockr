import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import streamlit as st
from datetime import date,timedelta
import datetime
from PIL import Image
import base64
import time


st.title("Investment Tracker")


tckr=st.text_input("Enter Ticker",'MSFT')
money=st.number_input("Enter Amount Invested",min_value=0,max_value=1000,value=100)

st.subheader('Select Starting and Ending Date')
format = '%b %d %Y %I:%M%p'
datetime_str = datetime.datetime.strptime('JAN 1 2010 10:07AM', format)
start= st.date_input("Enter Start Date",datetime_str,min_value=datetime_str)

default_end=date.today() - timedelta(days=1)

end = st.date_input("Enter End Date",default_end,max_value=date.today())

df=pdr.DataReader(tckr,'stooq',start,end)

time_period="Time Period: "+str(start)+" - "+str(end)



df=df.drop(['Open','High','Volume','Low'], axis=1)



tracker=df.copy()



ini=str(start)

for i in range(len(tracker)):
    denom=float(df.iloc[-1]['Close'])
    numer=float(df.iloc[i]['Close'])
    inv_val=(numer/denom)*float(money)
    tracker.iloc[i]['Close']=inv_val


#visual
st.subheader("Current Value")
cur="\$"+str(money)+" invested in "+str(tckr)+" on "+str(start)+" would be worth \$"+str(int(tracker.iloc[0]["Close"]))+" on "+str(end)
st.write(cur)

fig=plt.figure(figsize=(12,6))

plt.plot(tracker.Close)



st.pyplot(fig)
