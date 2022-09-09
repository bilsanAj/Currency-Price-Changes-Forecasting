from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
import dash 
from dash.dependencies import Output, Input
import dash_core_components as dcc 
import pandas as pd
import mplfinance as mpf
import MetaTrader5 as mt5
import dash_html_components as html 
import plotly 
import plotly.graph_objs as go 
from django_plotly_dash import DjangoDash
from datetime import datetime,timedelta
import json
from django.views import View
import pytz
import re
import time
from django.utils import timezone
from django.template import RequestContext,loader
from statsmodels.tsa.statespace.sarimax import SARIMAX 
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

class allData(View):
    graphParameters =[]
    def get(self,requiest):
        self.graphParameters.clear()
        Symbol = requiest.GET.get('Symbol', None)
        timeFrames = requiest.GET.get('timeFrames', None)
        self.graphParameters.append(Symbol)
        self.graphParameters.append(timeFrames)  
        print("from view")
        print(self.graphParameters )    
        return HttpResponse(self.graphParameters)
def getPrice(requiest):
    price = []
    now = datetime.now()
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    timezone = pytz.timezone("Asia/Damascus")
    utc_from = datetime(now.year,  now.month, now.day,now.hour,now.minute ,  tzinfo=timezone)
    utc_to = datetime(now.year, now.month, now.day+2,now.hour,now.minute, tzinfo=timezone)
    EURUSD_Ticks = mt5.copy_ticks_range("EURUSD", utc_from, utc_to, mt5.COPY_TICKS_ALL)
    EURUSD_Ticks_Frame = pd.DataFrame(EURUSD_Ticks)
    EURUSD_Ticks_Frame['time']=pd.to_datetime(EURUSD_Ticks_Frame['time'], unit='s')
    price.append(EURUSD_Ticks_Frame.tail(1))
    eb = str(price[0]['bid'])
    eb1 = re.compile("\d+\.\d+")
    EURUSD_Bid = eb1.findall(eb)
    ea = str(price[0]['ask'])
    ea1 = re.compile("\d+\.\d+")
    EURUSD_Ask = ea1.findall(ea)


    USDCHF_Ticks = mt5.copy_ticks_range("USDCHF", utc_from, utc_to, mt5.COPY_TICKS_ALL)
    USDCHF_Ticks_Frame = pd.DataFrame(USDCHF_Ticks)
    USDCHF_Ticks_Frame['time']=pd.to_datetime(USDCHF_Ticks_Frame['time'], unit='s')
    price.append(USDCHF_Ticks_Frame.tail(1))
    cb = str(price[1]['bid'])
    cb1 = re.compile("\d+\.\d+")
    USDCHF_Bid = cb1.findall(cb)
    ca = str(price[1]['ask'])
    ca1 = re.compile("\d+\.\d+")
    USDCHF_Ask = ca1.findall(ca)


    GBPUSD_Ticks = mt5.copy_ticks_range("GBPUSD", utc_from, utc_to, mt5.COPY_TICKS_ALL)
    GBPUSD_Ticks_Frame = pd.DataFrame(GBPUSD_Ticks)
    GBPUSD_Ticks_Frame['time']=pd.to_datetime(GBPUSD_Ticks_Frame['time'], unit='s')
    price.append(GBPUSD_Ticks_Frame.tail(1))
    gb = str(price[2]['bid'])
    gb1 = re.compile("\d+\.\d+")
    GBPUSD_Bid = gb1.findall(gb)
    ga = str(price[2]['ask'])
    ga1 = re.compile("\d+\.\d+")
    GBPUSD_Ask = ga1.findall(ga)
    USDJPY_Ticks = mt5.copy_ticks_range("USDJPY", utc_from, utc_to, mt5.COPY_TICKS_ALL)
    USDJPY_Ticks_Frame = pd.DataFrame(USDJPY_Ticks)
    USDJPY_Ticks_Frame['time']=pd.to_datetime(USDJPY_Ticks_Frame['time'], unit='s')
    price.append(USDJPY_Ticks_Frame.tail(1))
    jb = str(price[3]['bid'])
    jb1 = re.compile("\d+\.\d+")
    USDJPY_Bid = jb1.findall(jb)
    ja = str(price[3]['ask'])
    ja1 = re.compile("\d+\.\d+")
    USDJPY_Ask = ja1.findall(ja)
    all_Prices = {'EURUSD_Bid' :EURUSD_Bid , 'EURUSD_Ask':EURUSD_Ask , 'USDCHF_Bid':USDCHF_Bid ,
    'USDCHF_Ask':USDCHF_Ask , 'GBPUSD_Bid' :GBPUSD_Bid , 'GBPUSD_Ask':GBPUSD_Ask ,'USDJPY_Ask':USDJPY_Ask,
    'USDJPY_Bid':USDJPY_Bid
    }
    data = {'all_Prices' :all_Prices}
    return JsonResponse(data)
