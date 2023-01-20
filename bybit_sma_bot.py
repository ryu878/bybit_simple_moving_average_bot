# Ryuryu's Bybit USDT Perpetual Futures Bot
# Simpe Moving Average Edition (Production Mode #6973)
# ----------------------------------------------------
# (c) 2023 Ryan Hayabusa 
# GitGub: https://github.com/ryu878
# Web: https://aadresearch.xyz
# Discord: ryuryu#4087
# ----------------------------------------------------

import os
import time
import sqlite3
import pandas as pd
from config import *
import datetime as dt
from datetime import datetime
from inspect import currentframe
from pybit import usdt_perpetual



terminal_title = 'Bybit USDT Perpetual Futures Bot'
# print(f'\33]0;{terminal_title}[]\a', end='', flush=True)
ver = '1.0'

client = usdt_perpetual.HTTP(endpoint=endpoint, api_key=api_key, api_secret=api_secret)
session_unauth = usdt_perpetual.HTTP(endpoint=endpoint)

def get_linenumber():
    cf = currentframe()
    global line_number
    line_number = cf.f_back.f_lineno


######################
# Asking for Variables
######################

print('')
print('',terminal_title,ver)
print(' ─────────────────────────────────────')

symbol = input(' What asset to Trade? ')
symbol = (symbol+'USDT').upper()

print(' Asset:',symbol)

print(' Data refresh interval: 1 3 5 15 30 60 120 240 360 720 "D" "M" "W"')
interval = input(' Choose your Timeframe: ')
if interval.isdigit():
    interval = int(interval)

ma_length = input(' MA Lenght: ')
ma_length = int(ma_length)

waittime = input(' Timeout (minutes): ')
waittime = int(waittime)
# waittime = 1

csize = input(' Lot size: ')
csize = int(csize)
# csize = 1


####################
#  Removing Settings
####################

try:
    os.remove('settings_futures.db')
    os.remove('settings_futures.db-journal')
except Exception as e:
    # get_linenumber()
    # print(line_number, 'exeception: {}'.format(e))
    pass


#########################
# Saving Veriables to SQL
#########################

conn = sqlite3.connect('settings_futures.db')
cursor = conn.cursor()
conn.execute("""
    CREATE TABLE IF NOT EXISTS settings (
            interval text UNIQUE PRIMARY KEY NOT NULL,
            ma_length int,
            waittime int,
            csize real
    )""")

sqlite_update = """
    INSERT OR REPLACE INTO settings (
            interval,
            ma_length,
            waittime,
            csize) 
    VALUES (?, ?, ?, ?)
    """
        
data_tuple = (interval,ma_length,waittime,csize)
cursor.execute(sqlite_update, data_tuple)
conn.commit()
conn.close()


######################
# Get Settings from DB
######################

def get_settings_from_database():
    conn = sqlite3.connect('settings_futures.db')
    cursor = conn.cursor()
    data =  cursor.execute(f'SELECT * FROM settings').fetchall()
                
    for settings in data:
        global interval_db, ma_length_db, waittime_db, csize_db
        interval_db = settings[0]
        ma_length_db = settings[1]
        waittime_db = settings[2]
        csize_db = settings[3]

    conn.commit()
    conn.close()


get_settings_from_database()


def datefromtimestamp(timestamp):
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:00')
    return date

def year_from_timestamp(timestamp):
    year = datetime.utcfromtimestamp(timestamp).strftime('%Y')
    return int(year)

def month_from_timestamp(timestamp):
    month = datetime.utcfromtimestamp(timestamp).strftime('%m')
    return int(month)

def day_from_timestamp(timestamp):
    day = datetime.utcfromtimestamp(timestamp).strftime('%d')
    return int(day)

def hour_from_timestamp(timestamp):
    hour = datetime.utcfromtimestamp(timestamp).strftime('%H')
    return int(hour)

def min_from_timestamp(timestamp):
    minute = datetime.utcfromtimestamp(timestamp).strftime('%M')
    return int(minute)

def sec_from_timestamp(timestamp):
    sec = datetime.utcfromtimestamp(timestamp).strftime('%S')
    return int(sec)

