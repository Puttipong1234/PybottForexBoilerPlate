# ทดสอบเป็น tradingview
import requests

url = 'http://127.0.0.1:5000/webhook/forex'

signal = {'symbol': 'EURUSD' ,
          "lot" : 0.1 ,
          "action" : "OPEN SHORT" }

x = requests.post(url, json = signal)

print(x.text)