class Forecasting(View):
    Forecasting_data =[]
    def get(self,requiest):
        
        now = datetime.now()
        Symbol = requiest.GET.get('Symbol', None)
        timeFrames = requiest.GET.get('timeFrames', None)
        predict= requiest.GET.get('predict', None)
        self.Forecasting_data.clear()
        if predict == 'predict':
            try:
                if (timeFrames=='5 Minute'):
                    timeFrame = mt5.TIMEFRAME_M5
                    get_date = now - timedelta(hours=4)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                # date_list = [now + timedelta(minutes=x) for x in range(20)]
                elif (timeFrames=='10 Minute'):
                    timeFrame = mt5.TIMEFRAME_M10
                    get_date = now - timedelta(hours=8)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                elif (timeFrames=='20 Minute'):
                    timeFrame = mt5.TIMEFRAME_M20  
                    get_date = now - timedelta(hours=16)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour      
                elif (timeFrames=='30 Minute'):
                    timeFrame = mt5.TIMEFRAME_M30
                    get_date = now - timedelta(hours=32)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour 
                elif (timeFrames=='1 Hour'):
                    timeFrame = mt5.TIMEFRAME_H1
                    get_date = now - timedelta(days=6)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                elif (timeFrames=='6 Hours'):
                    timeFrame = mt5.TIMEFRAME_H6
                    get_date = now - timedelta(days=20)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour    
                elif (timeFrames=='12 Hours'):
                    timeFrame = mt5.TIMEFRAME_H12
                    get_date = now - timedelta(days=35)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                elif (timeFrames=='1 Day'):
                    timeFrame = mt5.TIMEFRAME_D1
                    get_date = now - timedelta(days=75)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                elif (timeFrames=='1 Week'):
                    timeFrame = mt5.TIMEFRAME_W1
                    get_date = now - timedelta(weeks=75)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                elif (timeFrames=='1 Month'):
                    timeFrame = mt5.TIMEFRAME_MN1
                    print("1 Month here")
                    get_date = now - timedelta(weeks=250)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour
                else:
                    timeFrame = mt5.TIMEFRAME_M1
                    get_date = now +timedelta(hours=1)
                    year = get_date.year
                    month = get_date.month
                    day = get_date.day
                    hour = get_date.hour          
            except:
                Symbol ='EURUSD'
                timeFrame = mt5.TIMEFRAME_M1
                get_date = now + timedelta(hours=1)
                year = get_date.year
                month = get_date.month
                day = get_date.day
                hour = get_date.hour
            rates = mt5.copy_rates_range(Symbol, timeFrame, datetime(year,month,day,hour,now.minute), datetime(now.year,now.month,now.day+1,now.hour,now.minute)) 
            rates_frame = pd.DataFrame(rates)
            rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
            open_price1 =rates_frame['open']
            close_price1 =rates_frame['close']
            high_price1 =rates_frame['high']
            low_price1 =rates_frame['low']
            close_model = SARIMAX(close_price1 ,  order = (0, 1, 1),  
                                    seasonal_order =(2, 1, 1, 12))
            close_result = close_model.fit()
            close_forecast = close_result.predict(start = len(high_price1),  
                                    end = (len(high_price1)+20),  
                                    typ = 'levels')
            open_model = SARIMAX(open_price1 ,  order = (0, 1, 1),  
                                        seasonal_order =(2, 1, 1, 12))
            open_result = open_model.fit()
            open_forecast = open_result.predict(start = len(high_price1),  
                                        end = (len(high_price1)+20),  
                                        typ = 'levels')
            high_model = SARIMAX(high_price1 ,  order = (0, 1, 1),  
                                        seasonal_order =(2, 1, 1, 12))
            high_result = high_model.fit()
            high_forecast = high_result.predict(start = len(high_price1),  
                                        end = (len(high_price1)+20),  
                                        typ = 'levels')
            low_model = SARIMAX(low_price1 ,  order = (0, 1, 1),  
                                        seasonal_order =(2, 1, 1, 12))
            low_result = low_model.fit()
            low_forecast = low_result.predict(start = len(high_price1),  
                                        end = (len(high_price1)+20),  
                                        typ = 'levels')
            self.Forecasting_data.append(open_forecast)
            self.Forecasting_data.append(close_forecast)
            self.Forecasting_data.append(high_forecast)
            self.Forecasting_data.append(low_forecast)
        else:
            
            self.Forecasting_data.append('h')
        return HttpResponse(self.Forecasting_data)
