import asyncio
import time

from client import client
from get_ships_list import ship_list, Ship
from data_decode import data_decode

from time import sleep
import random
from enum import Enum, unique, Flag
from transitions import Machine

from space_traders_api_client.api.agents import get_my_agent
from space_traders_api_client.api.fleet import extract_resources, sell_cargo, dock_ship, orbit_ship
from space_traders_api_client.models import SellCargoSellCargoRequest
from space_traders_api_client.models import ExtractResourcesJsonBody

from get_player_credits import wallet_df_to_sql
import duckdb
import pandas as pd

# con = duckdb.connect("file.db")
# # con.sql("CREATE TABLE IF NOT EXISTS wallet FROM df_market_data")
# # df_income = pd.DataFrame()
#
player_info = data_decode(get_my_agent.sync_detailed(client=client).content)
# df_income = pd.DataFrame()
# df_income['credits'] = player_info['credits']
# df_income['time_stamp'] = pd.Timestamp.now()
#
# df = duckdb.sql("SELECT * FROM market_data;").df()
# print(df.dtypes)
#
# # print(con.sql("SHOW TABLES"))
# # print(con_tables)
# # con.sql("CREATE TABLE IF NOT EXISTS wallet FROM df_income")
#
# con.sql("INSERT INTO wallet SELECT * FROM df_income")

# income_list = [player_info['credits'], time.clock_gettime()]

starting_credits = player_info['credits']

mining_ship_list = []
excavator_system_waypoint_list = []
for ship in ship_list:
    print(ship.symbol, ship.role)
    if ship.role == "EXCAVATOR":
        mining_ship_list.append(ship)

print(mining_ship_list[0])


# print(mining_ship_list[0].current_cargo)
# for item in mining_ship_list[0].current_cargo:
#     print(item)


# class MiningResults:
#     def __init__(self):
#         self.name = random.choice(['iron', 'copper', 'soy', 'baby_teeth'])
#         self.units = random.randint(1, 10)


