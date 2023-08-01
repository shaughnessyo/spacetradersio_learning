from playhouse.postgres_ext import ArrayField, PostgresqlExtDatabase
import peewee
import datetime
from peewee import *
from SECRETS import sql_account, sql_pw
import logging
import arrow

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

pg_db = PostgresqlExtDatabase('spacetraders',
                              user=sql_account,
                              password=sql_pw,
                              host='localhost',
                              port=5432)


# pg_db = peewee.PostgresqlDatabase('spacetraders',
#                                   user=sql_account,
#                                   password=sql_pw,
#                                   host='localhost',
#                                   port=5432)


class BaseModel(Model):
    class Meta:
        database = pg_db


class SurveyResult(BaseModel):
    signature = TextField()
    waypoint_symbol = TextField()
    expiration = DateTimeField()
    size = TextField()
    time_stamp = DateTimeField()

    def __repr__(self):
        return f"{self.signature}, {self.waypoint_symbol}, {self.expiration}, {self.size}, {self.time_stamp}"

    # class Meta:
    #
    #     table_name = 'svy_result'



class Deposit(BaseModel):
    survey = ForeignKeyField(SurveyResult, backref="deposits")
    survey_deposits = ArrayField(CharField)

    # class Meta:
    #     table_name = 'svy_deposit'


def create_svy_tables():
    with pg_db:
        pg_db.create_tables([SurveyResult, Deposit])
        # pg_db.create_tables([SurveyResult])


create_svy_tables()
