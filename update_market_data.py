from client import client
from space_traders_api_client.api.systems import (
    get_jump_gate,
    get_system_waypoints,
    get_market
)



from get_ships import ship_list, Ship, ship_dict
from df_print_full import df_print_full
from data_decode import data_decode

import pandas as pd
import duckdb
import sqlalchemy as sa


from time import sleep
import pprint as pp


engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')

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

    TODO this should probably be updated to use a sqlalchemy model-- should it though?

    todo this should happen as part of navigation if the waypoint has a market



    :param table_name:
    :return:
    """
    market_data = {}

    for k, ship in ship_dict.items():
        location = ship.nav_location
        wp_location = ship.nav_waypoint_location
        print(location, wp_location)

        response = get_market.sync_detailed(location,wp_location,client=client)
        if response.status_code in [200, 201]:

            print(response)

        if response.status_code not in [200, 201]:
            return response
        market_data[k] = data_decode(response.content)
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


#TODO closer, but need to cull older duplicate market data or it will get too big


df_market_data_from_sql = pd.read_sql("market_data", engine)
# print(df_market_data_from_sql)
#todo might have to rewrite or create a new way of getting ship system waypoints

#the basic idea is just to see if waypoint from list of system waypoints exists
# in market_data['system'] and add it to a To Visit list
# print(df_market_data_from_sql['system'].)
s = df_market_data_from_sql['system']

ship_system_waypoints = ship_list[0].get_ship_system_waypoints(markets=True)
needs_market_data = []
for system_waypoint in ship_system_waypoints.values():

    if system_waypoint[0] not in (s.values):
        needs_market_data.append(system_waypoint)

print("unvisited markets in system")
for system in needs_market_data:
    print(system)
# print(needs_market_data)
# print()
# df_print_full(df_market_data_from_sql)


# df_print_full(df_market_data_from_sql.sort_values(df_market_data_from_sql['system']))

# ['X1-JF24-77691C', 'X1-JF24-06790Z', 'X1-JF24-97552X',
#  'X1-JF24-78153C', 'X1-JF24-01924F', 'X1-JF24-23225F',
#  'X1-JF24-45556D', 'X1-JF24-73757X', 'X1-JF24-34538X', 'X1-JF24-00189Z']