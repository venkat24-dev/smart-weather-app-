#%% md
# Importing Libraries
#%%

#%%
import urllib.request as urllib2
import json
import time
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split  
#%%
import warnings
warnings.filterwarnings("ignore")
#%% md
# Thingspeak Configuration
#%%
READ_API_KEY= 'SZZOVTJU2AR48WK1'
CHANNEL_ID= '2868552'
#%%
# while True:
TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))

response = TS.read()
data=json.loads(response)


a = data['created_at']
b = data['field1']
c = data['field2']
d = data['field3']
e = data['field4']
f = data['field5']
g = data['field6']
print (a + "    " + b + "    " + c + "    " + d + "    " + e + "    " + f + "    " + g)
time.sleep(5)   

TS.close()
#%% md
# Reading the Dataset
#%%
ds=pd.read_csv("venkat file\webpage\ml backend\weatherAUS.csv")  
#%%
import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

#%%
ds.head()    
#%% md
# Cleaning the Dataset
#%%
ds = ds.drop(columns = ['Location','Evaporation', 'Sunshine', 'WindGustDir', 'WindGustSpeed', 'WindDir9am','WindDir3pm','WindSpeed9am', 'WindSpeed3pm', 'Cloud9am', 'Cloud3pm'])
#%%
ds.head()
#%%
ds['Humidity'] = ds[['Humidity9am', 'Humidity3pm']].mean(axis=1)
ds['Pressure'] = ds[['Pressure9am', 'Pressure3pm']].mean(axis=1)
ds['Temperature'] = ds[['Temp9am', 'Temp3pm']].mean(axis=1)
ds = ds.drop(columns = ['Humidity9am', 'Humidity3pm','Pressure9am', 'Pressure3pm','Temp9am', 'Temp3pm'])
new_cols = ['Date','MinTemp', 'MaxTemp', 'Humidity', 'Pressure', 'Temperature', 'RainToday', 'RainTomorrow']
ds = ds.reindex(columns=new_cols)
ds.head()
#%%
ds.isnull().sum()
#%%
ds = ds.dropna()
#%%
ds.isnull().sum()
#%% md

# Splitting the Dependent and Independent Variables
#%%
x = ds.iloc[:,1:7]
display(x.head())
#%%
y = ds.iloc[:,7]
display(y.head())
#%% md
# One Hot Encoding
#%%
x_encoded = pd.get_dummies(x, columns=['RainToday'], drop_first=True)
x_encoded.rename(columns = {'RainToday_Yes':'RainToday'}, inplace = True)
x_encoded.head()
#%%
y_encoded = pd.get_dummies(y, columns=['RainTomorrow'], drop_first=True)
y_encoded.rename(columns = {'Yes':'RainTomorrow'}, inplace = True)
y_encoded.head()
#%% md
# Splitting the Train and Test Data
#%%
x_train, x_test, y_train, y_test = train_test_split(x_encoded, y_encoded, test_size = 0.20, random_state=0)  
#%% md
# Model Building
#%%
from sklearn.ensemble import RandomForestClassifier
model_rf = RandomForestClassifier()
model_rf.fit(x_train,y_train)
#%% md
# Predicting using Test Data
#%%
pred = model_rf.predict(x_test)
#%%
from sklearn.metrics import accuracy_score
accuracy_score(y_test, pred, normalize = True)
#%% md
# Predicting for the Actual Data from the Sensors
#%%
import requests
import pandas as pd
import time
from datetime import datetime, timezone

CHANNEL_ID = "2868552"
READ_API_KEY = "SZZOVTJU2AR48WK1"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=5"

columns = ["Timestamp", "Temperature", "Humidity", "Rain Digital", "Rain Analog", "Gas Level", "Soil Moisture"]
df_live = pd.DataFrame(columns=columns)

