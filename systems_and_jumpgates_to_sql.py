from data_decode import data_decode, error_decode
from space_traders_api_client.api.systems import get_jump_gate
from client import client
import pickle
from time import sleep
from data_to_sql import system_waypoints_to_sql

with open("system_list.pickle", "rb") as f:
    full_system_list = pickle.load(f)

# print(full_system_list[0]['symbol'])


for system in full_system_list:
    # print(system)
    # if system['symbol'] == "X1-CJ75":
    for waypoint in system['waypoints']:
        # print(waypoint)
        #todo this is enough to store as a base table in postgresql
        # print(system['symbol'], waypoint['symbol'], waypoint['type'])
        system_symbol = system['symbol']
        jumpgate_list = []
        if waypoint['type'] == "JUMP_GATE":
            sleep(2)
            jump_gate_response = get_jump_gate.sync_detailed(system['symbol'], waypoint['symbol'], client=client)
            if jump_gate_response.status_code in [200, 201]:
                pass
            else:
                print(error_decode(jump_gate_response.content))

            jump_gate_response = data_decode(jump_gate_response.content)

            for jg in jump_gate_response['connectedSystems']:
                jumpgate_list.append(jg['symbol'])
            # print(system['symbol'],jump_gate_response['connectedSystems'])
        system_waypoints_to_sql(system_symbol=system_symbol, waypoint_symbol=waypoint['symbol'],
                                waypoint_type=waypoint['type'],jumpgate_list=jumpgate_list)
        print(system_symbol, waypoint['symbol'], waypoint['type'], jumpgate_list)