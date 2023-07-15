import time
from client import client
from data_decode import data_decode
from SECRETS import sql_account, sql_pw
import sqlalchemy as sa
import pandas as pd


engine = sa.create_engine(f'postgresql://{sql_account}:{sql_pw}@localhost:5432/spacetraders')


def append_df_to_sql_table(df: pd.DataFrame, table_name: str, engine=engine):
    df.to_sql(table_name, engine, if_exists="append")




#maybe some postgresql -> df methods?
df_test = pd.read_sql_query("SELECT * FROM player_wallet;", engine)
