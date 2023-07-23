"""
i either need to rewrite extract_resources_json_body, Survey, etc etc to take this or work with them
and right now i think working with them is probably the easier option

"""


from dataclasses import dataclass
import datetime


@dataclass
class MiningSurvey:
    signature: str
    waypoint_symbol: str
    deposits: list
    expiration: datetime.datetime
    size: str
