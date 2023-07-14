from client import client
from space_traders_api_client.api.systems import (
    get_jump_gate,
    get_system_waypoints,
    get_market
)

from get_ships_list import ship_list, Ship, ship_dict

from data_decode import data_decode

import pandas as pd
import duckdb

from time import sleep
import pprint as pp


"""
this needs: 
    -an initial market_data creating method
    -use pickled market_data if it exists 
    -market_data update that replaces older timestamp of same systems, adds new systems 

"""


def _create_market_data():

market_data = {}

for k, ship in ship_dict.items():
    location = ship.nav_location
    wp_location = ship.nav_waypoint_location
    market_data[k] = data_decode(get_market.sync_detailed(location, wp_location, client=client).content)

df_market = pd.DataFrame()
# print(market_data[0])
goods_list = []

for item in market_data.values():

    # tradeGoods seems to capture everything of interest
    for good in item['tradeGoods']:
        goods_list.append([
            item['symbol'],
            good['symbol'],
            good['purchasePrice'],
            good['sellPrice'],
            good['supply'],
            good['tradeVolume']]
        )
        # goods_list.append([*item.values()]) # yeah no, good to remember it's an option, but this isn't doing it

# df_weird_test = pd.DataFrame(goods_list)
# print(df_weird_test)
df_goods = pd.DataFrame(goods_list,
                        columns=['system', 'symbol', 'purchase_price', 'sell_price', 'supply', 'trade_volume'])
df_goods['timestamp'] = pd.Timestamp.now()

df_market_data = pd.DataFrame()
df_market_data = pd.concat([df_market_data, df_goods])

con = duckdb.connect("file.db")
duckdb.sql("CREATE TABLE market_data AS SELECT * FROM df_market_data").df()
con.sql()

# print(df_market_data['system'], df_market_data['symbol'], df_market_data['purchase_price'])


cargo_items = ship_list[0].get_ship_cargo()
# print(cargo_items)

def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')



# print(df_market_data['system'], df_market_data['symbol'],df_market_data['sell_price'])
print_full(df_market_data)


def find_best_deal(trade_goods:list[str]):
    # best_deal = df_market_data[["symbol"] == trade_good]

    #is there only one market that's buying these or is something getting lost along the way?

    for good in trade_goods:
        best_deal = df_market_data.loc[df_market_data['symbol'] == good[0]]
        print_full(best_deal)
        # row = best_deal['sell_price'].idxmax()
        # print(best_deal.loc[row])
    # print(best_deal["purchase_price"].max())





    # df = pd.DataFrame()
    # print(df_market_data.where(df_market_data['symbol'] == trade_good).max(df_market_data["purchase_price"]))
    # df_market_data[df_market_data[trade_good] == df_market_data[trade_good].max()]
    # print(df_market_data.groupby("symbol")['purchase_price'].max())
    # df['max_col'] = df_market_data.filter(like='purchase_price').max()
    # df['max_col'] = df.filter(like='Col_').idxmax(axis=1)
    # print(df)
    # print(df_market_data['purchase_price'].idxmax())
    # print(df_market_data.loc[15])


    # df_trade_good = df_market_data.where(df_market_data['symbol'] == trade_good)
    # print(df_market_data.where(df_market_data['symbol'] == trade_good))
    # df_trade_good.max(df_trade_good['purchase_price'])


print(ship_list[0].symbol, ship_list[0].nav_waypoint_location)
find_best_deal(cargo_items)


# df_goods
# print(goods_list)
# print(df_goods)

# print(df_market_data)

df_market_data.to_pickle("./market_data.pkl")

# Examples
#
# original_df = pd.DataFrame({"foo": range(5), "bar": range(5, 10)})
#
# original_df
#    foo  bar
# 0    0    5
# 1    1    6
# 2    2    7
# 3    3    8
# 4    4    9
#
# original_df.to_pickle("./dummy.pkl")
#
# unpickled_df = pd.read_pickle("./dummy.pkl")
#
# unpickled_df
#    foo  bar
# 0    0    5
# 1    1    6
# 2    2    7
# 3    3    8
# 4    4    9
#
# import os
#
# os.remove("./dummy.pkl")