while True:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        feeds = data.get("feeds", [])

        if not feeds:
            print("⚠️ No data received from ThingSpeak!")
            time.sleep(10)
            continue

        latest_entry = feeds[-1]  
        timestamp = latest_entry.get("created_at", None)

        if timestamp:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            current_time = datetime.now(timezone.utc)
            time_difference = (current_time - timestamp_dt).total_seconds()

            print(f"🕒 Latest Data Timestamp: {timestamp_dt} (Difference: {time_difference} sec)")

            if time_difference <= 60:  # Check if data is within the last minute
                new_data = {
                    "Timestamp": timestamp,
                    "Temperature": latest_entry.get("field1", None),
                    "Humidity": latest_entry.get("field2", None),
                    "Rain Digital": latest_entry.get("field3", None),
                    "Rain Analog": latest_entry.get("field4", None),
                    "Gas Level": latest_entry.get("field5", None),
                    "Soil Moisture": latest_entry.get("field6", None)
                }

                df_live = pd.concat([df_live, pd.DataFrame([new_data])], ignore_index=True)
                print(f"✅ Data recorded: {new_data}")

                csv_path = "/kaggle/working/live_weather_data.csv"
                df_live.to_csv(csv_path, index=False)

                break
            else:
                print("⚠️ No recent data found in the last 1 minute, waiting...")

        else:
            print("❌ No timestamp found in latest data!")

    else:
        print(f"❌ Failed to fetch data! HTTP Status Code: {response.status_code}")

    time.sleep(10)  # Check for every 10 seconds

#%%
df_live.head()  

#%%
df_live.head()

#%%
df_live.rename(columns = {'created_at':'Data and Time','entry_id':'Sr No.','field1':'Temperature', 'field2':'Humidity','field3':'Dew Point','field4':'Pressure','field5':'Altitude','field6':'Rainfall'},inplace = True)
df_live.head()
#%%
df_live[['Temperature', 'Humidity', 'Rain Analog', 'Gas Level', 'Soil Moisture']] = df_live[[
    'Temperature', 'Humidity', 'Rain Analog', 'Gas Level', 'Soil Moisture']].apply(pd.to_numeric, errors='coerce')

min_temp = df_live['Temperature'].min()
print('Min_Temp:', min_temp)

max_temp = df_live['Temperature'].max()
print('Max_Temp:', max_temp)


humidity = df_live['Humidity'].mean()
print('Humidity:', humidity)

pressure = df_live['Gas Level'].mean()
print('Pressure:', pressure)

temp = df_live['Temperature'].mean()
print('Temperature:', temp)

if df_live['Rain Analog'].mean() < 750:
    rain_today = 0
    print('Rainfall Today: No')
else:
    rain_today = 1
    print('Rainfall Today: Yes')

# Get the latest timestamp
prediction_date = df_live['Timestamp'].max()
print(f"Prediction Date: {prediction_date}")

#%%
print( df_live.columns.str.strip())  

#%%
print( df_live.columns)

#%%
print("project ended")
#%%
import numpy as np
import requests

# # Modify test data to simulate rainy conditions
# min_temp = 18  # Lower temperature
# max_temp = 22  # Lower temperature
# humidity = 90  # High humidity

# pressure = 990  # Low pressure
# temp = 20  # Moderate temperature
# rain_today = 1  # Indicates it rained today


test_data = np.array([[min_temp, max_temp, humidity, pressure, temp, rain_today]])

# Make prediction
rain_predict = model_rf.predict(test_data)[0]  # first element from the array

# Print prediction
if rain_predict == 1:
    print("Yes, it will rain tomorrow")
else:
    print("No, it won't rain tomorrow")

TELEGRAM_BOT_TOKEN = "7793358427:AAEshxCzFy_qTbAXx3LawZRlFWFiNVA5mPQ"

TELEGRAM_CHAT_ID = "1814731517"

# Function to send message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)  
    return response.json()

# Define prediction text
if rain_predict == 5:
    prediction_text = "☀️ Prediction: No rain tomorrow!"
else:
    prediction_text = "🌧️ Prediction: It will rain tomorrow!"
send_telegram_message(prediction_text)

#%%
print("project ended with telegram alert")