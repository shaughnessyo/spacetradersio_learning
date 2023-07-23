from sqlalchemy.orm import sessionmaker
# from get_ships import Ship
from models import Ships, SurveyResults
from models import SystemWaypoints
import sqlalchemy as sa

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')

Session = sessionmaker(bind=engine)


# i feel like there's something off with how i'm doing this-- i'm passing an object and then adding it?
def system_waypoints_to_sql(system_symbol, waypoint_symbol, waypoint_type, jumpgate_list):
    s = Session()
    system_waypoints = SystemWaypoints(system_symbol=system_symbol,
                                   waypoint_symbol=waypoint_symbol,
                                   waypoint_type=waypoint_type,
                                   jumpgate_list=jumpgate_list)
    s.add(system_waypoints)
    s.commit()
    s.close()


def ships_to_sql(ship):
    s = Session()
    ships = Ships(ship_symbol=ship.symbol, role=ship.role, nav_location=ship.nav_location,
                  nav_waypoint_location=ship.nav_waypoint_location, nav_status=ship.nav_status,
                  nav_flight_mode=ship.nav_flight_mode, fuel_current=ship.fuel_current,
                  fuel_capacity=ship.fuel_capacity, cargo_current=ship.cargo_current,
                  cargo_capacity=ship.cargo_capacity, systems_in_jumpgate_range=ship.systems_in_jumpgate_range)
    s.add(ships)
    s.commit()
    s.close()


def survey_results_to_sql(signature, waypoint_symbol, deposits, expiration, size):
    """
    i'm replicating the already existing schema for a Survey
    :param signature:
    :param waypoint_symbol:
    :param deposits:
    :param expiration:
    :param size:
    :return:
    """
    s = Session()
    survey_results = SurveyResults(signature=signature, waypoint_symbol=waypoint_symbol, deposits=deposits,
                                   expiration=expiration, size=size)
    s.add(survey_results)
    s.commit()
    s.close()



