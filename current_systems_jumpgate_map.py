from client import client
from space_traders_api_client.api.systems import (
    get_jump_gate,
    get_system_waypoints,
)

from get_ships_list import ship_list, Ship

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from data_decode import data_decode
from time import sleep
import pickle

# i don't know that i need this here, but i went through the trouble of getting it
with open("system_list.pickle", "rb") as f:
    full_system_list = pickle.load(f)


# current location is a starting point, but it should be a list of all current non-traveling(?-- not sure what information is available about ships in transit) ship locations

# TODO this could actually be a dataclass method/methods to get jumpgates in the same system as a ship?

# todo it feels like maybe there should be a class or dataclass here and i'm not 100% sure that the way i'm organizing these methods makes sense

# todo yeah this should be somehow integrated into the ship dataclass i think?

# a class would make it easier to track state


class CurrentSystems:
    def __init__(self):
        pass


# def _get_current_locations(ship_list: list[Ship]=ship_list) -> list[Ship.nav_location]:
def _get_current_locations(ship_list: list) -> list:
    """
    get the locations of all of your ships from ship_list[Ship].nav_location and return them in a list
    :param ship_list:
    :return: current_ship_locations[system symbols as str]
    """
    current_ship_locations = []

    for ship in ship_list:
        current_ship_locations.append(ship.nav_location)
    return current_ship_locations


def _get_current_system_waypoints():
    """
    this one is going to need some different logic if it's getting multiple system waypoints from multiple current locations

    for the purposes of dealing with markets etc, this is going to need to keep track of each ship even if they are in
    the same system

    :return:
    """
    current_locations = _get_current_locations(ship_list)
    # print("current locations", current_locations)
    current_system_waypoints = {}
    for location in set(current_locations):
        # todo it would be nice to have proper rate limiting here, but worry about that later
        if len(current_locations) >= 10:
            sleep(0.5)
        system_waypoint_list = data_decode(
            get_system_waypoints.sync_detailed(location, client=client).content
        )
        # not sure about this, but give it a try
        current_system_waypoints[location] = system_waypoint_list

    return current_system_waypoints


def _get_current_jump_gate_list() -> list:
    """
    for now this just gets the waypoint names for any waypoint type == JUMP_GATE in current system waypoints

    :return:
    """
    current_system_waypoints = _get_current_system_waypoints()
    # print("current_system_waypoints", current_system_waypoints)
    jump_gate_list = []

    for waypoints in current_system_waypoints.values():
        for system in waypoints:
            # print("\n what's going on here \n", type(waypoint), "\n", waypoint[1])
            # print("does this denest it?", system["type"])
            if system["type"] == "JUMP_GATE":
                jump_gate_list.append(system["symbol"])

    return jump_gate_list


def _get_system_waypoint_tuple_list():
    """
    this currently works for  getting the system symbol out of the system waypoint symbol, though it might break on update since i don't know the full range of system name characteristics
    the get_jump_gate api call needs a tuple of current system symbol, current system jumpgate waypoint symbol

    :return: (current system symbol, current system jumpgate waypoint symbol) eg ('X1-MP2', 'X1-MP2-66939E')
    """

    current_jump_gate_list = _get_current_jump_gate_list()
    # print("current_jump_gate_list", current_jump_gate_list)
    system_waypoint_tuple_list = []

    for jump_gate in current_jump_gate_list:
        system_waypoint_tuple_list.append(
            (jump_gate.split("-")[0] + "-" + jump_gate.split("-")[1], jump_gate)
        )

    return system_waypoint_tuple_list


def get_current_connected_systems():
    """
    final api call to get the systems connected by jumpgate to current systems
    this should be able to check to see if systems are already in it and do nothing if they are, which probably will
    need to change some of the helper functions

    :return:
    """
    # get_current_connected_systems.has_been_called = True
    system_waypoint_tuple_list = _get_system_waypoint_tuple_list()
    # print("system_waypoint_tuple_list", system_waypoint_tuple_list)
    # jump_gate_results_list = []
    jump_gate_symbol_list = []
    connected_systems = {}
    counter = 0
    for pair in system_waypoint_tuple_list:
        # TODO another place for proper rate limiting
        if counter % 3 == 0:
            sleep(0.5)
        jump_gate_results = data_decode(
            get_jump_gate.sync_detailed(*pair, client=client).content
        )
        # this isn't currently getting used and likely never will
        # jump_gate_results_list.append(jump_gate_results)

        for item in jump_gate_results["connectedSystems"]:
            jump_gate_symbol_list.append(item["symbol"])
        connected_systems[
            pair[0]
        ] = jump_gate_symbol_list  # narrowed this down to system symbol, but will probably need xy coords at some point
        # print("\n", jump_gate_results["connectedSystems"])
        counter += 1
    # return jump_gate_symbol_list
    return connected_systems


# if get_current_connected_systems().

# try:
#     current_connected_systems
# except NameError:
#     print("Not in scope!")
# else:
#     print("In scope!")

current_connected_systems = get_current_connected_systems()

#TODO this should probably be by ship instance otherwise it will just be None
# Ship.systems_in_jumpgate_range = current_connected_systems

ship_list[0].set_systems_in_jumpgate_range(current_connected_systems)




# print(ship_list[0].systems_in_jumpgate_range)
# print(current_connected_systems)

for k, v in enumerate(current_connected_systems):
    print(v, current_connected_systems[v])

# todo maybe try to do it with plotly


"""

all of this should get cached and updated as it expands-- check if system is in keys or values?

"""

# G = nx.Graph(current_connected_systems)
# #
# # print(G.edges)
#
#
# nx.draw(G, with_labels=True, font_weight="bold")
# plt.show()

# fig = go.Figure(data=current_connected_systems)
#
# fig.show()
# fig = go.Figure(data=[edge_trace, node_trace],
#              layout=go.Layout(
#                 title='<br>Network graph made with Python',
#                 titlefont_size=16,
#                 showlegend=False,
#                 hovermode='closest',
#                 margin=dict(b=20,l=5,r=5,t=40),
#                 annotations=[ dict(
#                     text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
#                     showarrow=False,
#                     xref="paper", yref="paper",
#                     x=0.005, y=-0.002 ) ],
#                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#                 )
# fig.show()
