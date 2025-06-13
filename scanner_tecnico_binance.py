import requests
import pandas as pd
import time

BASE_URL = "https://api.binance.com"
INTERVAL = "1h"
LIMIT = 100

def get_usdt_symbols():
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [s['symbol'] for s in data['symbols'] if 'USDT' in s['symbol'] and s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']
    return symbols

def get_klines(symbol, interval=INTERVAL, limit=LIMIT):
    url = f"{BASE_URL}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "trades", "taker_base_volume", "taker_quote_volume", "ignore"])
    df['close'] = df['close'].astype(float)
    return df

def calcular_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

def scanner_tecnico():
    resultados = []
    symbols = get_usdt_symbols()
    for symbol in symbols[:20]:
        try:
            df = get_klines(symbol)
            df['rsi'] = calcular_rsi(df)
            df['ema20'] = calcular_ema(df, 20)
            df['ema50'] = calcular_ema(df, 50)

            ultima_rsi = df['rsi'].iloc[-1]
            ultima_ema20 = df['ema20'].iloc[-1]
            ultima_ema50 = df['ema50'].iloc[-1]
            preco = df['close'].iloc[-1]

            if ultima_rsi < 30 and ultima_ema20 > ultima_ema50:
                resultados.append({
                    'symbol': symbol,
                    'price': preco,
                    'rsi': round(ultima_rsi, 2),
                    'ema20': round(ultima_ema20, 2),
                    'ema50': round(ultima_ema50, 2)
                })
        except Exception as e:
            print(f"Erro ao processar {symbol}: {e}")
        time.sleep(0.2)

    return pd.DataFrame(resultados)
