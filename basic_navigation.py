import get_ships
from client import client
from current_systems_jumpgate_map import get_current_connected_systems
from get_ships import ship_list, Ship
from mining_ships import mining_ship_list
from data_decode import data_decode

from update_market_data import update_market_data
# from current_systems_jumpgate_map import get_current_connected_systems
from space_traders_api_client.api.fleet import extract_resources, sell_cargo, dock_ship, orbit_ship, jump_ship
from space_traders_api_client.models import SellCargoSellCargoRequest, JumpShipJsonBody
from space_traders_api_client.models import ExtractResourcesJsonBody
from log_status_code import log_status_code

running = True


def print_list_of_ships():
    ship_id = 0
    for ship in ship_list:
        print("id:", ship_id, '|', ship.symbol, ship.role, '\t', ship.nav_location, ship.nav_waypoint_location,
              ship.nav_status, ship.nav_flight_mode)
        ship_id += 1


def choose_ship():
    print("select a ship by id")
    ship_selection = int(input())
    print(ship_list[ship_selection])
    return ship_selection


print_list_of_ships()
ship_selection = choose_ship()

#TODO i'd like a cooldown status check whenever it returns to the root menu

while running:
    # ship_id = 0
    # for ship in ship_list:
    #     print("id:", ship_id, '|', ship.symbol, ship.role, '\t', ship.nav_location, ship.nav_waypoint_location,
    #           ship.nav_status)
    #     ship_id += 1

    # print("select a ship by id")
    # ship_selection = int(input())
    # print(ship_list[ship_selection])

    print("actions:", '\n \t',
          "1. choose different ship \n\t",
          "a. orbit/undock", '\n \t',
          "b. dock", '\n \t',
          "c. nav", '\n\t',
          "d. waypoint action\n\t"
          "e. check cargo\n\t"
          "z. quit")
    action_selection = input()
    match action_selection:
        case '1':
            print_list_of_ships()
            choose_ship()
        case 'a':

            ship_list[ship_selection].orbit_current_waypoint()
            # print("orbiting")
            # todo update these to use the ship class methods instead of the api call even though it's the same thing it just feels like there should be some consistency

            # orbit_ship.sync_detailed(ship_list[ship_selection].symbol, client=client)
            pass
        case 'b':

            ship_list[ship_selection].dock()
            # dock_ship.sync_detailed(ship_list[ship_selection].symbol, client=client)
            # todo check fuel level before refueling automatically
            # ship_list[ship_selection].refuel_ship()

        case 'c':
            current_waypoint_dict = ship_list[ship_selection].get_ship_system_waypoints()
            # print('\n', '\t', ship_list[ship_selection].get_ship_system_waypoints())
            # print(current_waypoint_dict.items())
            for waypoint in current_waypoint_dict.items():
                print(waypoint)

            print("select waypoint:")
            waypoint_selection = int(input())
            print(current_waypoint_dict[waypoint_selection][0])
            waypoint = current_waypoint_dict[waypoint_selection][0]
            ship_list[ship_selection].nav_ship(waypoint)

        case 'd':
            # this should be a nested match case
            print("a. extract resources")
            print("b. sell junk")

            print("c. update market data")

            # need some logic around waypoint is jumpgate
            print("d. jumpgate")
            print("e. sell all")
            print("f. survey")
            print("g. mine from survey")
            mining_action_selection = input()
            match mining_action_selection:
                case "a":
                    # todo need a better way of choosing a mining ship
                    mining_ship_list[0].mine()
                    # ship_list[ship_selection].mining_ship.mine()
                case "b":
                    print("selling junk")
                    mining_ship_list[0].sell_junk()

                case "c":
                    update_market_data()

                case "d":
                    # todo move all of this to a method and import it
                    current_systems = get_current_connected_systems()
                    dict_index = 0
                    jump_targets = {}
                    # todo i think this is weirding out and duplicating items + getting other values that aren't valid40
                    for i, v in enumerate(current_systems.values()):
                        for system in v:
                            jump_targets[dict_index] = system
                            dict_index += 1
                    for item in jump_targets.items():
                        print(item)
                    jump_gate_choice = input()
                    jump_ship_json = JumpShipJsonBody(jump_targets[int(jump_gate_choice)])
                    jump_results = jump_ship.sync_detailed(ship_symbol=ship_list[ship_selection].symbol,
                                                           json_body=jump_ship_json, client=client)
                    print(jump_results)
                    jump_targets.clear()
                    current_systems.clear()
                    # to do this needs to set the ship.system_waypoint to the jump gate waypoint in the target system
                    # get_ships.get_ships_list()
                    # print(current_systems)
                # this needs to go somewhere
                # if ship_list[ship_selection] in mining_ship_list:
                #     #todo need an if for waypoint features
                #     pass
                case "e":
                    mining_ship_list[0].sell_junk(sell_all=True)
                case "f":
                    mining_ship_list[0].survey()
                case "g":
                    mining_ship_list[0].mine_from_survey()
        case 'e':
            ship_list[ship_selection].check_cargo()
        case 'z':

            running = False