def get_orderbook_rest():
    orderbook = session_unauth.orderbook(symbol=symbol)
    df = pd.DataFrame(orderbook['result'])
    # print(df)
    global ask, bid
    ask = float(df['price'][25])
    bid = float(df['price'][0])
    # print(ask,bid)

try:
    get_orderbook_rest()
except Exception as e:
    get_linenumber()
    print(line_number, 'exeception: {}'.format(e))
    pass

print(' Ask:',ask)
print(' Bid:',bid)


def get_position_rest():
    positions = client.my_position(symbol=symbol)
    
    global sell_position_size
    global sell_position_prce
    global buy_position_size
    global buy_position_prce
    
    # print(positions)
   
    for position in positions['result']:
    
        if position['side'] == 'None':
            
            sell_position_size = 0
            sell_position_prce = 0
            buy_position_size = 0
            buy_position_prce = 0
        if position['side'] == 'Sell':
            sell_position_size = position['size']
            sell_position_prce = position['entry_price']
            buy_position_size = 0
            buy_position_prce = 0
        if position['side'] == 'Buy':
            sell_position_size = 0
            sell_position_prce = 0
            buy_position_size = position['size']
            buy_position_prce = position['entry_price']

get_position_rest()


while True:

    time_now = int(time.time())+10800
    print('         Time now:',time_now)
    print('     Date from ts:',datefromtimestamp(time_now))
        
    if interval == int(interval):
        # print('Integer')
        from_time = time_now - (interval * ma_length * 60)
        start_year = year_from_timestamp(from_time)
        start_month = month_from_timestamp(from_time)
        start_day = day_from_timestamp(from_time)
        start_hour = hour_from_timestamp(from_time)
        start_min = min_from_timestamp(from_time)
        start_sec = sec_from_timestamp(from_time)
    if interval == 'D':
        # print('Day')
        from_time = time_now - (1440 * ma_length * 60)
        start_year = year_from_timestamp(from_time)
        start_month = month_from_timestamp(from_time)
        start_day = day_from_timestamp(from_time)
        start_hour = hour_from_timestamp(from_time)
        start_min = min_from_timestamp(from_time)
        start_sec = sec_from_timestamp(from_time)
    if interval == 'W':
        # print('Week')
        from_time = time_now - (10080 * ma_length * 60)
        start_year = year_from_timestamp(from_time)
        start_month = month_from_timestamp(from_time)
        start_day = day_from_timestamp(from_time)
        start_hour = hour_from_timestamp(from_time)
        start_min = min_from_timestamp(from_time)
        start_sec = sec_from_timestamp(from_time)
    if interval == 'M':
        # print('Week')
        from_time = time_now - (43800 * ma_length * 60)
        start_year = year_from_timestamp(from_time)
        start_month = month_from_timestamp(from_time)
        start_day = day_from_timestamp(from_time)
        start_hour = hour_from_timestamp(from_time)
        start_min = min_from_timestamp(from_time)
        start_sec = sec_from_timestamp(from_time)


    print(' ─────────────────────────────────────')
    print('            Asset:',symbol)
    print('        Timeframe:',interval_db)
    print('        MA length:',ma_length_db)
    print('          Timeout:',waittime_db)
    print('         Lot size:',csize_db)
    print('        From Time:',from_time)
    # print('Human Start Time:',startTime)

    print('             Time:',start_year,start_month,start_day,start_hour,start_min)
    print('')
    print('         Time now:',time_now,datefromtimestamp(time_now))
    print('        From time:',from_time,datefromtimestamp(from_time))
    print('             Diff:',time_now - from_time,(time_now - from_time) / 60)


    def get_bybit_candles(symbol, interval, limit, startTime):

        startTime = str(int(startTime.timestamp()))
        data = session_unauth.query_kline(symbol=symbol,interval=interval,limit=limit,from_time=startTime)
        df = pd.DataFrame(data['result'])

        if df.empty == False:   
            df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time]
            df.index.name = 'DataTime' 
            return df
        else:
            return None

    df_list = []

    # Input data
    startTime = dt.datetime(start_year, start_month, start_day, start_hour, start_min)

    while True:
        new_df = get_bybit_candles(symbol=symbol, interval=interval, limit=200, startTime=startTime)
        time.sleep(0.1)

        if new_df is None:
            print('end')
            break
        df_list.append(new_df)

        startTime = max(new_df.index)

    df = pd.concat(df_list)
    df = df.drop(columns = ['turnover','volume'])

    print(df)

    get_settings_from_database()

    df['open_time'] = pd.to_datetime(df['open_time'], unit='s', origin='unix')
    print(df)
    df['sma'] = df['close']
    df['sma'] = pd.to_numeric(df['sma'], downcast='float')
    df['sma'] = df['sma'].mean()
    global sma
    sma = df['sma'].iloc[-1]

    print(sma)

    try:
        get_orderbook_rest()
    except Exception as e:
        get_linenumber()
        print(line_number, 'exeception: {}'.format(e))
        pass
    
    print(' ─────────────────────────────────────')
    print(' Ask:',ask,'Bid:',bid)
    print(' SMA:',sma)
    print(' ─────────────────────────────────────')

    
    try:
        get_position_rest()

    except Exception as e:
        get_linenumber()
        print(line_number, 'exeception: {}'.format(e))
        pass


    if buy_position_size == 0 and sell_position_size == 0:

        if ask > sma:
            print(' Ask > SMA')
            print(' To Buy',csize,'lots')

            try:
                market_buy = client.place_active_order(side='Buy',symbol=symbol,order_type='Market',qty=csize,time_in_force='GoodTillCancel',reduce_only=False,close_on_trigger=False)
                print(' Market Buy')
            except Exception as e:
                get_linenumber()
                print(line_number, 'exeception: {}'.format(e))
                pass
            
            time.sleep(0.01)

            print(' Waiting...',waittime,'mins')

        if bid < sma:
            print(' Bid < SMA')
            print(' To Sell',csize,'lots')

            try:
                market_sell = client.place_active_order(side='Sell',symbol=symbol,order_type='Market',qty=csize,time_in_force='GoodTillCancel',reduce_only=False,close_on_trigger=False)
                print(' Market Sell')
            except Exception as e:
                get_linenumber()
                print(line_number, 'exeception: {}'.format(e))
                pass
            
            time.sleep(0.01)

            print(' Waiting...',waittime,'mins')

    else:
        print(' Positions found:')
        print('             Buy:',buy_position_size,'@',buy_position_prce)
        print('            Sell:',sell_position_size,'@',sell_position_prce)


    if buy_position_size > 0 and ask > sma:
        print(' Buy position found. Ask > SMA. Waiting...')

    if sell_position_size > 0 and bid < sma:
        print(' Sell position found. Bid < SMA. Waiting...')

    
    if buy_position_size > 0 and bid < sma:
        print(' Buy position found, but Bid < SMA. Closing it and opening Sell.')

        try:
            market_sell = client.place_active_order(side='Sell',symbol=symbol,order_type='Market',qty=buy_position_size,time_in_force='GoodTillCancel',reduce_only=True,close_on_trigger=True)
        except Exception as e:
            get_linenumber()
            print(line_number, 'exeception: {}'.format(e))
            pass
        
        time.sleep(0.01)
        
        try:
            market_sell = client.place_active_order(side='Sell',symbol=symbol,order_type='Market',qty=csize,time_in_force='GoodTillCancel',reduce_only=False,close_on_trigger=False)
        except Exception as e:
            get_linenumber()
            print(line_number, 'exeception: {}'.format(e))
            pass
        
        time.sleep(0.01)

    if sell_position_size > 0 and ask > sma:
        print(' Sell position found, but Bid < SMA.  Closing it and opening Buy.')

        try:
            market_buy = client.place_active_order(side='Buy',symbol=symbol,order_type='Market',qty=sell_position_size,time_in_force='GoodTillCancel',reduce_only=True,close_on_trigger=True)
        except Exception as e:
            get_linenumber()
            print(line_number, 'exeception: {}'.format(e))
            pass
        
        time.sleep(0.01)

        try:
            market_buy = client.place_active_order(side='Buy',symbol=symbol,order_type='Market',qty=csize,time_in_force='GoodTillCancel',reduce_only=False,close_on_trigger=False)
        except Exception as e:
            get_linenumber()
            print(line_number, 'exeception: {}'.format(e))
            pass
        
        time.sleep(0.01)


    time.sleep(waittime*60)
