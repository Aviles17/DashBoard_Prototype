import pandas as pd
import requests
from datetime import datetime
import time
import pandas_ta as ta
import pytz
import numpy as np
from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

global client, api_key, api_secret
load_dotenv()
Api_key = os.getenv("API_KEY")
Api_secret = os.getenv("API_SECRET")
client = HTTP(testnet=False, api_key=Api_key, api_secret=Api_secret)
'''
###################################################################################
[Proposito]: Funcion para limpiar la entrada de la informacion del cliente y proveer la informacion de cuenta
[Parametros]: symbol(Stock por la cual se quiere filtrar, Ejemplo : USDT), cliente (Informacion del cliente de bybit)
[Retorna]: Retorna valor 'float' del balance de la moneda asignada por parametro en la cuenta
###################################################################################
'''


def Get_Balance(symbol: str):
    filt_Balance = 0
    while(filt_Balance == 0):
        balance = client.get_coin_balance(accountType="UNIFIED", coin=symbol)
        if balance is not None:
            filt_Balance = balance["result"]["balance"]["walletBalance"]
        else:
            filt_Balance = 0

    return filt_Balance


'''
###################################################################################
[Proposito]: Funcion para obtener informacion cada minuto de una moneda en especifico
[Parametros]: symbol (Simbolo de la moneda que se quiere analizar, Ejemplo : BTCUSDT),
              interval (String que representa el intervalo en el que se van a trabajar los datos, Ejemplo: '15' para 15 minutos)
[Retorno]: Dataframe de pandas con la informacion solicitada
###################################################################################
'''


