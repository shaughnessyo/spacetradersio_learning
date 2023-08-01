from space_traders_api_client.api.systems import (
    get_market,
    get_jump_gate,
    get_systems,
    get_system_waypoints,
)
from data_decode import data_decode
from time import sleep

import pickle
from client import client
import os
from os import listdir

"""
this needs to run every server reset because systems apparently aren't static?

"""

#TODO some qol feedback on this process would be nice, i can't remember how long it is supposed to take

def _depaginate_results(paginated_system_list: list[dict]) -> list[dict]:
    """

    just a cleaning step in _get_all_systems

    :param paginated_system_list: this is the paginated list returned by get_all_systems
    :return: just appending each system in each page of systems into a new unpaginated list
    """
    system_list = []

    for i in range(0, len(paginated_system_list) - 1):
        for system in paginated_system_list[i]:
            system_list.append(system)

    return system_list


def _get_all_systems(page: int = 1, limit: int = 20, client=client):
    """
    todo this seems ratelimited by plane wireless timing out


    this returns a list of all of the systems from get_systems
    there are 12k systems, pagination max is 20 per page, so 600 pages
    :param page: int 1-600
    :param limit: 20 max
    :param client: defined in shiplist

    :return:
    """
    full_systems_list = []
    # probably should be more granular than 100
    page_hundred = 100

    current_page = 0
    for i in range(0, 7):
        if os.path.isfile(f"system_list_{page_hundred}.pickle") is True:
            page = page_hundred
        page_hundred +=100
        # print(current_page)
        # print(os.path.isfile(f"system_list_{hundred}.pickle"))


    while page < 600:
        # i can't think through the math right now, so i'll just sleep every two pages
        if page % 2 == 0:
            sleep(0.5)
        get_systems_response = get_systems.sync_detailed(page=page, limit=20, client=client)
        #todo i really need to handle status codes generally
        if get_systems_response.status_code in [200, 201]:
            print(f"page {page} of 600, {page // 600}")
            pass
        else:
            print(get_systems_response)

        full_systems_list.append(data_decode(get_systems.sync_detailed(page=page, limit=20, client=client).content))
        if page == page_hundred:
            """
            this is jenky 
            """
            cleaned_hundred_pages = _depaginate_results(full_systems_list)
            with open(f"system_list_{page}.pickle", "wb") as f:
                pickle.dump(cleaned_hundred_pages, f)
                page_hundred += 100

        page += 1
    cleaned_systems_list = _depaginate_results(full_systems_list)

    return cleaned_systems_list


system_list_test = _get_all_systems()


print(len(system_list_test))
with open('system_list.pickle', 'wb') as f:
    pickle.dump(system_list_test, f)



# TODO to get the system list after it has been processed and also i should add a try except or conditional to see if
# # TODO the pickled system list exists before running this
# with open('system_list.pickle', 'rb') as f:
#     system_list = pickle.load(f)



# for system in system_list_test:
#     print(system['symbol'])


# print(system_list_test)

# system_list = []
#
# for i in range(0, len(system_list_test)-1):
#
#     for system in system_list_test[i]:
#         system_list.append(system)
#
# print(system_list)
#
