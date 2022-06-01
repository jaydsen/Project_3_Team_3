# Load imports and libraries
from distutils.log import info
from requests import Request, Session
import json
import time
import webbrowser
import pprint
import os
from dotenv import load_dotenv
import pandas as pd
import questionary
import smtplib
from utils import send

crypto = questionary.select(
    'Select the cryptocurrency you want to keep track of',
    choices=['bitcoin','ethereum','ripple','dogecoin']
).ask()

converted = questionary.select(
    'Select the converted currency you wish to display data in',
    choices=['USD','CAD','EUR','GBP']
).ask()

load_dotenv()
coin_mkt_api_key = os.getenv('COIN_MKT_API_KEY')

def getInfo (): # Function to get the info

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # Coinmarketcap API url

    parameters = { 'slug': crypto, 'convert': converted } # API parameters to pass in for retrieving specific cryptocurrency data

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_mkt_api_key
    } # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)

    pprint.pprint(info)
        
getInfo() # Calling the function to get the statistics

"""Initialize the first dataframe"""

# Format current date as ISO format
start_date = (pd.Timestamp.utcnow() - pd.Timedelta(4,'h')).isoformat()
end_date = pd.Timestamp.utcnow().isoformat() 
# timeframe = '15m'
crypto_data = coin_mkt_api_key(
    crypto,
    start = start_date,
    end = end_date
).df
crypto_data = crypto_data.dropna()
print(crypto_data)


while True:
    
    c = False
    while c == False:
        if (pd.Timestamp.utcnow().minute % int(t_num) == 0 and
            crypto_data.index[-1].minute != pd.Timestamp.utcnow().minute
        ):
            c = True
    #exit the while loop and update the dataframe

    crypto_data = coin_mkt_api_key.get_barset(
        crypto,
        start = start_date,
        end = pd.Timestamp.utcnow().isoformat()
    ).df
    crypto_data = crypto_data.dropna()
    
    #create a dataframe of the close prices
    
    close_df = pd.DataFrame()

    for ticker in tickers:
        close_df[str(ticker)] = crypto_data[str(ticker)]['close']

    #calculate 14 period rsi for dataframe
    rsi_period = 14
    chg = close_df.diff(1)
    gain = chg.mask(chg<0,0)
    loss = chg.mask(chg>0,0)
    avg_gain = gain.ewm(com = rsi_period-1,min_periods=rsi_period).mean()
    avg_loss = loss.ewm(com = rsi_period-1,min_periods=rsi_period).mean()
    rs = abs(avg_gain / avg_loss)
    rsi_close = 100 - (100/(1+rs))

    # code to generate signal
    rsi_sell = (rsi_close>70) & (rsi_close.shift(1)<=70)
    rsi_buy = (rsi_close<30) & (rsi_close.shift(1)>=30)
    
    rsi_signals=pd.concat([rsi_buy.iloc[-1],rsi_sell.iloc[-1]],axis=1)
    rsi_signals.columns=['RSI Buy', 'RSI Sell']

    # calculate ma for dataframe
    ma_short = close_df.ewm(span=12, adjust=False).mean()
    ma_long = close_df.ewm(span=26, adjust=False).mean()
    
    # code to generate signals and dataframe
    ma_sell = ((ma_short <= ma_long) & (ma_short.shift(1) >= ma_long.shift(1)))
    ma_buy = ((ma_short >= ma_long) & (ma_short.shift(1) <= ma_long.shift(1)))

    ma_signals=pd.concat([ma_buy.iloc[-1], ma_sell.iloc[-1]], axis=1)
    ma_signals.columns=['MA Buy','MA Sell']
    all_signals=pd.concat([rsi_signals,ma_signals],axis=1)
    

    # send message if any values in dataframe are true
    if True in all_signals.values:
        some_text = f'you have a stock signal {all_signals}'
        send(some_text)