"""
THIS IS THE SUCCESSFUL NAV RETURN-- need to grab the relevant info out of it 

Response(status_code=<HTTPStatus.OK: 200>, content=b'{"data":{"nav":{"systemSymbol":"X1-MP2","waypointSymbol":"X1-MP2-50435D","route":{"departure":{"symbol":"X1-MP2-12220Z","type":"PLANET","systemSymbol":"X1-MP2","x":7,"y":25},"destination":{"symbol":"X1-MP2-50435D","type":"ASTEROID_FIELD","systemSymbol":"X1-MP2","x":-5,"y":-40},"arrival":"2023-07-12T23:10:33.168Z","departureTime":"2023-07-12T23:09:45.168Z"},"status":"IN_TRANSIT","flightMode":"CRUISE"},"fuel":{"current":1134,"capacity":1200,"consumed":{"amount":66,"timestamp":"2023-07-12T23:09:45.179Z"}}}}', headers=Headers({'x-powered-by': 'Express', 'access-control-allow-origin': '*', 'access-control-expose-headers': 'Retry-After, X-RateLimit-Type, X-RateLimit-Limit-Burst, X-RateLimit-Limit-Per-Second, X-RateLimit-Remaining, X-RateLimit-Reset', 'retry-after': '1', 'x-ratelimit-type': 'IP Address', 'x-ratelimit-limit-burst': '10', 'x-ratelimit-limit-per-second': '2', 'x-ratelimit-remaining': '0', 'x-ratelimit-reset': '2023-07-12T23:09:45.964Z', 'content-type': 'application/json; charset=utf-8', 'etag': 'W/"1fd-Gg+Pd7LEitdyNamTxWdahOOAKl0"', 'x-cloud-trace-context': '98ce029b892ad23f00e34a50b1a87a1f', 'date': 'Wed, 12 Jul 2023 23:09:45 GMT', 'server': 'Google Frontend', 'content-length': '509', 'via': '1.1 google, 1.1 google', 'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'}), parsed=NavigateShipResponse200(data=NavigateShipResponse200Data(fuel=ShipFuel(current=1134, capacity=1200, consumed=ShipFuelConsumed(amount=66, timestamp=datetime.datetime(2023, 7, 12, 23, 9, 45, 179000, tzinfo=tzutc()), additional_properties={}), additional_properties={}), nav=ShipNav(system_symbol='X1-MP2', waypoint_symbol='X1-MP2-50435D', route=ShipNavRoute(destination=ShipNavRouteWaypoint(symbol='X1-MP2-50435D', type=<WaypointType.ASTEROID_FIELD: 'ASTEROID_FIELD'>, system_symbol='X1-MP2', x=-5, y=-40, additional_properties={}), departure=ShipNavRouteWaypoint(symbol='X1-MP2-12220Z', type=<WaypointType.PLANET: 'PLANET'>, system_symbol='X1-MP2', x=7, y=25, additional_properties={}), departure_time=datetime.datetime(2023, 7, 12, 23, 9, 45, 168000, tzinfo=tzutc()), arrival=datetime.datetime(2023, 7, 12, 23, 10, 33, 168000, tzinfo=tzutc()), additional_properties={}), status=<ShipNavStatus.IN_TRANSIT: 'IN_TRANSIT'>, flight_mode=<ShipNavFlightMode.CRUISE: 'CRUISE'>, additional_properties={}), additional_properties={}), additional_properties={}))

Process finished with exit code 0


"""
