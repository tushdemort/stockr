import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import streamlit as st
from datetime import date,timedelta
import datetime
from PIL import Image
import base64
import time



st.title("Stock trender")

tckr=st.text_input("Enter ticker",'MSFT')

st.subheader('Select Starting and Ending Date')
format = '%b %d %Y %I:%M%p'
datetime_str = datetime.datetime.strptime('JAN 1 2010 10:07AM', format)
start= st.date_input("Enter Start Date",datetime_str,min_value=datetime_str)

default_end=date.today() - timedelta(days=1)

end = st.date_input("Enter End Date",default_end,max_value=date.today())

df=pdr.DataReader(tckr,'stooq',start,end)

time_period="Time Period: "+str(start)+" - "+str(end)

st.subheader(time_period)


st.write(df)

#visual
st.subheader("Closing vs time with 100 and 200 moving average")
mv100= df.Close.rolling(100).mean()
mv200= df.Close.rolling(200).mean()

rsi=df.Close.rolling(300).mean()






   

"""option = st.selectbox(
     'Indicators',
    ('100 Moving Average', '200 Moving Average', 'RSI'))   """ 
mv100_check=st.checkbox("100 moving avg")
mv200_check=st.checkbox("200 moving avg")

       

fig=plt.figure(figsize=(12,6))
plt.plot(df.Close)


if mv100_check:
  plt.plot(mv100)
if mv200_check:
  plt.plot(mv200)  





st.pyplot(fig)

#pred
data_train=pd.DataFrame(df['Close'][0:int(len(df)*0.75)])
data_test=pd.DataFrame(df['Close'][int(len(df)*0.75):int(len(df))])
 
scaler=MinMaxScaler(feature_range=(0,1))

data_train_array=scaler.fit_transform(data_train)


#load model
model=load_model('keras_model_250.h5')

#testing
past100days=data_train.tail(100)
finaldf= past100days.append(data_test)
finaldf=finaldf.iloc[::-1]
input_data=scaler.fit_transform(finaldf)

x_test=[]
y_test=[]
for i in range(100,input_data.shape[0]):
  x_test.append(input_data[i-100:i])
  y_test.append(input_data[i,0])
x_test,y_test=np.array(x_test),np.array(y_test)
y_pred=model.predict(x_test)
factor=scaler.scale_[0]
factor=float(factor)
scale_factor=1/factor
y_pred=y_pred*scale_factor
y_test=y_test*scale_factor
lstm_head="LSTM Predicition: "+str(tckr)
st.subheader(lstm_head)
pred_fig=plt.figure(figsize=(12,6))
plt.plot(y_test,'b', label="original price")
plt.plot(y_pred,'r',label="pred price")
plt.xlabel('Time')
plt.ylabel('price')
plt.legend()
st.pyplot(pred_fig)


#formatting

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


