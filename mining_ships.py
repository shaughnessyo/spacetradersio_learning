from log_market_transaction import log_market_transaction
import datetime
from time import sleep

import arrow
import numpy as np
import pandas as pd
import sqlalchemy as sa

from SECRETS import sql_account, sql_pw
from client import client
from data_decode import data_decode, error_decode
from get_ships import ship_list, Ship
from log_market_transaction import log_market_transaction
from space_traders_api_client.api.fleet import get_mounts, extract_resources, sell_cargo, create_survey
from space_traders_api_client.models import ExtractResourcesJsonBody, SellCargoSellCargoRequest
# todo if i'm going to use the Survey object here, i might as well use it for sql parts
from space_traders_api_client.models import Survey
from space_traders_api_client.models.survey_deposit import SurveyDeposit
from space_traders_api_client.models.survey_size import SurveySize

engine = sa.create_engine(f"postgresql://{sql_account}:{sql_pw}@localhost:5432/spacetraders")

# engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')


# print(ship, mount['symbol'])

# mnt_test = mounts[0]['symbol']
# print(mnt_test)
# if "MINING" in mnt_test:
#     print("mining ship")


class MiningShip:
    def __init__(self, ship: Ship):
        self.ship = ship

    def mine(self):
        """
        it might make more sense for this to incorporate an argument to handle survey results, but i don't know how
        weird dealing with surveys is going to be, so i'm going to do it separately at least at first

        :return:
        """

        ext_res = ExtractResourcesJsonBody()
        response = extract_resources.sync_detailed(self.ship.symbol, json_body=ext_res, client=client)
        if response.status_code in [200, 201]:
            print('mining')

            # todo just extract cooldown and inventory from the successful codes
            # print(data_decode(response.content))
            extract_return = data_decode(response.content)
            print(
                f"{extract_return['extraction']['shipSymbol']} mined {extract_return['extraction']['yield']['units']} "
                f"units of {extract_return['extraction']['yield']['symbol']}")
            print(f"cooldown: {extract_return['cooldown']['totalSeconds']} seconds")
            self.ship.update_current_cargo()
            print(f"total cargo: {self.ship.cargo_current}")
        if response.status_code not in [200, 201]:
            error_response = error_decode(response.content)
            print(error_response)
            # print(r_status_code)

    def survey(self):

        response = create_survey.sync_detailed(self.ship.symbol, client=client)
        if response.status_code in [200, 201]:
            print("surveying")
            create_survey_response = data_decode(response.content)
            # print(create_survey_response)
            # print(create_survey_response['surveys'][0]['signature'])
            # print(create_survey_response['surveys'][0]['symbol'])
            # print(create_survey_response['surveys'][0]['deposits'])
            # print(create_survey_response['surveys'][0]['size'])
            survey_signature = create_survey_response['surveys'][0]['signature']
            survey_symbol = create_survey_response['surveys'][0]['symbol']
            raw_deposits = create_survey_response['surveys'][0]['deposits']
            deposit_list = []

            for deposit in raw_deposits:
                # print(deposit['symbol'])
                deposit_list.append(deposit['symbol'])
            for item in deposit_list:
                print(item)
            expiration = create_survey_response['surveys'][0]['expiration']
            size = create_survey_response['surveys'][0]['size']
            print(survey_signature, deposit_list, expiration, size)
            # todo apparently storing a list like this is bad database normalization practice-- it should be a
            # parent-child table linked by a foreign key, but for now WHO CARE

            from data_to_sql import survey_results_to_sql_peewee

            time_stamp = arrow.utcnow()
            survey_results_to_sql_peewee(signature=survey_signature,waypoint_symbol=survey_symbol,
                                         expiration=expiration,size=size,time_stamp=time_stamp.datetime,
                                         survey_deposits=deposit_list)

            # survey_results_to_sql(signature=survey_signature, waypoint_symbol=survey_symbol,
            #                       deposits=deposit_list, expiration=expiration, size=size)

            # print(create_survey_response['surveys']['signature'])
            # print(create_survey_response['surveys']['symbol'])
            # print(create_survey_response['surveys']["deposits"])
            # deposit_list = []
            # for deposit in create_survey_response['surveys']["deposits"]:
            #     deposit_list.append(deposit['symbol'])
            # print(deposit_list)
            # print(create_survey_response['surveys']["deposits"]['expiration'])

            # data_to_sql.survey_results_to_sql()
        else:
            error_response = error_decode(response.content)
            print(error_response)
        pass


    def mine_from_survey_peewee(self):

        from peewee_models import SurveyResult
        survey_results = SurveyResult.select()
        # print(survey_results)
        # print(survey_results.columns())
        for result in survey_results:
            print(result.id, result.waypoint_symbol, result.deposits)
        pass


    def mine_from_survey(self):
        """
        this is going to need to check for viable survey results, so i'm thinking MiningShip.survey stores the
        survey result in postgresql and this pulls the table and narrows it down to survey results at the current
        waypoint that haven't expired, then gives you a choice of them? or it could be weighted by results or time
        before expiration

        okay this should grab the table and parse it

        :return:
        """
        # so i could either grab them as a dataframe or extract them with sql, which could make some of the sorting easier?

        df_test = pd.read_sql("survey_results", engine)
        # df_print_full(df_test)

        # it probably makes sense to sort by expiration first and i need some way of culling expired ones?

        # print(df_test['signature'].loc[[0]])

        now = datetime.datetime.now()
        today = datetime.datetime.today()
        arrow_now = arrow.utcnow()
        # print(arrow_now, type(arrow_now))
        # print(now, type(now))
        # print(today, type(today))
        df_test['expiration_dt'] = pd.to_datetime(df_test['expiration'])
        # print(df_test.where(df_test['expiration_dt'] > arrow_now.datetime))
        # print(df_test.mask(df_test['expiration_dt'] < arrow_now.datetime))
        # df_print_full(df_test['expiration_dt'])

        df_test = df_test.mask(df_test['expiration_dt'] < arrow_now.datetime)
        df_test = df_test.replace('nan', np.nan)
        df_test = df_test.dropna()

        # print(df_test.transpose())
        # print(df_test['id'], df_test['signature'],)
        # print(df_test['deposits'],df_test['size'],df_test['expiration'])

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(df_test)

        dict_test = df_test.to_dict()

        # this might have problems because the df could have more than one value for it so it will probably need to be
        # narrowed down before trying to select specific values or use loc to select the narrowed down single row

        # pretend whatever business logic has pared down the df to a best row or rows and take the top one

        ###TODO this needs a check that there is a valid nonexpired survey regardless of its value
        #todo short term it would probably make more sense to be able to choose a survey
        # maybe also swap this out for the psycopg2 sql query since it seems to be a bit cleaner

        # def choose_survey()
        best_survey = df_test.tail(1)
        svy_signature = best_survey['signature'].to_numpy()[0]

        svy_waypoint_symbol = best_survey['waypoint_symbol'].to_numpy()[0]



        deposits_from_sql = best_survey['deposits'].values.tolist()
        # print(deposits_from_sql[0].replace('{', '[').replace('}', ']'))

        # deposits_from_sql = deposits_from_sql[0].replace('{','[').replace('}',']')
        #TODO this needs ot be updated to match the new sql query biz
        deposits_from_sql = deposits_from_sql[0].replace('{', '').replace('}', '')
        deposits_from_sql = deposits_from_sql.split(',')

        # print(deposits_from_sql)
        deposit_list = []

        for item in deposits_from_sql:
            deposit_obj = SurveyDeposit(item)
            deposit_list.append(deposit_obj)

        svy_expiration = arrow.get(best_survey['expiration'].to_numpy()[0])

        # print(best_survey['size'].to_numpy())
        size = best_survey['size'].to_numpy()[0]
        svy_size = SurveySize(size)



        # signature: str
        # symbol: str
        # deposits: List["SurveyDeposit"]
        # expiration: datetime.datetime
        # size: SurveySize

        #not 100% sure that this is going to work-- might have to specifically grab the single value
        survey_obj = Survey(signature=svy_signature,
                            symbol=svy_waypoint_symbol,
                            deposits=deposit_list,
                            expiration=svy_expiration.datetime,
                            size=svy_size)

        # mining_survey = MiningSurvey(df_test['signature'], df_test['waypoint_symbol'], df_test['deposits'],
        #                              df_test['expiration'], df_test['size'])

        # print(mining_survey)

        """
        okay, need to create a survey object of currently valid biz weighted by value, pass it to extract_resources,
        and mine it 
        
        """

        # df_print_full(df_test)
        # survey_results = SurveyResults(signature=signature, waypoint_symbol=waypoint_symbol, deposits=deposits,
        #                                expiration=expiration, size=size)
        # Survey
        ext_res = ExtractResourcesJsonBody(survey_obj)
        response = extract_resources.sync_detailed(self.ship.symbol, json_body=ext_res, client=client)


        if response.status_code in [200, 201]:
            print("mining from survey")
            # create_survey_response = data_decode(response.content)
            extract_return = data_decode(response.content)
            print(
                f"{extract_return['extraction']['shipSymbol']} mined {extract_return['extraction']['yield']['units']} "
                f"units of {extract_return['extraction']['yield']['symbol']}")
            print(f"cooldown: {extract_return['cooldown']['totalSeconds']} seconds")
            self.ship.update_current_cargo()
        else:
            error_response = error_decode(response.content)
            print(error_response)
        pass

    def sell_junk(self, sell_all=False):

        # for this to work, i need to hit the api call for this specific ship's cargo and update it before it tries to sell
        # TODO this should maybe be a ship method though trading logic will probably be more complicated so maybe not
        sell_list = []
        self.ship.update_current_cargo()
        for item in self.ship.cargo_current:
            # print(item, item[0])
            # print(item[0], item[0] not in ["IRON_ORE", "COPPER_ORE", "ALUMINUM_ORE"])
            # todo this will need to be expanded beyond starting system ores
            if sell_all is False:
                if item[0] not in ["IRON_ORE", "COPPER_ORE", "ALUMINUM_ORE"]:
                    sell_list.append((item[0], item[1]))

                else:
                    continue
            if sell_all is True:
                sell_list.append((item[0], item[1]))
        print(sell_list)
        while sell_list:
            sale_item = sell_list.pop()
            sc = SellCargoSellCargoRequest(sale_item[0], sale_item[1])
            response = sell_cargo.sync_detailed(self.ship.symbol, json_body=sc, client=client)
            if response.status_code in [200, 201]:
                # todo just extract cooldown and inventory from the successful codes
                # print(data_decode(response.content))
                decode_response = data_decode(response.content)

                print(decode_response)
                credits = decode_response['agent']['credits']

                waypoint_symbol = decode_response['transaction']['waypointSymbol']
                ship_symbol = decode_response['transaction']['shipSymbol']
                trade_symbol = decode_response['transaction']['tradeSymbol']
                market_interaction_type = decode_response['transaction']['type']
                units = decode_response['transaction']['units']
                price_per_unit = decode_response['transaction']['pricePerUnit']
                total_price = decode_response['transaction']['totalPrice']
                # print(credits)
                # print(waypoint_symbol)

                log_market_transaction(
                    credits,
                    waypoint_symbol,
                    ship_symbol,
                    trade_symbol,
                    market_interaction_type,
                    units,
                    price_per_unit,
                    total_price)

            if response.status_code not in [200, 201]:
                error_response = error_decode(response.content)
                print(error_response)
            # print(response)
            # print(decode_response)
            # agent = decode_response['agent']
            # cargo = decode_response['cargo']
            # transaction = decode_response['transaction']
            # sell_cargo_response = SellCargoSellCargo201ResponseData(agent, cargo, transaction)

            # todo fuck it, i'll just grab the values i need, but should revisit this when i have less of a headache

            sleep(.5)
        pass


def build_mining_ship_list(ship_list: list[Ship]) -> list[MiningShip]:
    mining_mount = []
    for ship in ship_list:

        response = get_mounts.sync_detailed(ship.symbol, client=client)
        mounts = data_decode(response.content)
        for mount in mounts:
            if "MINING" in mount['symbol']:
                # print("mining", ship)
                mining_mount.append(ship)
    mining_ship_list = []
    for ship in mining_mount:
        mining_ship = MiningShip(ship)
        mining_ship_list.append(mining_ship)
    return mining_ship_list


mining_ship_list = build_mining_ship_list(ship_list)

for mining_ship in mining_ship_list:
    print(mining_ship.ship.symbol)

# def check_mining_ship_membership()


# TODO this should be stored in the database and only looked up from the api when something changes
