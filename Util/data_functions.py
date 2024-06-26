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
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)
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
        balance = client.get_coin_balance(accountType="CONTRACT", coin=symbol)
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
def get_data(symbol: str,interval: str,unixtimeinterval: int = 1800000):
  list_registers = []
  DATA_200 = 180000
  now = datetime.now()
  unixtime = int(time.mktime(now.timetuple()))
  since = unixtime
  while(unixtimeinterval != 0):
    start= str(since - unixtimeinterval)
    url = 'http://api.bybit.com/v5/market/kline?symbol='+symbol+'&interval='+interval+'&from='+str(start)
    while(True):
      try:
        data = requests.get(url).json()
        break
      except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
        time.sleep(10)
      except requests.RequestException as e:
        print(f"Connection error occurred: {e}, Retrying in 10 seconds...\n")
        time.sleep(10)
    df = pd.DataFrame(data['result']["list"], columns=['Time','Open','High','Low','Close','Volume', 'Turnover'])
    df['Time'] = pd.to_numeric(df['Time'])
    df = df.drop_duplicates()
    df['Time'] = df['Time'].apply(lambda x: datetime.fromtimestamp(x / 1000, tz=pytz.UTC))
    target_timezone = pytz.timezone('Etc/GMT+5')
    df['Time'] = df['Time'].apply(lambda x: x.astimezone(target_timezone))
    #df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume','open_time':'Time'}, inplace=True)
    df = df.drop(columns=['Turnover'])
    list_registers.append(df)
    unixtimeinterval = unixtimeinterval - DATA_200
    
  concatenated_df = pd.concat([list_registers[0], list_registers[1], list_registers[2], list_registers[3], list_registers[4], list_registers[5], list_registers[6], list_registers[7], list_registers[8], list_registers[9]], axis=0)
  concatenated_df = concatenated_df.reset_index(drop=True)
  float_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
  concatenated_df[float_columns] = concatenated_df[float_columns].astype(float)
  return concatenated_df

'''
###################################################################################
[Proposito]: Funcion para calcular las lineas que representan el SuperTrend superior e inferior, sus etiquetas e indicadores correspondientes
[Parametros]: symbol (String que representa la moneda a la que se va a suscribir), 
              df (Dataframe con la informacion del activo), 
              mult (Multiplicador para calcular SuperTrend)
[Retorno]: Retorna el dataframe modificado, con columnas añadidas 
###################################################################################
'''
def CalculateSupertrend(data: pd.DataFrame):
  reversed_df = data.iloc[::-1]
  Temp_Trend = ta.supertrend(
    high= reversed_df['High'], 
    low = reversed_df['Low'], 
    close = reversed_df['Close'], 
    period=10, 
    multiplier=3)
  # Calcular DEMA800
  ema1 = ema(reversed_df['Close'], length=800)
  ema2 = ema(ema1, length=800)
  Temp_Trend['DEMA800'] = 2 * ema2 - ema1 
  Temp_Trend = Temp_Trend.rename(columns={'SUPERT_7_3.0':'Supertrend','SUPERTd_7_3.0':'Polaridad','SUPERTl_7_3.0':'ST_Inferior','SUPERTs_7_3.0':'ST_Superior'})
  df_merge = pd.merge(data,Temp_Trend,left_index=True, right_index=True)
  return df_merge


'''
###################################################################################
[Proposito]: Funcion auxiliar para calcular el Exponential Moving Average (EMA) de una serie Pandas
[Parametros]: source (pandas.Series que representa el precio de cierre o con lo que se calculara el EMA), 
              length (La ventana de tiempo del EMA a calcular), 
[Retorno]: Retorna serie de pandas con el EMA calculado
###################################################################################
'''
def ema(source, length):     

  #Calcular factor de suavisado (alpha)
  alpha = 2 / (length + 1)
  #Inicializar el EMA con el primer valor de la fuente
  ema = source.iloc[0]      
  #Calcular EMA para cada valor en la fuente
  ema_values = []    
  for i,value in enumerate(source):         
    ema = alpha * value + (1 - alpha) * ema         
    ema_values.append(ema)
  ema_values = ema_values
  # Convertir lista a serie de pandas 
  ema_series = pd.Series(ema_values)          
  return ema_series


def get_clean_data(df: pd.DataFrame):
    #Limpiar el dataframe
    if df['DEMA800'].isnull().values.any():
        df.dropna(subset=['DEMA800'], inplace=True)
    return df.head(200)

