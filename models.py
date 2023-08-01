### models.py ###
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, orm
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import array
from sqlalchemy.dialects import postgresql
from sqlalchemy import select, func

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')
Base = sa.orm.declarative_base()


class Ships(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True)
    ship_symbol = Column(String)
    role = Column(String)
    nav_location = Column(String)
    nav_waypoint_location = Column(String)
    nav_status = Column(String)
    nav_flight_mode = Column(String)
    fuel_current = Column(Integer)
    fuel_capacity = Column(Integer)
    cargo_current = Column(String)
    cargo_capacity = Column(Integer)
    systems_in_jumpgate_range = Column(String)

    # miner = Column(String)
    # okay not sure about how to do the systems in jumpgate range -- maybe i can just cast text into a dict etc?

    def __repr__(self):
        return "<Ships(id='{}', ship_symbol='{}', role='{}', nav_location='{}', nav_waypoint_location='{}', " \
               "nav_status='{}', nav_flight_mode='{}',fuel_current='{}',fuel_capacity='{}',cargo_current='{}'," \
               "cargo_capacity='{}',systems_in_jumpgate_range='{}'," \
            .format(self.id, self.ship_symbol, self.role, self.nav_location, self.nav_waypoint_location,
                    self.nav_status,
                    self.nav_flight_mode, self.fuel_current, self.fuel_capacity, self.cargo_current,
                    self.cargo_capacity,
                    self.systems_in_jumpgate_range)

    # this is probably the way to do it
    # def set_miner(self):


class StatusCode(Base):
    __tablename__ = 'status_codes'
    id = Column(Integer, primary_key=True)
    obj_symbol = Column(String)
    api_call = Column(String)
    status_code = Column(Integer)
    tm_stamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=sa.func.now())

    def __repr__(self):
        return "<StatusCode(id='{}', obj_symbol='{}'," \
               " status_code='{}', tm_stamp={})>".format(self.id, self.obj_symbol, self.status_code, self.tm_stamp)

    def set_ship_symbol(self, obj_symbol):
        self.obj_symbol = obj_symbol


class MarketTransactions(Base):
    __tablename__ = "market_transactions"

    id = Column(Integer, primary_key=True)
    player_credits = Column(Integer)
    waypoint_symbol = Column(String)
    ship_symbol = Column(String)
    trade_symbol = Column(String)
    # todo type might need an intermediary object that contains BUY/SELL
    market_interaction_type = Column(String)
    units = Column(Integer)
    price_per_unit = Column(Integer)
    total_price = Column(Integer)
    time_stamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=sa.func.now())

    def __repr__(self):
        return "MarketTransactions(id ='{}', player_credits='{}', waypoint_symbol = '{}', ship_symbol='{}', trade_symbol='{}', type ='{}', " \
               "units='{}', price_per_unit = '{}', total_price = '{}', \
               time_stamp = '{}'" \
            .format(self.id, self.player_credits, self.waypoint_symbol, self.ship_symbol, self.trade_symbol,
                    self.market_interaction_type, self.units,
                    self.price_per_unit, self.total_price, self.time_stamp)

    def set_player_credits(self, credits):
        self.player_credits = credits


# todo think about how to store systems and waypoints for the easiest lookup

class SystemWaypoints(Base):
    __tablename__ = "system_waypoints"

    id = Column(Integer, primary_key=True)
    system_symbol = Column(String)
    waypoint_symbol = Column(String)
    waypoint_type = Column(String)
    jumpgate_list = Column(String)

    def __repr__(self):
        return f"SystemWaypoints(id={self.id}, system_symbol = {self.system_symbol}," \
               f" waypoint_symbol= {self.waypoint_symbol}, jumpgate_list = {self.jumpgate_list}"


# class SystemWaypointsJumpgate


# todo i can either switch to peewee orm or figure out how to do the things i need in alchemy
# i could import the array type from postgresql extensions
class SurveyResults(Base):
    __tablename__ = "survey_results"
    id = Column(Integer, primary_key=True)
    signature = Column(String)
    waypoint_symbol = Column(String)
    # deposits = Column(String)  # actually a list

    deposits = Column("deposits", postgresql.ARRAY(String))  # actually a list
    expiration = Column(String)  # this is a datetime but i'm not sure how to handle it before it goes into postgresql
    # datetime.fromisoformat(
    size = Column(String)  # actually an enum i think?
    time_stamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=sa.func.now())

    def __repr__(self):
        return f"SurveyResults(id={self.id}, signature={self.signature}, waypoint_symbol={self.waypoint_symbol}," \
               f"deposits={self.deposits}, expiration={self.expiration}, size={self.size}"


# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     author = Column(String)
#     pages = Column(Integer)
#     published = Column(Date)
#
#     def __repr__(self):
#         return "<Book(title='{}', author='{}', pages={}, published={})>" \
#             .format(self.title, self.author, self.pages, self.published)


Base.metadata.create_all(engine)
