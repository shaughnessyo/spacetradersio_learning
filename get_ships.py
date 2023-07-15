from space_traders_api_client.api.systems import get_system_waypoints
from dataclasses import dataclass
import player
from client import client

from data_decode import data_decode
import pprint as pp
import pandas as pd
from df_print_full import df_print_full

# import duckdb

from space_traders_api_client.api.fleet import (
    get_my_ships, get_my_ship_cargo, navigate_ship, refuel_ship, orbit_ship
)

import sqlalchemy as sa
from df_to_sql import append_df_to_sql_table




engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')



def get_ships_list(full=False) -> dict[int, dict[list]]:
    """
    i wanted a version of this that preserved all of the data that is part of a ship object rather than grabbing what i want and then having to backfill stuff i missed later

    :return:
    """
    ship_list = data_decode(get_my_ships.sync_detailed(client=client).content)
    # print(ship_list)

    full_ships_dict = {}
    counter = 1
    by_full_ship_dict = {}

    my_ships_dict = {}
    my_nested_ships_dict = {}
    for ship in ship_list:

        cargo_tuple_list = []
        cargo = ship['cargo']['inventory']
        for item in cargo:
            cargo_tuple_list.append((item['symbol'], item['units']))

        my_ships_dict = {

        "symbol": ship["symbol"],
        "role": ship['registration']['role'],
        "nav_location": ship["nav"]["systemSymbol"],
        "nav_waypoint_location": ship["nav"]["waypointSymbol"],
        "nav_flight_mode": ship["nav"]["flightMode"],
        "nav_status": ship["nav"]["status"],

        #need more nav -- going to have to deal with route departure/arrival etc

        #frame has module slots and mount points etc

        "fuel_current": ship["fuel"]["current"],
        "fuel_capacity": ship["fuel"]["capacity"],

        "cargo_current": cargo_tuple_list,
        "cargo_capacity": ship["cargo"]["capacity"]
        }

        name = ship['symbol']
        #this looks like the easiest way to organize ALL of the data
        #and then i can slice it up as desired-- a lot of these also have separate api calls that might make more sense dealing with this?
        full_ships_dict[(name,'registration')] = ship['registration']
        full_ships_dict[(name,'nav')] = ship['nav']
        full_ships_dict[(name,'nav','route')] = ship['nav']['route']
        full_ships_dict[(name,'crew')] = ship['crew']
        full_ships_dict[(name,'frame')] = ship['frame']
        full_ships_dict[(name,'reactor')] = ship['reactor']
        full_ships_dict[(name,'engine')] = ship['engine']
        full_ships_dict[(name,'modules')] = ship['modules']
        full_ships_dict[(name,'mounts')] = ship['mounts']
        full_ships_dict[(name,'cargo')] = ship['cargo']
        full_ships_dict[(name,'fuel')] = ship['fuel']

        by_full_ship_dict[counter] = full_ships_dict
        my_nested_ships_dict[counter] = my_ships_dict

        counter += 1
    if full is True:
        return full_ships_dict
    if full is False:
        return my_nested_ships_dict


raw_ship_dict = get_ships_list(full=False)
# print(raw_ship_dict)
# print(ship_dict.keys())





class Ship:
    def __init__(self, symbol:str, role:str, nav_location:str, nav_waypoint_location:str, nav_status:str, nav_flight_mode:str, fuel_current:int, fuel_capacity:int, cargo_current: list[tuple], cargo_capacity:int):
        self.symbol = symbol
        self.role = role
        self.nav_location = nav_location
        self.nav_waypoint_location = nav_waypoint_location
        self.nav_status = nav_status
        self.nav_flight_mode = nav_flight_mode
        self.fuel_current = fuel_current
        self.fuel_capacity = fuel_capacity
        self.cargo_current = cargo_current
        self.cargo_capacity = cargo_capacity
        self.systems_in_jumpgate_range = None


    def __str__(self):
        """
        not bad, maybe revisit
        :return:
        """
        return f"{self.symbol} {self.role} {self.nav_location} {self.nav_waypoint_location}"

    def __repr__(self):
        return f"{self.symbol}, {self.role}, {self.nav_location}, {self.nav_waypoint_location}, {self.nav_status}, {self.nav_flight_mode}, {self.fuel_current}, {self.fuel_capacity}, {self.cargo_current}, {self.cargo_capacity}"

    def set_systems_in_jumpgate_range(self, systems_in_jumpgate_range: dict):
        self.systems_in_jumpgate_range = systems_in_jumpgate_range

#i don't remember if i ended up using get_ship_system_waypoints
    # def get_ship_system_waypoints(self):
    #     raw_system_waypoints = data_decode(get_system_waypoints.sync_detailed(self.nav_location, client=client).content)
    #     clean_system_waypoint_list = []
    #     # print(raw_system_waypoints)
    #     waypoint_dict = {}
    #     dict_index = 0
    #     for waypoint in raw_system_waypoints:
    #         waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type']]
    #         for trait in waypoint['traits']:
    #             if trait['symbol'] == "MARKETPLACE" or trait['symbol'] == "SHIPYARD" or trait['symbol'] == "JUMP_GATE":
    #                 waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type'], trait['symbol']]
    #
    #         print(waypoint['traits'])
    #         dict_index += 1
    #     #TODO - okay, i need to add more details about the features of each waypoint
    #         # print(waypoint['symbol'], waypoint['type'])
    #     # pp.pprint(waypoint_dict.items())
    #     pp.pprint(waypoint_dict)
    #     return waypoint_dict

    def nav_ship(self, waypoint):
        pass

    def orbit_current_waypoint(self):
        print(f"orbiting {self.nav_waypoint_location}")
        orbit_ship.sync_detailed(self.symbol, client=client)
    def refuel_ship(self):
        pass




def create_ship_object_dict(raw_ships_dict: dict) -> dict[int:Ship]:
    """

    :param raw_ships_dict: uses the dict values to create a dataclass
    :return: a dict [int(0:n of ships) : ship object
    """
    ship_dict = {}
    for i in range(1, len(raw_ships_dict)+1):
        print(Ship(*raw_ships_dict[i].values()))
        ship_dict[i] = Ship(*raw_ships_dict[i].values())

    return ship_dict

ship_dict = create_ship_object_dict(raw_ship_dict)
# print(raw_ship_dict)
# print(ship_dict.keys(), ship_dict.items())
# print(ship_dict.values())

ship_list = []
for ship in ship_dict.values():
    # print(ship)
    ship_list.append(ship)


# def ship_list_to_df():
df = pd.DataFrame.from_dict(raw_ship_dict).transpose()
df_print_full(df)