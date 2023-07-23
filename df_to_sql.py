import time
from client import client
from data_decode import data_decode
from SECRETS import sql_account, sql_pw
import sqlalchemy as sa
import pandas as pd
from typing import Literal

engine = sa.create_engine(f'postgresql://{sql_account}:{sql_pw}@localhost:5432/spacetraders')


def df_to_sql_table(df: pd.DataFrame, table_name: str, if_exists: Literal["fail", "replace", "append"], engine=engine):
    df.to_sql(table_name, engine, if_exists=if_exists)


def df_append_to_sql_table(df: pd.DataFrame, table_name: str, engine=engine):
    df.to_sql(table_name, engine, if_exists="append")


def df_replace_to_sql_table(df: pd.DataFrame, table_name: str, engine=engine):
    df.to_sql(table_name, engine, if_exists="replace")

# maybe some postgresql -> df methods?
# df_test = pd.read_sql_query("SELECT * FROM player_wallet;", engine)
