# ทดสอบเป็น tradingview
import requests

url = 'http://127.0.0.1:5000/webhook'

signal = {'symbol': 'EURUSD' ,
          "lot" : 0.5 ,
          "action" : "CLOSE SHORT 50" }

x = requests.post(url, json = signal)

print(x.text)