def newOrder(requiest):
    take_profit = requiest.GET.get('take_profit', None)
    stop_loss = requiest.GET.get('stop_loss', None)
    Deviation = requiest.GET.get('Deviation', None)
    Volume = requiest.GET.get('Volume', None)
    symbols = requiest.GET.get('symbols', None)
    order_type = requiest.GET.get('type', None)
    print(order_type)
    if order_type == 'sell':
        price = mt5.symbol_info_tick(symbols).bid
        orederType =mt5.ORDER_TYPE_SELL
    else:
        price = mt5.symbol_info_tick(symbols).ask
        orederType =mt5.ORDER_TYPE_BUY       


    take_profit = float(take_profit)
    stop_loss= float(stop_loss)
    Volume = float(Volume)
    Deviation = int(Deviation)
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    symbol = "EURUSD"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbols,
        "volume": Volume,
        "type": orederType,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": Deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with Deviation={} points".format(symbol,lot,price,Deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
   
    mt5.shutdown()
    return HttpResponse (True)

def Login(requiest):
    username = requiest.GET.get('username', None)
    password = requiest.GET.get('password', None)
    try:
        mt5.initialize()
        authorized=mt5.login(username)      
        account_info=mt5.account_info()
        account_info_dict = mt5.account_info()._asdict()
        UserName = account_info_dict['name']
        Balance = account_info_dict['balance']
        account = {'UserName':UserName, 'Balance':Balance}
        data = {'account':account}
    except:
        data = 'not found'
    return JsonResponse(data)
def autoTrade(requiest):
    take_profit = requiest.GET.get('auto_take_profit', None)
    stop_loss = requiest.GET.get('auto_stop_loss', None)
    Deviation = requiest.GET.get('auto_Deviation', None)
    Volume = requiest.GET.get('auto_Volume', None)
    symbols = requiest.GET.get('auto_symbols', None)
    take_profit = float(take_profit)
    stop_loss= float(stop_loss)
    Volume = float(Volume)
    Deviation = int(Deviation)
    while (True):
        now = datetime.now()
        get_date = now - timedelta(hours=32)
        year = get_date.year
        month = get_date.month
        day = get_date.day
        hour = get_date.hour 
        rates = mt5.copy_rates_range(symbols, mt5.TIMEFRAME_M30, datetime(year,month,day,hour,now.minute), datetime(now.year,now.month,now.day+1,now.hour,now.minute)) 
        rates_frame = pd.DataFrame(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        open_price1 =rates_frame['open']
        close_price1 =rates_frame['close']
        high_price1 =rates_frame['high']
        low_price1 =rates_frame['low']
        close_model = SARIMAX(close_price1 ,  order = (0, 1, 1),  
                        seasonal_order =(2, 1, 1, 12))
        close_result = close_model.fit()
        close_forecast = close_result.predict(start = len(high_price1),  
                        end = (len(high_price1)),  
                        typ = 'levels')
        open_model = SARIMAX(open_price1 ,  order = (0, 1, 1),  
                        seasonal_order =(2, 1, 1, 12))
        open_result = open_model.fit()
        open_forecast = open_result.predict(start = len(high_price1),  
                        end = (len(high_price1)),  
                        typ = 'levels')

        hello = 'h'
        data = {'close_forecast':close_forecast}
        p = open_forecast -close_forecast
        p = str(p)
        p1 = re.findall("\d+\.\d+", p)
        p1 = p[0]
        Symbol_Price = float(p1)  
        if Symbol_Price > 0.0:
            price = mt5.symbol_info_tick(symbols).ask
            orederType =mt5.ORDER_TYPE_BUY
            stopLoss = price - stop_loss
            takeProfit = price + take_profit
        else:
  
            price = mt5.symbol_info_tick(symbols).bid
            orederType =mt5.ORDER_TYPE_SELL
            stop_loss = price + stop_loss
            take_profit = price - take_profit
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbols,
            "volume": Volume,
            "type": orederType,
            "price": price,
            "sl": stopLoss,
            "tp": takeProfit,
            "deviation": Deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }    
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            result_dict=result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field,result_dict[field]))
                if field=="request":
                    traderequest_dict=result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        time.sleep(280)
    mt5.shutdown()
    return HttpResponse(data)

