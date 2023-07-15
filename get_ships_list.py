"""
this needs to be cleaned up a bit


"""

from dataclasses import dataclass
import player
from data_decode import data_decode
# from current_systems_jumpgate_map import current_connected_systems

from space_traders_api_client import AuthenticatedClient
from space_traders_api_client.api.fleet import (
    get_my_ships, get_my_ship_cargo, navigate_ship, refuel_ship, orbit_ship
)

# from space_traders_api_client.api.fleet import get_my_ships
import ast
import pprint as pp

from client import client
from space_traders_api_client.api.systems import get_system_waypoints
from space_traders_api_client.models import NavigateShipJsonBody, RefuelShipJsonBody


def get_ships_list(raw=False, ship_dict=False) -> dict[int, dict[list]]:
    ship_list = get_my_ships.sync_detailed(client=client).content
    ship_list = ship_list.decode()
    ship_list = ast.literal_eval(ship_list)
    # print(ship_list)
    ship_list = ship_list["data"]

    # print(ship_list)
    if raw:
        # pp.pprint(ship_list)
        return ship_list

    if ship_dict is False:
        my_ships = []

        for ship in ship_list:
            print(
                ship["symbol"],
                ship["nav"]["systemSymbol"],
                ship["registration"]["role"],
            )
            my_ships.append(
                [
                    ship["symbol"],
                    ship["nav"]["systemSymbol"],
                    ship["registration"]["role"],
                ]
            )
        return my_ships

    elif ship_dict is True:
        # my_ships_dict = {}
        bigger_dict = {}
        i = 0
        for ship in ship_list:

            cargo_tuple_list = []
            cargo = ship['cargo']['inventory']
            for item in cargo:
                cargo_tuple_list.append((item['symbol'], item['units']))

            my_ships_dict = {
                "symbol": ship["symbol"],
                "role": ship["registration"]["role"],
                "nav_location": ship["nav"]["systemSymbol"],
                "nav_waypoint_location": ship["nav"]["waypointSymbol"],
                "nav_status": ship["nav"]["status"],
                "nav_flight_mode": ship["nav"]["flightMode"],
                "current_fuel": ship["fuel"]["current"],
                "capacity_fuel": ship["fuel"]["capacity"],
                # this gets weird with zero cases
                # 'pct_fuel': ship['fuel']['current'] / ship['fuel']['capacity'], #maybe make this an int idk
                "current_cargo": cargo_tuple_list,
                "capacity_cargo": ship["cargo"]["capacity"],
                # 'pct_cargo':len(ship['cargo']['inventory']) / ship['cargo']['capacity']
            }
            bigger_dict[
                i
            ] = my_ships_dict  # this feels clunky, but maybe i can just dump it into a dataclass obj?
            i += 1

        # mounts, crew might need some logic since they could be empty

        return bigger_dict


# raw_ships_data = get_ships_list(raw=True)

# maybe this is what that first method should return? wait, it is what it returns,
# there are just parameters that i likely will never use
raw_ships_dict = get_ships_list(ship_dict=True)


# ultimately a dict might not be ideal, i'm imagining lists of objects based on state, which might also not be ideal idk

