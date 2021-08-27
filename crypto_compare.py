import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
from datetime import timezone
import altair as alt
import numpy as np

cg = CoinGeckoAPI()

st.title("Crypto Compare")
st.markdown("![Alt Text](https://media.giphy.com/media/K6hbXJZsgWN8CPbCvK/giphy.gif)")
st.write("""
Calculates the Cumulative Returns of cryptoassets for easier performance comparison.
""")


tickers = ('bitcoin', 'ethereum', 'tether', 'binancecoin', 'cardano', 'ripple', 'dogecoin', 'usd-coin', 'polkadot',
 'uniswap', 'binance-usd', 'bitcoin-cash', 'solana', 'litecoin', 'chainlink', 'matic-network', 'wrapped-bitcoin',
 'ethereum-classic', 'theta-token', 'stellar', 'internet-computer', 'dai', 'vechain', 'filecoin', 'tron',
 'shiba-inu', 'aave', 'eos', 'monero', 'cosmos', 'compound-usd-coin', 'terra-luna', 'crypto-com-chain',
 'cdai', 'algorand', 'leo-token', 'celsius-degree-token', 'pancakeswap-token', 'okb', 'amp-token', 'compound-ether',
 'bitcoin-cash-sv', 'ftx-token', 'maker', 'neo', 'klay-token', 'iota', 'tezos', 'compound-governance-token', 
 'avalanche-2', 'the-graph', 'terrausd', 'kusama', 'theta-fuel', 'elrond-erd-2', 'havven', 'thorchain', 
 'bittorrent-2', 'huobi-token', 'safemoon', 'decred', 'hedera-hashgraph', 'sushi', 'true-usd', 'waves',
 'staked-ether', 'huobi-btc', 'dash', 'chiliz', 'zcash', 'yearn-finance', 'xdce-crowd-sale', 'enjincoin',
 'helium', 'blockstack', 'nem', 'holotoken', 'telcoin', 'quant-network', 'kucoin-shares', 'paxos-standard',
 'harmony', 'zilliqa', 'nexo', 'mdex', 'near', 'titanswap', 'decentraland', 'basic-attention-token', 
 'bitcoin-gold', 'liquity-usd', '0x', 'bancor', 'axie-infinity', 'qtum', 'zencash', 'ecomi', 'flow',
 'siacoin', 'compound-usdt')

dropdown = st.multiselect ('Please pick cryptoassets (max=5)', tickers, default=["bitcoin"])


def datetime_to_unix(year, month, day):
    '''datetime_to_unix(2021, 6, 1) => 1622505600.0'''
    dt = datetime(year, month, day)
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    return timestamp

def unix_to_datetime(unix_time):
    '''unix_to_datetime(1622505700)=> ''2021-06-01 12:01am'''
    ts = int(unix_time/1000 if len(str(unix_time)) > 10 else unix_time) # /1000 handles milliseconds
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d').lower()

def relativeret(df):
    rel= df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


start = st.date_input ('Start date', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End date', value = pd.to_datetime('today'))

start_from = start.strftime('%Y-%m-%d')
end_at = end.strftime('%Y-%m-%d')

start_year = start_from[0:-6]
start_month = start_from[5:-3]
start_day = start_from[8:]
end_year = end_at[0:-6]
end_month = end_at[5:-3]
end_day = end_at[8:]


a_list = []

for idx, val in enumerate(dropdown):
    
    result = cg.get_coin_market_chart_range_by_id(
    id=val, 
    vs_currency='usd',
    from_timestamp=datetime_to_unix(int(start_year), int(start_month), int(start_day)),
    to_timestamp=datetime_to_unix(int(end_year), int(end_month), int(end_day)))
    a_list.append(result['prices'])



if len(a_list)==1:
    index = ( unix_to_datetime(i[0]) for i in a_list[0] )
    p_array = np.array(a_list[0])
    asset = p_array[:,1]

    d = dict( index =index, asset = asset )
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))

    #df = pd.DataFrame({'time':time, 'price':price})
    df=df.fillna(0)
    x_cols = [x for x in df.columns if x != 'index']
    x_cols1 = df[x_cols]   
    x_cols1 = relativeret(x_cols1)
    df_new = pd.merge(df['index'], x_cols1, right_index = True,
               left_index = True)


if len(a_list)==2:
    time1 = ( unix_to_datetime(i[0]) for i in a_list[0] )
    p_array1 = np.array(a_list[0])
    coin1 = p_array1[:,1]
    p_array2 = np.array(a_list[1])
    coin2 = p_array2[:,1]
 
#asset1 is a df for the first asset
    asset1 = pd.DataFrame({'time1':time1,'coin1':coin1})
    time2 = ( unix_to_datetime(i[0]) for i in a_list[1] )
    asset2 = pd.DataFrame({'time2':time2,'coin2':coin2})

    asset1 = asset1.set_index('time1')
    asset2 = asset2.set_index('time2')

    df = pd. concat([asset1['coin1'],asset2['coin2']], axis=1, keys=['asset1', 'asset2'])

    df=df.fillna(0)
    df.reset_index(inplace=True)
    x_cols = [x for x in df.columns if x != 'index']
    x_cols1 = df[x_cols]   
    x_cols1 = relativeret(x_cols1)
    df_new = pd.merge(df['index'], x_cols1, right_index = True,
               left_index = True)