def get_data(symbol: str, interval: str):
    list_registers = []
    unix_endtime = None
    for i in range(0, 3):
        if i == 0:  # Primer llamado: Historial de mercado con tiempo actual
            url = 'http://api.bybit.com/v5/market/kline?symbol=' + \
                symbol+'&interval='+interval+'&limit='+str(1000)
            while (True):
                try:
                    data = requests.get(url).json()
                    unix_endtime = data['result']["list"][-1][0]
                    break
                except requests.exceptions.ConnectionError as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
                except requests.RequestException as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
                except Exception as e:
                    print(
                        f"An error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
        if i == 1 and unix_endtime != None:
            url = 'http://api.bybit.com/v5/market/kline?symbol='+symbol + \
                '&interval='+interval+'&limit=' + \
                str(1000)+'&end='+str(unix_endtime)
            while (True):
                try:
                    data = requests.get(url).json()
                    unix_endtime = data['result']["list"][-1][0]
                    break
                except requests.exceptions.ConnectionError as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
                except requests.RequestException as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
        if i == 2 and unix_endtime != None:
            url = 'http://api.bybit.com/v5/market/kline?symbol='+symbol + \
                '&interval='+interval+'&limit=' + \
                str(200)+'&end='+str(unix_endtime)
            while (True):
                try:
                    data = requests.get(url).json()
                    break
                except requests.exceptions.ConnectionError as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
                except requests.RequestException as e:
                    print(
                        f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
                    time.sleep(10)
        # Crear proto dataframe y añadir a lista
        df = pd.DataFrame(data['result']["list"], columns=[
                          'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover'])
        df['Time'] = pd.to_numeric(df['Time'])
        df = df.drop_duplicates()
        df['Time'] = df['Time'].apply(
            lambda x: datetime.fromtimestamp(x / 1000, tz=pytz.UTC))
        target_timezone = pytz.timezone('Etc/GMT+5')
        df['Time'] = df['Time'].apply(lambda x: x.astimezone(target_timezone))
        df = df.drop(columns=['Turnover'])
        list_registers.append(df)

    concatenated_df = pd.concat(
        [list_registers[0], list_registers[1], list_registers[2]], axis=0)
    concatenated_df = concatenated_df.reset_index(drop=True)
    float_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    concatenated_df[float_columns] = concatenated_df[float_columns].astype(
        float)
    concatenated_df = concatenated_df.drop_duplicates()
    return concatenated_df


"""
###################################################################################
"""

"""
###################################################################################
[Proposito]: Funcion auxiliar para calcular el Simple Moving Average (SMA) de una serie de datos
[Parametros]: source (lista o serie que representa los datos de entrada),
              length (La ventana de tiempo del SMA a calcular),
              rounded (Numero de decimales para redondear el resultado, por defecto 5)
[Retorno]: Retorna el valor SMA calculado como un float
###################################################################################
"""


def ta_sma(source, length, rounded=7) -> float:

    sum_length = sum(source)
    SMA = round(sum_length/length, rounded)

    return SMA


"""
###################################################################################
[Proposito]: Funcion para calcular el Exponential Moving Average (EMA) de una serie Pandas
[Parametros]: source (pandas.Series que representa el precio de cierre o con lo que se calculara el EMA),
              length (La ventana de tiempo del EMA a calcular),
              rounded (Numero de decimales para redondear los resultados, por defecto 5)
[Retorno]: Retorna una lista con el EMA calculado
###################################################################################
"""


def ta_ema(source: pd.Series, length: int, rounded=7, ):

    alpha = 2 / (length + 1)

    SMA = []
    EMA = []

    aux = 0
    prev_ema = 0

    for close_price in source:

        aux = aux + 1

        if (aux < length):
            SMA.append(close_price)
            EMA.append(None)
            continue

        elif (aux == length):
            prev_ema = ta_sma(SMA, length)
            EMA.append(prev_ema)
            continue

        elif (aux > length):
            close_price = round(close_price, rounded)
            prev_ema = round(
                (alpha * close_price + (1 - alpha) * prev_ema), rounded)
            EMA.append(prev_ema)

    return EMA


"""
###################################################################################
[Proposito]: Funcion para calcular un segundo EMA basado en los resultados del primer EMA
[Parametros]: source (lista o serie que representa los valores del primer EMA),
              length (La ventana de tiempo del segundo EMA a calcular),
              rounded (Numero de decimales para redondear los resultados, por defecto 5)
[Retorno]: Retorna una lista con el segundo EMA calculado
###################################################################################
"""


def ta_second_ema(source, length, rounded=7):

    alpha = 2 / (length + 1)

    SMA = []
    EMA2 = []

    aux = 0
    prev_ema2 = 0

    for ema_value in source:

        if (ema_value == None):
            EMA2.append(None)
            continue

        elif (ema_value != None):

            aux = aux + 1

            if (aux < length):
                SMA.append(ema_value)
                EMA2.append(None)
                continue

            elif (aux == length):
                prev_ema2 = ta_sma(SMA, length)
                EMA2.append(prev_ema2)
                continue

            elif (aux > length):
                prev_ema2 = round(
                    (alpha * ema_value + (1 - alpha) * prev_ema2), rounded)
                EMA2.append(prev_ema2)

    return EMA2


"""
###################################################################################
[Proposito]: Funcion para calcular el Double Exponential Moving Average (DEMA) de una serie de datos
[Parametros]: df (pandas.DataFrame que contiene los datos de precio),
              length (La ventana de tiempo del DEMA a calcular, por defecto 800),
              rounded (Numero de decimales para redondear los resultados, por defecto 5)
[Retorno]: Retorna una lista con el DEMA calculado
###################################################################################
"""


def dema(df: pd.DataFrame, length: int = 800, rounded=7):

    src = df['Close']

    e1 = ta_ema(src, length)
    e2 = ta_second_ema(e1, length)

    dema = []

    for a, b in zip(e1, e2):

        if a is None or b is None:
            dema.append(None)

        else:
            result = round(2 * a - b, rounded)
            dema.append(result)

    return dema


'''
###################################################################################
[Proposito]: Funcion para calcular las lineas que representan el SuperTrend superior e inferior, sus etiquetas e indicadores correspondientes
[Parametros]: df (Dataframe con la informacion del activo)
[Retorno]: Retorna el dataframe modificado, con columnas de 'Supertrend' añadidas 
###################################################################################
'''


def CalculateSupertrend(data: pd.DataFrame, mult: int):

    reversed_df = data.iloc[::-1]
    Temp_Trend = ta.supertrend(
        high=reversed_df['High'],
        low=reversed_df['Low'],
        close=reversed_df['Close'],
        period=10,
        multiplier=mult)
    
    ATR = ta.atr(high=reversed_df['High'], low=reversed_df['Low'], close=reversed_df['Close'], length=14)

    Temp_Trend = Temp_Trend.rename(columns={f'SUPERT_7_{mult}.0': 'Supertrend', f'SUPERTd_7_{mult}.0': 'Polaridad',
                                   f'SUPERTl_7_{mult}.0': 'ST_Inferior', f'SUPERTs_7_{mult}.0': 'ST_Superior'})

    df_merge = pd.merge(data, Temp_Trend, left_index=True, right_index=True)
    df_merge = pd.merge(df_merge, ATR, left_index=True, right_index=True)

    df_merge_ma_final = update_df(df_merge) # Actualizar el dataframe con las medias moviles (EMA , DEMA)
    return df_merge_ma_final


"""
###################################################################################
[Proposito]: Funcion para actualizar un DataFrame con calculos de EMA y DEMA
[Parametros]: data (pandas.DataFrame que contiene los datos de precio),
              test_length (La ventana de tiempo para los calculos de EMA y DEMA, por defecto 800)
[Retorno]: Retorna un DataFrame actualizado con columnas adicionales para EMA y DEMA
###################################################################################
"""


def update_df(data: pd.DataFrame, test_length: int = 800):

    kline = data.iloc[::-1].reset_index(drop=True)

    _ema = ta_ema(kline['Close'], test_length)
    _dema = dema(kline, test_length)

    kline["EMA"] = _ema
    kline["DEMA800"] = _dema

    FULL_original_order_klin = kline.iloc[::-1].reset_index(drop=True)

    return FULL_original_order_klin


def get_order_info(symb: str):
    try:
        positions = client.get_positions(category='linear', symbol=symb)
        data = positions["result"]["list"]
        for item in data:
            if item["size"] != '0':
                return item
    except Exception as e:
        print(
            f"An exception occurred connecting to Bybit 'get_positions' endpoint: {e}")
    return {}


def get_position(side: str, symbol: str, df: pd.DataFrame):
    symbol_res = get_order_info(symbol)
    if len(symbol_res) != 0:
        position = None
        if side == symbol_res["side"] and symbol_res["size"] != 0:
            size = float(symbol_res["size"])
            entry = float(symbol_res["avgPrice"])
            stoploss = float(symbol_res["stopLoss"])
            goal_price = (2*entry) - stoploss
            return size, str(entry), str(stoploss), goal_price
        else:
            return 0, 0, 0, 0
    else:
        return 0, 0, 0, 0

def get_position_history(defined_interval: str = "m"): # 'm' for montly, 'a' for all time
  timezone = pytz.timezone("Etc/GMT+5")
  date_origin = datetime(2024,10,27,0,0,0, tzinfo=timezone) # Octubre 23 del 2024
  utc_date_origin = date_origin.astimezone(pytz.utc)
  ms_date_origin = int(utc_date_origin.timestamp()*1000)
  # Convert both to Unix time
  if defined_interval == "m":
    start_time = int(time.time() *1000) - (31 * 24 * 60 * 60 * 1000)
  else:
    start_time = int(time.time() *1000) - (365 * 24 * 60 * 60 * 1000)
  if start_time < ms_date_origin:
    start_time = ms_date_origin

    concat_list = []
    # Get the first hsitory of 7 days
    res = client.get_closed_pnl(category="linear", limit=100)
    concat_list.extend(res["result"]["list"])
    endtime = int(res["result"]["list"][-1]["createdTime"])
    try:
        while start_time <= endtime:
            res = client.get_closed_pnl(category="linear",endTime = endtime, limit=100)
            if len(res["result"]["list"]) != 0:
              endtime = int(res["result"]["list"][-1]["createdTime"])
              concat_list.extend(res["result"]["list"])
            else:
              break
        return concat_list
    except Exception as e:
        print(
            f"An exception occurred connecting to Bybit 'get_closed_pnl' endpoint: {e}")
        return []


def get_kpi_history(supported_coins: list):
    history = get_position_history()
    if len(history) != 0:
        proto_dataframe = []
        for register in history:
            register_list = []
            register_list.append(register["createdTime"])
            register_list.append(float(register["closedPnl"]))
            register_list.append(register["symbol"])
            proto_dataframe.append(register_list)

        df = pd.DataFrame(proto_dataframe, columns=[
                          'Time', 'Profit', 'Symbol'])
        df = df.sort_values(by='Time')
        df['Time'] = pd.to_datetime(pd.to_numeric(df['Time']), unit='ms')
        df['Time'] = df['Time'].dt.strftime('%m/%d/%H:%S')
        coin_cumulative = get_cumulative(df, supported_coins)
        return df, df['Profit'].sum(), df['Profit'].mean(), coin_cumulative


def get_cumulative(df: pd.DataFrame, supported_coins: list) -> dict:
    cumulative_sum = df.groupby("Symbol")["Profit"].sum()
    return cumulative_sum.to_dict()
