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
import sqlalchemy as sa

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')


from time import sleep
import pprint as pp


"""
this needs: 

    -market_data update that replaces older timestamp of same systems, adds new systems
    -some sort of agent/event subscription that divides up getting market data based on oldest timestamp etc 

"""

# def wallet_df_to_sql(table_name: str, engine=engine):
#     player_credits = get_player_credits()
#     df = player_credits_to_df(player_credits)
#     df.to_sql(table_name, engine, if_exists="append")




# def _create_market_data():

def update_market_data(table_name="market_data"):
    """
    i want this to have the ship that's the source of the market data-- this is going to need to be reworked to do it,
    or i could just try to match waypoints near the end of it

    :param table_name:
    :return:
    """
    market_data = {}

    for k, ship in ship_dict.items():
        location = ship.nav_location
        wp_location = ship.nav_waypoint_location
        market_data[k] = data_decode(get_market.sync_detailed(location, wp_location, client=client).content)
    df_market = pd.DataFrame()
    goods_list = []
    for item in market_data.values():
        for good in item['tradeGoods']:
            goods_list.append([
                item['symbol'],
                good['symbol'],
                good['purchasePrice'],
                good['sellPrice'],
                good['supply'],
                good['tradeVolume']]
            )

    df_goods = pd.DataFrame(goods_list,
                            columns=['system', 'symbol', 'purchase_price', 'sell_price', 'supply', 'trade_volume'])
    df_goods['timestamp'] = pd.Timestamp.now()
    df_market_data = pd.DataFrame()
    df_market_data = pd.concat([df_market_data, df_goods])
    df_market_data.to_sql(table_name, engine, if_exists="append")

update_market_data()

#
#
# market_data = {}
#
# for k, ship in ship_dict.items():
#     location = ship.nav_location
#     wp_location = ship.nav_waypoint_location
#     market_data[k] = data_decode(get_market.sync_detailed(location, wp_location, client=client).content)
#
# df_market = pd.DataFrame()
# # print(market_data[0])
# goods_list = []
#
# for item in market_data.values():
#
#     # tradeGoods seems to capture everything of interest
#     for good in item['tradeGoods']:
#         goods_list.append([
#             item['symbol'],
#             good['symbol'],
#             good['purchasePrice'],
#             good['sellPrice'],
#             good['supply'],
#             good['tradeVolume']]
#         )
#         # goods_list.append([*item.values()]) # yeah no, good to remember it's an option, but this isn't doing it
#
# # df_weird_test = pd.DataFrame(goods_list)
# # print(df_weird_test)
# df_goods = pd.DataFrame(goods_list,
#                         columns=['system', 'symbol', 'purchase_price', 'sell_price', 'supply', 'trade_volume'])
# df_goods['timestamp'] = pd.Timestamp.now()
#
# df_market_data = pd.DataFrame()
# df_market_data = pd.concat([df_market_data, df_goods])
#
# con = duckdb.connect("file.db")
# # con.sql("INSERT * ")
# # con.sql("CREATE TABLE market_data AS SELECT * FROM df_market_data")
# con.sql("INSERT INTO market_data SELECT * FROM df_market_data")
# # print(con.sql("SELECT COUNT(*) FROM system").df())
# print(con.sql("SELECT * FROM market_data"))