import warnings
from datetime import datetime
import MetaTrader5 as mt5
warnings.filterwarnings("ignore")


def orders(symbol, lot, buy=True, id_position=None):
       """ Send the orders """

       # Initialize the connection if there is not
       if mt5.initialize() == False:
           mt5.initialize()

       # Get filling mode 
       filling_mode = mt5.symbol_info(symbol).filling_mode - 1

       # Take ask price
       ask_price = mt5.symbol_info_tick(symbol).ask

       # Take bid price
       bid_price = mt5.symbol_info_tick(symbol).bid

       # Take the point of the asset
       point = mt5.symbol_info(symbol).point

       deviation = 20  # mt5.getSlippage(symbol)
       # **************************** Open a trade *****************************
       if id_position == None:

           if buy:
               type_trade = mt5.ORDER_TYPE_BUY
               sl = ask_price*(1-0.5)
               tp = ask_price*(1+0.5)
               price = ask_price

           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_SELL
               sl = bid_price*(1+0.5)
               tp = bid_price*(1-0.5)
               price = bid_price

           # Open the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "price": price,
               "deviation": deviation,
               "sl": sl,
               "tp": tp,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }
           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment

       # **************************** Close a trade *****************************
       else:
           # Buy order Parameters
           if buy:
               type_trade = mt5.ORDER_TYPE_SELL
               price = bid_price

           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_BUY
               price = ask_price

           # Close the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "position": id_position,
               "price": price,
               "deviation": deviation,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }

           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment
       print(result_comment)
       return result.comment
   

def close_orders(sym,is_buy,lot):
    res = mt5.positions_get()
    for i in res:
        if i.symbol == sym:
            res = orders(symbol = i.symbol, lot = lot ,buy=is_buy, id_position=i.ticket)
            return res

if __name__ == '__main__':
    mt5.initialize()
    
    # OPEN POSITION
    
    # res = orders(symbol = "GBPUSD", lot = 0.01)
    # res = orders(symbol = "EURUSD", lot = 0.01 ,buy=True, id_position=1726559659)
    
    
    # CLOSE POSITION
    
    # res = mt5.positions_get()
    # for i in res:
    #     if i.symbol == "GBPUSD":
    #         print(i.ticket)
    #         res = orders(symbol = i.symbol, lot = 0.01 ,buy=True, id_position=i.ticket)
    
    
       