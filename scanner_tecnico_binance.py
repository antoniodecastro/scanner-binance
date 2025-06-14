import requests
import pandas as pd
import time

def get_usdt_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    data = requests.get(url, timeout=10).json()
    symbols = [s['symbol'] for s in data['symbols'] if 'USDT' in s.get('symbol', '') and s.get('quoteAsset') == 'USDT' and s.get('status') == 'TRADING']
    return symbols

def get_klines(symbol, interval, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "trades", "taker_base_volume", "taker_quote_volume", "ignore"])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
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

def calcular_macd(df):
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

def scanner_tecnico(intervalo="1d"):
    resultados = []
    symbols = get_usdt_symbols()
    for symbol in symbols:
        try:
            df = get_klines(symbol, interval=intervalo)
            rsi = calcular_rsi(df)
            ema20 = calcular_ema(df, 20)
            ema50 = calcular_ema(df, 50)
            macd_line, signal_line = calcular_macd(df)

            preco = df['close'].iloc[-1]
            rsi_val = rsi.iloc[-1]
            ema20_val = ema20.iloc[-1]
            ema50_val = ema50.iloc[-1]
            macd_cross = (macd_line.iloc[-2] < signal_line.iloc[-2]) and (macd_line.iloc[-1] > signal_line.iloc[-1])

            if rsi_val < 40 and ema20_val > ema50_val and preco > ema20_val and macd_cross:
                resultados.append({
                    'symbol': symbol,
                    'Preço': round(preco, 4),
                    'RSI': round(rsi_val, 2),
                    'EMA20': round(ema20_val, 2),
                    'EMA50': round(ema50_val, 2),
                    'MACD Cross': macd_cross,
                    'Timeframe': intervalo,
                    'Sinal': "✅ Entrada potencial"
                })
        except Exception as e:
            print(f"Erro em {symbol}: {e}")
        time.sleep(0.3)
    return pd.DataFrame(resultados)