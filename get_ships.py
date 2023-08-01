from datetime import datetime

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from client import client
from data_decode import data_decode, error_decode
from df_print_full import df_print_full
from df_to_sql import df_to_sql_table
from space_traders_api_client.api.fleet import (
    get_my_ships, refuel_ship, orbit_ship, dock_ship, navigate_ship, get_my_ship_cargo
)
from space_traders_api_client.api.systems import get_system_waypoints
from space_traders_api_client.models import RefuelShipJsonBody, NavigateShipJsonBody
from space_traders_api_client import errors
# import duckdb
import pprint as pp
from SECRETS import sql_account, sql_pw
engine = sa.create_engine(f"postgresql://{sql_account}:{sql_pw}@localhost:5432/spacetraders")

Session = sessionmaker(bind=engine)


def get_ships_list(full=False) -> dict[int, dict[list]]:
    """
    i wanted a version of this that preserved all of the data that is part of a ship object rather than grabbing what i want and then having to backfill stuff i missed later

    :return:
    """
    response = get_my_ships.sync_detailed(client=client)
    # sa.values()

    # i know there has to be a better way of doing this but for now

    # headers = response.headers
    # parsed = response.parsed
    # print(type(parsed))
    #
    #
    # s = Session()
    # s_c = StatusCode(status_code=status_code)
    # s.add(s_c)
    # s.commit()
    # s.close()
    #
    # print(status_code)
    # print(headers)
    # print(headers['date'])
    # print(parsed)

    ship_list = data_decode(response.content)
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

            # need more nav -- going to have to deal with route departure/arrival etc

            # frame has module slots and mount points etc

            "fuel_current": ship["fuel"]["current"],
            "fuel_capacity": ship["fuel"]["capacity"],

            "cargo_current": cargo_tuple_list,
            "cargo_capacity": ship["cargo"]["capacity"]
        }

        name = ship['symbol']
        # this looks like the easiest way to organize ALL of the data
        # and then i can slice it up as desired-- a lot of these also have separate api calls that might make more sense dealing with this?
        full_ships_dict[(name, 'registration')] = ship['registration']
        full_ships_dict[(name, 'nav')] = ship['nav']
        full_ships_dict[(name, 'nav', 'route')] = ship['nav']['route']
        full_ships_dict[(name, 'crew')] = ship['crew']
        full_ships_dict[(name, 'frame')] = ship['frame']
        full_ships_dict[(name, 'reactor')] = ship['reactor']
        full_ships_dict[(name, 'engine')] = ship['engine']
        full_ships_dict[(name, 'modules')] = ship['modules']
        full_ships_dict[(name, 'mounts')] = ship['mounts']
        full_ships_dict[(name, 'cargo')] = ship['cargo']
        full_ships_dict[(name, 'fuel')] = ship['fuel']

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
    def __init__(self, symbol: str, role: str, nav_location: str, nav_waypoint_location: str, nav_status: str,
                 nav_flight_mode: str, fuel_current: int, fuel_capacity: int, cargo_current: list[tuple],
                 cargo_capacity: int):
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
        return f"{self.symbol} {self.role} {self.nav_location} {self.nav_waypoint_location} {self.nav_status}"

    def __repr__(self):
        return f"{self.symbol}, {self.role}, {self.nav_location}, {self.nav_waypoint_location}, {self.nav_status}, {self.nav_flight_mode}, {self.fuel_current}, {self.fuel_capacity}, {self.cargo_current}, {self.cargo_capacity}"

    def set_systems_in_jumpgate_range(self, systems_in_jumpgate_range: dict):
        self.systems_in_jumpgate_range = systems_in_jumpgate_range

    def update_current_cargo(self):
        ship_cargo = get_my_ship_cargo.sync_detailed(self.symbol, client=client).content
        ship_cargo = data_decode(ship_cargo)
        cargo = ship_cargo['inventory']
        cargo_tuple_list = []
        for item in cargo:
            cargo_tuple_list.append((item['symbol'], item['units']))
        self.cargo_current = cargo_tuple_list

    def check_cargo(self):
        self.update_current_cargo()
        cargo_sum = 0
        for item in self.cargo_current:
            cargo_sum = cargo_sum + item[1]
        print(f"{self.cargo_current}")
        print(f"{self.cargo_capacity - cargo_sum} units remaining")

    def get_systems_in_range_of_jumpgate(self):
        """
        this actually doesn't make sense in this context because the input/selection logic isn't handled by Ship,
        though maybe it should be? also maybe i should just return a dict of the choices?
        :return: now it returns a dict of int choices for systems in jumpgate range
        """
        from jumpgate_lookup import jumpgate_lookup
        jumpgate_lookup(self.nav_location)

    def nav_ship(self, waypoint):
        """
        just copying the old nav. this still needs to handle fuel and travel time and all that stuff

        :param waypoint:
        :return:
        """
        # todo this isn't working and i still haven't figured out where nav_status and nav_flight_mode have mixed up
        if self.nav_status == "DOCKED":
            print("undocking")
            self.orbit_current_waypoint()
        _nav_ship = NavigateShipJsonBody(waypoint)
        nav_results = navigate_ship.sync_detailed(self.symbol, json_body=_nav_ship, client=client)
        if nav_results.status_code in [200, 201]:
            nav_decode = data_decode(nav_results.content)
            print(datetime.fromisoformat(nav_decode['nav']['route']['arrival']) - datetime.fromisoformat(
                nav_decode['nav']['route']['departureTime']), 'travel time')
            # print(nav_decode['route'])
            # nav_results = data_decode(nav_results.content)
            print(nav_results.content)
        else:
            print(error_decode(nav_results.content))

        # print(nav_results)
        # todo clean up the response/status code/etc

    def orbit_current_waypoint(self):
        orbit_results = orbit_ship.sync_detailed(self.symbol, client=client)
        if orbit_results.status_code in [200, 201]:
            print(f"orbiting {self.nav_waypoint_location}")

            pass
        else:
            print(error_decode(orbit_results.content))

    def dock(self):
        dock_results = dock_ship.sync_detailed(self.symbol, client=client)
        if dock_results.status_code in [200, 201]:
            print(f"docking {self.nav_waypoint_location}")

            pass
        else:
            print(error_decode(dock_results.content))
        pass

    def refuel_ship(self):
        _refuel_json = RefuelShipJsonBody()

        refuel_results = refuel_ship.sync_detailed(self.symbol, client=client, json_body=_refuel_json)
        if refuel_results.status_code in [200, 201]:
            print(f"refueling {self.symbol}")
        else:
            print(error_decode(refuel_results.content))

    def get_ship_system_waypoints(self, markets=False):
        """
        todo i should be storing this in the db to reduce the number of api calls
        :param markets:
        :return:
        """
        # todo more response handling
        raw_system_waypoints = data_decode(get_system_waypoints.sync_detailed(self.nav_location,
                                                                              limit=20,
                                                                              # currently limited to 20 results without dealing with pagination
                                                                              client=client).content)
        # print(raw_system_waypoints)
        waypoint_dict = {}
        dict_index = 0
        for waypoint in raw_system_waypoints:
            print(waypoint['symbol'])
            trait_list = []
            for trait in waypoint['traits']:
                trait_list.append(trait['symbol'])

            waypoint_dict[dict_index] = waypoint['symbol'], waypoint['type'], trait_list
            dict_index += 1
        return waypoint_dict

        # waypoint_dict = {}
        # market_dict = {}
        # dict_index = 0
        # for waypoint in raw_system_waypoints:
        #     waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type']]
        #     for trait in waypoint['traits']:
        #         # todo arg to limit it to market+shipyard
        #         if trait['symbol'] == "MARKETPLACE" or trait['symbol'] == "SHIPYARD" \
        #                 or trait['symbol'] == "JUMP_GATE" or trait['symbol'] == "ASTEROID_FIELD":
        #             waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type'], trait['symbol']]
        #         if markets is True:
        #             if trait['symbol'] == "MARKETPLACE":
        #                 market_dict[dict_index] = [waypoint['symbol'], waypoint['type'], trait['symbol']]
        #     # print(waypoint['traits'])
        #     dict_index += 1
        # # TODO - okay, i need to add more details about the features of each waypoint
        # # print(waypoint['symbol'], waypoint['type'])
        # # pp.pprint(waypoint_dict.items())
        # pp.pprint(waypoint_dict)
        # if markets is True:
        #     return market_dict
        # return waypoint_dict

    # def get_jumpgate_systems(self):


def create_ship_object_dict(raw_ships_dict: dict) -> dict[int:Ship]:
    """

    :param raw_ships_dict: uses the dict values to create a dataclass
    :return: a dict [int(0:n of ships) : ship object
    """
    ship_dict = {}
    for i in range(1, len(raw_ships_dict) + 1):
        # print(Ship(*raw_ships_dict[i].values()))
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
# df = pd.DataFrame.from_dict(raw_ship_dict)
# df_print_full(df)

df_to_sql_table(df, "ships", if_exists="replace")

#
# df_test = pd.read_sql("ships", engine)
# df_print_full(df_test)


# TODO think about this biz, i could effectively store a ship object and convert back and forth?
# from models import Ships
# from ships_to_sql import ships_to_sql
#
# for ship in ship_list:
#     ships_to_sql(ship)
