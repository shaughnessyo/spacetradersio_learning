from sqlalchemy.orm import sessionmaker

from models import StatusCode, MarketTransactions
import sqlalchemy as sa

engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')

Session = sessionmaker(bind=engine)


# class MarketTransactions(Base):
#     __tablename__ = "market_transactions"
#
#     id = Column(Integer, primary_key=True)
#     waypoint_symbol = Column(String)
#     ship_symbol = Column(String)
#     trade_symbol = Column(String)
#     #todo type might need an intermediary object that contains BUY/SELL
#     type = Column(String)
#     units = Column(Integer)
#     price_per_unit = Column(Integer)
#     total_price = Column(Integer)
#     time_stamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=sa.func.now())
#

# todo you're tired, come back to this because it's being weird
def log_market_transaction(player_credits: int,
                           waypoint_symbol: str,
                           ship_symbol: str,
                           trade_symbol: str,
                           market_interaction_type: str,
                           units: int,
                           price_per_unit: int,
                           total_price: int,
                           ) -> None:
    """

    :param :
    :return:
    """
    s = Session()
    market_transaction = MarketTransactions(player_credits=player_credits,waypoint_symbol=waypoint_symbol, ship_symbol=ship_symbol,
                                            trade_symbol=trade_symbol, market_interaction_type=market_interaction_type, units=units,
                                            price_per_unit=price_per_unit, total_price=total_price)
    print("market_transaction?")
    s.add(market_transaction)
    s.commit()
    s.close()
