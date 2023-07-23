from sqlalchemy.orm import sessionmaker

from models import StatusCode
import sqlalchemy as sa

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')

Session = sessionmaker(bind=engine)


def log_status_code(api_call: str, ship_symbol:str, status_code: int) -> None:
    """

    :param status_code:
    :return:
    """
    s = Session()
    status_code = StatusCode(api_call=api_call, obj_symbol=ship_symbol, status_code=status_code)
    s.add(status_code)
    s.commit()
    s.close()


class LogInformation:
    """
    created a class to pass information i want to log from the api call and insert it into postgresql

    shit, this is going to be a problem each time the server resets

    """
    def __init__(self):
        self.api_endpoint = None
        self.obj_symbol = None
        self.status_code = None

    def set_api_endpoint(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def set_obj_symbol(self, ship_symbol: str):
        self.obj_symbol = ship_symbol

    def set_status_code(self, status_code: int):
        self.status_code = status_code
        self.data_to_sql()

    def data_to_sql(self):
        if self.status_code and self.api_endpoint and self.obj_symbol:
            log_status_code(ship_symbol=self.obj_symbol, api_call=self.api_endpoint, status_code=self.status_code)

