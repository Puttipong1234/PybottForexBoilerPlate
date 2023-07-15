from trade import orders , close_orders
import MetaTrader5 as mt5
from flask import Flask , request
import json
import time

app = Flask(__name__)

@app.route('/webhook/forex', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        
        mt5.initialize()
        
        print("Signal from tradingview")
        print("Preparing for an order")
        print("Data incoming : " + str(request.data))
        
        # รับ Data แปลงให้เป็น dictionary
        signal = request.data.decode("utf-8")
        signal = json.loads(signal)
        
        # แยกแยะแล้วจัดเก็บใส่ตัวแปร
        symbol = signal["symbol"]
        lot = float(signal["lot"])
        action = signal["action"].split(" ")[0]
        side = signal["action"].split(" ")[1]
        
        partial = 100
        if action == "CLOSE":
            partial = int(signal["action"].split(" ")[2])
        
        
        # ทำการเปิด orders + ป้องกันการเกิด requote
        while True:
            r = ""
            if action == "OPEN":
                if side == "LONG":
                    r = orders(symbol, lot)
                elif side == "SHORT":
                    r = orders(symbol, lot,buy=False)
            
            elif action == "CLOSE":
                if side == "LONG":
                    r = close_orders(symbol,True ,lot*(partial/100))
                elif side == "SHORT":
                    r = close_orders(symbol,False ,lot*(partial/100))
                    
        # + ป้องกันการเกิด requote
            if r == "Requote":
                time.sleep(0.5)
                continue
            else:
                break
        
        mt5.shutdown()
        
        return request.data , 200
    else:
        return "This is a FOREX service"

if __name__ == '__main__':
    
    app.run(debug=True)
    