import dash 
import json
from dash.dependencies import Output, Input
import dash_core_components as dcc 
import pandas as pd
import mplfinance as mpf
import MetaTrader5 as mt5
import dash_html_components as html 
import plotly 
import plotly.graph_objs as go 
from django_plotly_dash import DjangoDash
from datetime import datetime ,timedelta
from . import views
from calendar import monthrange
from statsmodels.tsa.statespace.sarimax import SARIMAX 
mt5.initialize()

now = datetime.now()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
  
app.layout = html.Div( 
    [   
        dcc.Graph(id = 'live-graph', animate = True), 
        dcc.Interval( 
            id = 'graph-update', 
            interval = 1000, 
            n_intervals = 0,
           
        ), 
        
    ] 
) 
@app.callback( 
    Output('live-graph', 'figure'), 
    [ Input('graph-update', 'n_intervals') ] 
) 
def update_graph_scatter(n):
    try:
        req = (views.allData.graphParameters)

        symbol = req[0]
        if (req[1]=='5 Minute'):
            timeFrame = mt5.TIMEFRAME_M5
            get_date = now - timedelta(hours=4)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(minutes=x+5) for x in range(0,100,5)]
        elif (req[1]=='10 Minute'):
            timeFrame = mt5.TIMEFRAME_M10
            get_date = now - timedelta(hours=8)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(minutes=x+10) for x in range(0,200,10)]
        elif (req[1]=='20 Minute'):
            timeFrame = mt5.TIMEFRAME_M20  
            get_date = now - timedelta(hours=16)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour   
            date_list = [now + timedelta(minutes=x+20) for x in range(0,400,20)]   
        elif (req[1]=='30 Minute'):
            timeFrame = mt5.TIMEFRAME_M30
            get_date = now - timedelta(hours=32)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour 
            date_list = [now + timedelta(minutes=x+30) for x in range(0,600,30)]
        elif (req[1]=='1 Hour'):
            timeFrame = mt5.TIMEFRAME_H1
            get_date = now - timedelta(days=6)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(hours=x) for x in range(22)]
        elif (req[1]=='6 Hours'):
            timeFrame = mt5.TIMEFRAME_H6
            get_date = now - timedelta(days=20)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour  
            date_list = [now + timedelta(hours=x+6) for x in range(0,135,6)]  
        elif (req[1]=='12 Hours'):
            timeFrame = mt5.TIMEFRAME_H12
            get_date = now - timedelta(days=35)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(hours=x+12) for x in range(0,275,12)] 
        elif (req[1]=='1 Day'):
            timeFrame = mt5.TIMEFRAME_D1
            get_date = now - timedelta(days=75)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(days=x) for x in range(22)]
        elif (req[1]=='1 Week'):
            timeFrame = mt5.TIMEFRAME_W1
            get_date = now - timedelta(weeks=75)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(weeks=x) for x in range(22)]
        elif (req[1]=='1 Month'):
            timeFrame = mt5.TIMEFRAME_MN1
            get_date = now - timedelta(weeks=250)
            year = get_date.year
            month = get_date.month
            day = get_date.day
            hour = get_date.hour
            date_list = [now + timedelta(weeks=x+4) for x in range(0,44,4)]
        else:
            timeFrame = mt5.TIMEFRAME_M1
            get_date = now +timedelta(hours=1)
            year = get_date.year
            month = get_date.month

            day = get_date.day
            hour = get_date.hour 
            date_list = [now + timedelta(minutes=x) for x in range(22)]         
    except:
        symbol ='EURUSD'
        timeFrame = mt5.TIMEFRAME_M1
        get_date = now + timedelta(hours=1)
        year = get_date.year
        month = get_date.month
        day = get_date.day
        hour = get_date.hour
        
        date_list = [now + timedelta(minutes=x) for x in range(1,30)]
    rates = mt5.copy_rates_range(symbol, timeFrame, datetime(year,month,day,hour,now.minute+30), datetime(now.year,now.month,now.day+1,now.hour,now.minute)) 
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    open_price =rates_frame['open']
    close_price =rates_frame['close']
    high_price =rates_frame['high']
    low_price =rates_frame['low']
    time = rates_frame['time']
    req1 = (views.Forecasting.Forecasting_data)
    print(len(req1))
    try:

        data =[
        go.Candlestick(
            x = time ,
            low = low_price,
            high = high_price,
            close = close_price,
            open = open_price,
            increasing_line_color = 'black',
            decreasing_line_color = 'red' ),   
            go.Candlestick(
            x = date_list ,
            low = req1[3],
            high = req1[2],
            close = req1[1],
            open = req1[0],
            increasing_line_color = 'rgb(0,255,0)',
            decreasing_line_color = 'rgb(0,0,255)' ),  
            
        ]
        time1 = date_list
        if min(low_price)> min(req1[3]):
            min_data = min(req1[3])
        else:
            min_data = min(low_price)
        if max(high_price) > max(req1[2]):
            max_data = max(high_price)
        else:
            max_data = max(req1[2])
    except:
        data =[
        go.Candlestick(
            x = time ,
            low = low_price,
            high = high_price,
            close = close_price,
            open = open_price,
            increasing_line_color = 'black',
            decreasing_line_color = 'red' ),

        ]
        time1 = time
        min_data = min(low_price)
        max_data = max(high_price)
    return {'data': data, 'layout' : go.Layout(xaxis=dict(range=[min(time),max(time1)]),
                                                yaxis=dict(range=[min_data-0.0002,max_data + 0.0002]),) }
         
         
