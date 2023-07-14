from client import client
from get_ships_list import ship_list, Ship
from data_decode import data_decode

from space_traders_api_client.api.fleet import extract_resources, sell_cargo, dock_ship, orbit_ship
from space_traders_api_client.models import SellCargoSellCargoRequest
from space_traders_api_client.models import ExtractResourcesJsonBody

running = True

def print_list_of_ships():
    ship_id = 0
    for ship in ship_list:
        print("id:", ship_id, '|', ship.symbol, ship.role, '\t', ship.nav_location, ship.nav_waypoint_location,
              ship.nav_status)
        ship_id += 1

def choose_ship():
    print("select a ship by id")
    ship_selection = int(input())
    print(ship_list[ship_selection])
    return ship_selection


print_list_of_ships()
ship_selection = choose_ship()

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
          "z. quit")
    action_selection = input()
    match action_selection:
        case '1':
            print_list_of_ships()
            choose_ship()
        case 'a':
            print("orbiting")
            orbit_ship.sync_detailed(ship_list[ship_selection].symbol, client=client)
            pass
        case 'b':
            print("docking")
            dock_ship.sync_detailed(ship_list[ship_selection].symbol, client=client)
        case 'c':
            current_waypoint_dict = ship_list[ship_selection].get_ship_system_waypoints()
            # print('\n', '\t', ship_list[ship_selection].get_ship_system_waypoints())
            print("select waypoint:")
            waypoint_selection = int(input())
            print(current_waypoint_dict[waypoint_selection][0])
            waypoint = current_waypoint_dict[waypoint_selection][0]
            ship_list[ship_selection].nav_ship(waypoint)

        case 'z':

            running = False


"""
THIS IS THE SUCCESSFUL NAV RETURN-- need to grab the relevant info out of it 

Response(status_code=<HTTPStatus.OK: 200>, content=b'{"data":{"nav":{"systemSymbol":"X1-MP2","waypointSymbol":"X1-MP2-50435D","route":{"departure":{"symbol":"X1-MP2-12220Z","type":"PLANET","systemSymbol":"X1-MP2","x":7,"y":25},"destination":{"symbol":"X1-MP2-50435D","type":"ASTEROID_FIELD","systemSymbol":"X1-MP2","x":-5,"y":-40},"arrival":"2023-07-12T23:10:33.168Z","departureTime":"2023-07-12T23:09:45.168Z"},"status":"IN_TRANSIT","flightMode":"CRUISE"},"fuel":{"current":1134,"capacity":1200,"consumed":{"amount":66,"timestamp":"2023-07-12T23:09:45.179Z"}}}}', headers=Headers({'x-powered-by': 'Express', 'access-control-allow-origin': '*', 'access-control-expose-headers': 'Retry-After, X-RateLimit-Type, X-RateLimit-Limit-Burst, X-RateLimit-Limit-Per-Second, X-RateLimit-Remaining, X-RateLimit-Reset', 'retry-after': '1', 'x-ratelimit-type': 'IP Address', 'x-ratelimit-limit-burst': '10', 'x-ratelimit-limit-per-second': '2', 'x-ratelimit-remaining': '0', 'x-ratelimit-reset': '2023-07-12T23:09:45.964Z', 'content-type': 'application/json; charset=utf-8', 'etag': 'W/"1fd-Gg+Pd7LEitdyNamTxWdahOOAKl0"', 'x-cloud-trace-context': '98ce029b892ad23f00e34a50b1a87a1f', 'date': 'Wed, 12 Jul 2023 23:09:45 GMT', 'server': 'Google Frontend', 'content-length': '509', 'via': '1.1 google, 1.1 google', 'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'}), parsed=NavigateShipResponse200(data=NavigateShipResponse200Data(fuel=ShipFuel(current=1134, capacity=1200, consumed=ShipFuelConsumed(amount=66, timestamp=datetime.datetime(2023, 7, 12, 23, 9, 45, 179000, tzinfo=tzutc()), additional_properties={}), additional_properties={}), nav=ShipNav(system_symbol='X1-MP2', waypoint_symbol='X1-MP2-50435D', route=ShipNavRoute(destination=ShipNavRouteWaypoint(symbol='X1-MP2-50435D', type=<WaypointType.ASTEROID_FIELD: 'ASTEROID_FIELD'>, system_symbol='X1-MP2', x=-5, y=-40, additional_properties={}), departure=ShipNavRouteWaypoint(symbol='X1-MP2-12220Z', type=<WaypointType.PLANET: 'PLANET'>, system_symbol='X1-MP2', x=7, y=25, additional_properties={}), departure_time=datetime.datetime(2023, 7, 12, 23, 9, 45, 168000, tzinfo=tzutc()), arrival=datetime.datetime(2023, 7, 12, 23, 10, 33, 168000, tzinfo=tzutc()), additional_properties={}), status=<ShipNavStatus.IN_TRANSIT: 'IN_TRANSIT'>, flight_mode=<ShipNavFlightMode.CRUISE: 'CRUISE'>, additional_properties={}), additional_properties={}), additional_properties={}))

Process finished with exit code 0


"""