from sqlalchemy.orm import sessionmaker
# from get_ships import Ship
from models import Ships
import sqlalchemy as sa

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')

Session = sessionmaker(bind=engine)


#am i just tired-- should i just be importing the Ship object?

def ships_to_sql(ship):

    s = Session()
    ships = Ships(ship_symbol=ship.symbol,role=ship.role,nav_location=ship.nav_location,
                  nav_waypoint_location=ship.nav_waypoint_location,nav_status=ship.nav_status,
                  nav_flight_mode=ship.nav_flight_mode,fuel_current=ship.fuel_current,
                  fuel_capacity=ship.fuel_capacity,cargo_current=ship.cargo_current,
                  cargo_capacity=ship.cargo_capacity,systems_in_jumpgate_range=ship.systems_in_jumpgate_range)
    s.add(ships)
    s.commit()
    s.close()


