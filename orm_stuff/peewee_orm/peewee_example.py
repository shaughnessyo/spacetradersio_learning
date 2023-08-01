from playhouse.postgres_ext import ArrayField
import peewee
import datetime
from peewee import *
from SECRETS import sql_account, sql_pw
import logging


logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
# create a peewee database instance -- our models will use this database to
# persist information
pg_db = peewee.PostgresqlDatabase('spacetraders',
                                  user=sql_account,
                                  password=sql_pw,
                                  host='localhost',
                                  port=5432)


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = pg_db


# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()


# this model contains two foreign keys to user -- it essentially allows us to
# model a "many-to-many" relationship between users.  by querying and joining
# on different columns we can expose who a user is "related to" and who is
# "related to" a given user
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        # `indexes` is a tuple of 2-tuples, where the 2-tuples are
        # a tuple of column names to index and a boolean indicating
        # whether the index is unique or not.
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('from_user', 'to_user'), True),
        )


# a dead simple one-to-many relationship: one user has 0..n messages, exposed by
# the foreign key. a users messages will be accessible as a special attribute,
# User.messages.
class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()


def create_tables():
    with pg_db:
        pg_db.create_tables([User, Relationship, Message])

create_tables()