def getNews(requiest):
    url = 'https://www.forexfactory.com/calendar.php?day=today'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    table = page_soup.find_all("tr",{"class":"calendar_row"})
    forcal = []
    for item in table:
        dict = {}
        dict["Currency"] = item.find_all("td", {"class":"calendar__currency"})[0].text #Currency
        dict["Event"] = item.find_all("td",{"class":"calendar__event"})[0].text.strip() #Event Name
        dict["Time_Eastern"] = item.find_all("td", {"class":"calendar__time"})[0].text #Time Eastern
        impact = item.find_all("td", {"class":"impact"})
        for icon in range(0,len(impact)):
            dict["Impact"] = impact[icon].find_all("span")[0]['title'].split(' ', 1)[0]
        dict["Actual"] = item.find_all("td", {"class":"calendar__actual"})[0].text #Actual Value
        dict["Forecast"] = item.find_all("td", {"class":"calendar__forecast"})[0].text #forecasted Value
        dict["Previous"] = item.find_all("td", {"class":"calendar__previous"})[0].text # Previous
        forcal.append(dict)
    df = pd.DataFrame(forcal)
    Currency =[]
    Event=[]
    Time_Eastern =[]
    Actual=[]
    Forecast=[]
    Previous=[]
    Impact=[]
    df["Currency"]
    for i in df["Currency"]:
        a_string = i.rstrip("\n")
        Currency.append(a_string[1:])
    for i in df["Event"]:
        Event.append(i)
    for i in df["Time_Eastern"]:
        Time_Eastern.append(i)
    for i in df["Actual"]:
        Actual.append(i)
    for i in df["Forecast"]:
        Forecast.append(i)
    for i in df["Previous"]:
        Previous.append(i)
    for i in df["Impact"]:
        Impact.append(i)
    News = {'Currency':Currency ,'Event':Event , 'Impact':Impact , 'Time_Eastern':Time_Eastern , 'Actual':Actual ,
    'Forecast':Forecast , 'Previous':Previous}
    data = {'News' : News}
    return JsonResponse(data)

