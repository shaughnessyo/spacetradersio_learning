import time
from datetime import datetime
from client import client

from data_decode import data_decode

from space_traders_api_client.api.agents import get_my_agent
from SECRETS import sql_account, sql_pw
import sqlalchemy as sa
import pandas as pd

engine = sa.create_engine(f'postgresql://{sql_account}:{sql_pw}@localhost:5432/spacetraders')

import pandas as pd


# df = pd.read_csv("https://raw.githubusercontent.com/kirenz/datasets/master/gapminder.csv")


def get_player_credits() -> int:
    player_info = data_decode(get_my_agent.sync_detailed(client=client).content)
    player_credits = player_info['credits']
    return player_credits


def player_credits_to_df(player_credits:int) -> pd.DataFrame:
    df = pd.DataFrame({"credits":player_credits, "tm": datetime.now()},index=[0])
    return df


#TODO you should just make a general df to sql method for however many cases there are-- it seems like if_exists="append" covers a lot of them but there might be others
def wallet_df_to_sql(table_name: str, engine=engine):
    player_credits = get_player_credits()
    df = player_credits_to_df(player_credits)
    df.to_sql(table_name, engine, if_exists="append")


# wallet_df_to_sql("player_wallet")



# i thought making a simple class would make sense, but this is being weird
class PlayerWalletEntry:
    def __init__(self, player_credits, timestamp=datetime.now()):
        self.credits = player_credits
        self.timestamp = timestamp
        # self.wallet_list = ["credits", self.credits, "timestamp", self.timestamp]
        # self.wallet_dict = {"credits": int(self.credits),
        #                     "timestamp": str(self.timestamp)}
    # def __repr__(self):
    #     return self.credits, self.timestamp
    #
    # def __str__(self):
    #     return self.credits + self.timestamp


# def create_wallet_entry(player_credits):
#     wallet_entry = PlayerWalletEntry(player_credits)
#     return wallet_entry


# def player_wallet_to_df(wallet_entry: PlayerWalletEntry) -> pd.DataFrame:
#     # print(wallet_entry)
#     print(wallet_entry.credits)
#     # df = pd.DataFrame(data=wallet_entry.wallet_list, columns=['credits', 'timestamp'])
#     df = pd.DataFrame({"credits": int(wallet_entry.credits),
#                        "tm": str(wallet_entry.timestamp)}, index=[0])
#     # df['credits'] = wallet_entry.wallet_list[0]
#     # df['timestamp'] = wallet_entry.wallet_list[1]
#     return df

# def wallet_df_to_sql(table_name: str, engine=engine):
#     """
#     I NEED TO REWORK THIS ENTIRELY, THIS WAS JUST A FIRST TRY AT STORING BIZ IN A DB, but one weird thing that isn't
#     following what i would expect is that the timestamp isn't updating when wallet_entry is created
#
#     also, timestamp is being handled as a str in postgresql so that needs to be fixed
#
#     :param table_name:
#     :param engine:
#     :return:
#     """
#     player_credits = get_player_credits()
#     wallet_entry = create_wallet_entry(player_credits)
#     df = player_wallet_to_df(wallet_entry)
#     df.to_sql(table_name, engine, if_exists="append")





# wallet_df_to_sql("player_wallet")

# credits = get_player_credits()
# wallet_entry = create_wallet_entry(credits)
# # print(wallet_entry)
#
# df = player_wallet_to_df(wallet_entry)
# print(df)

# wallet_df_to_sql("player_wallet")
df_test = pd.read_sql_query("SELECT * FROM player_wallet;", engine)

print(df_test)
s = df_test['credits']
print(s.pct_change())
print(s.diff())