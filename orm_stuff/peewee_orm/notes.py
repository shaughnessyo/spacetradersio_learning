import peewee
from SECRETS import sql_account, sql_pw


# pg_db = peewee.PostgresqlDatabase('my_app', user=sql_account, password=sql_pw,
#                                   host='localhost', port=5432)



from peewee import *

# db = SqliteDatabase('people.db')
pg_db = peewee.PostgresqlDatabase('spacetraders',
                                  user=sql_account,
                                  password=sql_pw,
                                  host='localhost',
                                  port=5432)

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = pg_db # This model uses the "people.db" database.