def get_order_info(symb: str):
  try:
    positions = client.get_positions(category='linear',symbol= symb)
    data = positions["result"]["list"]
    for item in data:
        if item["size"] != '0':
          return item
  except Exception as e:
    print(f"An exception occurred connecting to Bybit 'get_positions' endpoint: {e}")
  return {}
    

def get_position(side: str, symbol: str, df: pd.DataFrame):
    symbol_res = get_order_info(symbol)
    if len(symbol_res) != 0:
        position = None
        if side == symbol_res["side"] and symbol_res["size"] != 0:
            size =  float(symbol_res["size"])
            entry =  float(symbol_res["avgPrice"])
            stoploss = float(symbol_res["stopLoss"])
            leverage = float(symbol_res["leverage"])
            if(side == 'Sell'):
                quote_currency = (df['Close'].iloc[-1] - entry)*size*leverage
                notial = entry*size*leverage
                pyl = (quote_currency/notial)*-100
            else:
                quote_currency = (df['Close'].iloc[-1] - entry)*size*leverage
                notial = entry*size*leverage
                pyl = (quote_currency/notial)*100
            return size, str(entry), str(stoploss), pyl
        else:
            return 0, 0, 0, 0
    else:
        return 0, 0, 0, 0
  
def get_position_history():
  start_test_unix = 1710172106699 + 764000000 # 2024-03-21 10:00:30
  endtime = int(datetime.now().timestamp() * 1000)
  avg_seven = 604800 * 1000
  concat_list = []
  try:
      for i in range(5):
        res = client.get_closed_pnl(category="linear", endTime = endtime, limit=100)
        endtime -= avg_seven
        concat_list.extend(res["result"]["list"])

      unique_list = [dict(t) for t in {tuple(sorted(d.items())) for d in concat_list}]
      filtered_list = []
      for item in unique_list:
        if int(item["createdTime"]) >= start_test_unix:
          filtered_list.append(item)
          
      return filtered_list
      
  except Exception as e:
      print(f"An exception occurred connecting to Bybit 'get_closed_pnl' endpoint: {e}")
      return []
      
      
def get_history():
  history = get_position_history()
  if len(history) != 0:
    proto_dataframe = []
    for register in history:
      register_list = []
      register_list.append(register["createdTime"])
      register_list.append(float(register["closedPnl"]))
      if register["side"] == "Buy":
        quote_currency = (float(register["avgExitPrice"]) - float(register["avgEntryPrice"]))*float(register["closedSize"])*float(register["leverage"])
        notional = float(register["avgEntryPrice"])*float(register["closedSize"])*float(register["leverage"])
        pyl = (quote_currency/notional)*-100
      else:
        quote_currency = (float(register["avgExitPrice"]) - float(register["avgEntryPrice"]))*float(register["closedSize"])*float(register["leverage"])
        notional = float(register["avgEntryPrice"])*float(register["closedSize"])*float(register["leverage"])
        pyl = (quote_currency/notional)*100
        
      register_list.append(pyl)
      proto_dataframe.append(register_list)
      
    df = pd.DataFrame(proto_dataframe, columns=['Time','Profit','P&L'])
    df = df.sort_values(by='Time')
    df['P&L'] *= 100
    df['Time'] = pd.to_datetime(pd.to_numeric(df['Time']), unit='ms')
    df['Time'] = df['Time'].dt.strftime('%m/%d/%H:%S')
    prop_positives, prop_negatives, prop_count_positives, prop_count_negatives = sum_and_count_positives_negatives(df, 'Profit')
    df.to_csv('History.csv')
    return df, df['Profit'].sum(), df['P&L'].mean(), prop_positives, prop_negatives, prop_count_positives, prop_count_negatives
      

def sum_and_count_positives_negatives(df: pd.DataFrame, column_name: str):
  # Filtrar los valores positivos y negativos
  positives = df[df[column_name] > 0][column_name]
  negatives = df[df[column_name] < 0][column_name]
  
  sum_positives = positives.sum()
  sum_negatives = negatives.sum()
  count_positives = positives.count()
  count_negatives = negatives.count()
  prop_positives = sum_positives / (sum_positives + abs(sum_negatives))
  prop_negatives = abs(sum_negatives) / (sum_positives + abs(sum_negatives))
  prop_count_positives = count_positives / (count_positives + count_negatives)
  prop_count_negatives = count_negatives / (count_positives + count_negatives)
  return prop_positives, prop_negatives, prop_count_positives, prop_count_negatives