class Miner(Ship):
    states = ['orbit', 'mine', 'dock', 'sell']

    transitions = [

        {'trigger': "begin_mine", "source": 'orbit', "dest": "mine"},
        {'trigger': 'begin_dock', 'source': 'mine', 'dest': 'dock'},
        {'trigger': 'begin_sell', 'source': 'dock', 'dest': 'sell'},
        {'trigger': 'begin_orbit', 'source': 'sell', 'dest': 'orbit'}

    ]

    def __init__(self, ship_obj: Ship):
        """
        #TODO CLEAN THIS UP NOW THAT IT PROPERLY INHERITS SHIP
        :param ship_obj:
        """
        self.Ship = ship_obj
        self.cargo_max = self.Ship.capacity_cargo
        self.cargo = []
        # self.docked = False
        # self.orbiting = True
        self.cargo_full = False
        self.machine = Machine(model=self, states=Miner.states, transitions=Miner.transitions, initial='orbit')
        self.running = True
        self.money = 0

    def check_cargo(self):
        """
        rework this to transition at like 90% or whatever, so i lose fewer cycles to filling the last little bit
        :return:
        """
        self.Ship.get_ship_cargo()
        cargo_sum = 0
        for item in self.Ship.current_cargo:
            cargo_sum += item[1]
        if cargo_sum < self.cargo_max:
            self.cargo_full = False
        elif cargo_sum >= self.cargo_max:
            self.cargo_full = True
        return self.cargo_full

    def cargo_pct(self):
        """
        this needs to take over as the flag for when it's time to sell like if there's <5 units of storage left

        :return:
        """
        cargo_sum = 0
        for item in self.Ship.current_cargo:
            # print(item[1])
            cargo_sum = cargo_sum + item[1]
        print("current cargo units:", 60 - cargo_sum)
        return 60 - cargo_sum

    def _mine(self):
        """
        this might make more sense as a static method

        :return:
        """
        print('mining')

        ext_res = ExtractResourcesJsonBody()
        extract_resources.sync_detailed(self.Ship.symbol, json_body=ext_res, client=client)
        self.cargo = self.Ship.get_ship_cargo()

    def _dock(self):
        # okay let's do it for a single ship and worry about having Miner inherit Ship later
        print('docking')
        dock_ship.sync_detailed(self.Ship.symbol, client=client)

    def _orbit(self):
        print('orbiting')
        orbit_ship.sync_detailed(self.Ship.symbol, client=client)

    def _sell_junk(self):
        sell_list = []
        for item in self.Ship.current_cargo:
            # print(item, item[0])
            # print(item[0], item[0] not in ["IRON_ORE", "COPPER_ORE", "ALUMINUM_ORE"])
            if item[0] not in ["IRON_ORE", "COPPER_ORE", "ALUMINUM_ORE"]:
                sell_list.append((item[0], item[1]))
            else:
                continue
        print(sell_list)
        while sell_list:
            sale_item = sell_list.pop()
            sc = SellCargoSellCargoRequest(sale_item[0], sale_item[1])
            sell_cargo.sync_detailed(self.Ship.symbol, json_body=sc, client=client)
            sleep(.5)
        wallet_df_to_sql("player_wallet")

    def _sell(self):
        print('selling')
        player_info = data_decode(get_my_agent.sync_detailed(client=client).content)
        starting_credits = player_info['credits']
        # okay this is written for a ship object instance

        # print(self.current_cargo)
        # for item in self.current_cargo:
        #     print(item)

        """
        i need to be able to separate out cargo to sell these at way more at a nearby system:
        "IRON_ORE"
        "COPPER_ORE"
        "ALUMINUM_ORE"
        """

        for _ in range(len(self.Ship.current_cargo)):
            sale_item = self.Ship.current_cargo.pop()
            sc = SellCargoSellCargoRequest(sale_item[0], sale_item[1])

            sell_cargo.sync_detailed(self.Ship.symbol, json_body=sc, client=client)
            sleep(.5)
        wallet_df_to_sql("player_wallet")

        # i can either lookup locally, which could be good for later behavior
        # or just grab player credits and compare to starting credit value
        # cargo_values = {'iron': 10,
        #                 'copper': 8,
        #                 'soy': 3,
        #                 'baby_teeth': 15}
        # for item in self.cargo:
        #     current = self.cargo.pop()
        #     self.money += cargo_values[current[0]] * current[1]

    def state_manager(self):
        counter = 0
        while self.running:

            print(self.Ship.symbol, self.Ship.role)
            counter += 1
            print("cycle:", counter)

            match self.state:
                case 'orbit':
                    self._orbit()
                    self.begin_mine()
                    # self._mine()

                case 'mine':
                    print(self.cargo)
                    print(self.cargo_pct())
                    if self.cargo_pct() <= 10:
                    # if self.check_cargo() is True:
                        self.begin_dock()
                    else:
                        self._mine()

                        # mining_cooldown = 70

                        for i in range(70, 0, -10):
                            print(f"{i} seconds")
                            sleep(10)

                case 'dock':
                    self._dock()
                    self.begin_sell()
                case 'sell':
                    self._sell_junk()
                    self.begin_orbit()

            self.cargo = self.Ship.get_ship_cargo()
            if self.cargo:
                print(self.cargo)
            # print(self.money)

            if counter > 5000:
                self.running = False


# async def main():
#     await.asyncio.gather()
miner_dict = {0: Miner(ship_list[0]),
              1: Miner(ship_list[2])}


"""
no state manager needs to to be rewritten to handle more than one ship iteratively 

"""
for _miner in miner_dict.values():
    _miner.state_manager()
# miner = Miner(ship_list[2])
# miner2 = Miner(ship_list[0])
# miner.state_manager()
# miner2.state_manager()


# import multiprocessing
# p1 = multiprocessing.Process(target=miner.state_manager())
# p2 = multiprocessing.Process(target=miner2.state_manager())
#
# p1.start()
# p2.start()