#TODO it might eventually be worth it to have ship just be a class-- the main benefits of a dataclass are reducing
#boilerplate, but i might actually want to customize some of that stuff
@dataclass()
class Ship:
    symbol: str
    role: str
    nav_location: str  # probably should be an object type
    nav_waypoint_location: str
    nav_status: str
    nav_flight_mode: str
    current_fuel: int
    capacity_fuel: int
    current_cargo: list[tuple]

    capacity_cargo: int

    systems_in_jumpgate_range: dict | None = None

    # this makes sense, but i need to change the functions to accept a lookup from an individual ship location
    # it will work for now because there are two ships in the same system
    #

    # def __post_init__(self):
    #     if self.systems_in_jumpgate_range is None:
    #         self.systems_in_jumpgate_range = get_current_connected_systems()
    def __refuel_ship(self):
        _refuel = RefuelShipJsonBody()
        refuel_ship.sync_detailed(self.symbol, json_body=_refuel, client=client)
        print(self.current_fuel)

    def _orbit_current_waypoint(self):
        print(f"orbiting {self.nav_waypoint_location}")
        orbit_ship.sync_detailed(self.symbol, client=client)

    def nav_ship(self, waypoint):
        if self.nav_status == "DOCKED":
            print("undocking")
            self._orbit_current_waypoint()
        #TODO this needs to check for fuel
        #TODO this also needs to handle/return the information that navigate_ship gives you as far as dest, travel time, etc
        _nav_ship = NavigateShipJsonBody(waypoint)
        nav_results = navigate_ship.sync_detailed(self.symbol, json_body=_nav_ship, client=client)
        print(nav_results)


    # toDO i think this makes sense for how to handle get_market
    def get_market_from_ship_waypoint(self, nav_location):
        pass

    def get_ship_cargo(self):
        #TODO this throws an unhandled response error if ship cargo is empty? it might be a rate limit error
        new_cargo = data_decode(get_my_ship_cargo.sync_detailed(self.symbol, client=client).content)
        #TODO fixed_cargo needs a better name
        fixed_cargo = []
        # cargo_sum = 0
        for item in new_cargo['inventory']:
            # cargo_sum += cargo_sum + item["units"]
            fixed_cargo.append((item["symbol"], item["units"]))
        self.current_cargo = fixed_cargo

        return fixed_cargo

    # def get_systems_in_jumpgate_range(self):
    #     if self.systems_in_jumpgate_range is None:
    #         self.systems_in_jumpgate_range = current_connected_systems
    def set_systems_in_jumpgate_range(self, systems_in_jumpgate_range: dict):
        """
        just a quick set method to add current systems in jumpgate range

        :param systems_in_jumpgate_range:
        :return:
        """
        self.systems_in_jumpgate_range = systems_in_jumpgate_range

    def get_ship_system_waypoints(self):
        raw_system_waypoints = data_decode(get_system_waypoints.sync_detailed(self.nav_location, client=client).content)
        clean_system_waypoint_list = []
        # print(raw_system_waypoints)
        waypoint_dict = {}
        dict_index = 0
        for waypoint in raw_system_waypoints:
            waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type']]
            for trait in waypoint['traits']:
                if trait['symbol'] == "MARKETPLACE" or trait['symbol'] == "SHIPYARD" or trait['symbol'] == "JUMP_GATE":
                    waypoint_dict[dict_index] = [waypoint['symbol'], waypoint['type'], trait['symbol']]

            print(waypoint['traits'])
            dict_index += 1
        #TODO - okay, i need to add more details about the features of each waypoint
            # print(waypoint['symbol'], waypoint['type'])
        # pp.pprint(waypoint_dict.items())
        pp.pprint(waypoint_dict)
        return waypoint_dict

def create_ship_object_dict(raw_ships_dict: dict) -> dict[int:Ship]:
    """

    :param raw_ships_dict: uses the dict values to create a dataclass
    :return: a dict [int(0:n of ships) : ship object
    """
    ship_dict = {}
    for i in range(len(raw_ships_dict)):

        ship_dict[i] = Ship(*raw_ships_dict[i].values())
    return ship_dict


ship_dict = create_ship_object_dict(raw_ships_dict)
# pp.pprint(ship_dict)
#
# print(ship_dict[1].nav_status)
# print("number of ships:", len(ship_dict.keys()))
# print('number of docked ships:', DOCKED' in ship_dict.values()))

# okay this works for passing objects into flask
ship_list = []
for ship in ship_dict.values():
    ship_list.append(ship)
    # print(ship)

# print(ship_list[0].systems_in_jumpgate_range)