if len(a_list)==3:
    time1 = ( unix_to_datetime(i[0]) for i in a_list[0] )
    p_array1 = np.array(a_list[0])
    coin1 = p_array1[:,1]
    p_array2 = np.array(a_list[1])
    coin2 = p_array2[:,1]
    p_array3 = np.array(a_list[2])
    coin3 = p_array3[:,1]


#asset1 is a df for the first asset
    asset1 = pd.DataFrame({'time1':time1,'coin1':coin1})
    time2 = ( unix_to_datetime(i[0]) for i in a_list[1] )
    asset2 = pd.DataFrame({'time2':time2,'coin2':coin2})
    time3 = ( unix_to_datetime(i[0]) for i in a_list[2] )
    asset3 = pd.DataFrame({'time3':time3,'coin3':coin3})


    asset1 = asset1.set_index('time1')
    asset2 = asset2.set_index('time2')
    asset3 = asset3.set_index('time3')

    df = pd. concat([asset1['coin1'],asset2['coin2'],asset3['coin3']], axis=1, keys=['asset1', 'asset2','asset3'])
    df=df.fillna(0)
    df.reset_index(inplace=True)
    x_cols = [x for x in df.columns if x != 'index']
    x_cols1 = df[x_cols]   
    x_cols1 = relativeret(x_cols1)
    df_new = pd.merge(df['index'], x_cols1, right_index = True,
               left_index = True)




if len(a_list)==4:
    time1 = ( unix_to_datetime(i[0]) for i in a_list[0] )
    p_array1 = np.array(a_list[0])
    coin1 = p_array1[:,1]
    p_array2 = np.array(a_list[1])
    coin2 = p_array2[:,1]
    p_array3 = np.array(a_list[2])
    coin3 = p_array3[:,1]
    p_array4 = np.array(a_list[3])
    coin4 = p_array4[:,1]

#asset1 is a df for the first asset
    asset1 = pd.DataFrame({'time1':time1,'coin1':coin1})
    time2 = ( unix_to_datetime(i[0]) for i in a_list[1] )
    asset2 = pd.DataFrame({'time2':time2,'coin2':coin2})
    time3 = ( unix_to_datetime(i[0]) for i in a_list[2] )
    asset3 = pd.DataFrame({'time3':time3,'coin3':coin3})
    time4 = ( unix_to_datetime(i[0]) for i in a_list[3] )
    asset4 = pd.DataFrame({'time4':time4,'coin4':coin4})

    asset1 = asset1.set_index('time1')
    asset2 = asset2.set_index('time2')
    asset3 = asset3.set_index('time3')
    asset4 = asset4.set_index('time4')

    df = pd. concat([asset1['coin1'],asset2['coin2'],asset3['coin3'],asset4['coin4']], axis=1, keys=['asset1', 'asset2','asset3','asset4'])


    df=df.fillna(0)
    df.reset_index(inplace=True)
    x_cols = [x for x in df.columns if x != 'index']
    x_cols1 = df[x_cols]   
    x_cols1 = relativeret(x_cols1)
    df_new = pd.merge(df['index'], x_cols1, right_index = True,
               left_index = True)





if len(a_list)==5:
    time1 = ( unix_to_datetime(i[0]) for i in a_list[0] )
    p_array1 = np.array(a_list[0])
    coin1 = p_array1[:,1]
    p_array2 = np.array(a_list[1])
    coin2 = p_array2[:,1]
    p_array3 = np.array(a_list[2])
    coin3 = p_array3[:,1]
    p_array4 = np.array(a_list[3])
    coin4 = p_array4[:,1]
    p_array5 = np.array(a_list[4])
    coin5 = p_array5[:,1]



#asset1 is a df for the first asset
    asset1 = pd.DataFrame({'time1':time1,'coin1':coin1})
    time2 = ( unix_to_datetime(i[0]) for i in a_list[1] )
    asset2 = pd.DataFrame({'time2':time2,'coin2':coin2})
    time3 = ( unix_to_datetime(i[0]) for i in a_list[2] )
    asset3 = pd.DataFrame({'time3':time3,'coin3':coin3})
    time4 = ( unix_to_datetime(i[0]) for i in a_list[3] )
    asset4 = pd.DataFrame({'time4':time4,'coin4':coin4})
    time5 = ( unix_to_datetime(i[0]) for i in a_list[4] )
    asset5 = pd.DataFrame({'time5':time5,'coin5':coin5})


    asset1 = asset1.set_index('time1')
    asset2 = asset2.set_index('time2')
    asset3 = asset3.set_index('time3')
    asset4 = asset4.set_index('time4')
    asset5 = asset5.set_index('time5')

    df = pd. concat([asset1['coin1'],asset2['coin2'],asset3['coin3'],asset4['coin4'],asset5['coin5']], axis=1, keys=['asset1', 'asset2','asset3','asset4','asset5'])


    df=df.fillna(0)
    df.reset_index(inplace=True)
    x_cols = [x for x in df.columns if x != 'index']
    x_cols1 = df[x_cols]   
    x_cols1 = relativeret(x_cols1)
    df_new = pd.merge(df['index'], x_cols1, right_index = True,
               left_index = True)    




df_new = df_new.set_index('index')
df_new

#st.line_chart(df_new)

data = df_new.reset_index().melt('index')

my_chart = alt.Chart(data).mark_line().encode(
    x=alt.X('index:T', title='Time'),
    y='value',
    color='variable'
).properties(
    width=900,
    height=400
).interactive()

st.altair_chart(my_chart)
