# old psycopg2 query
# sql1 = '''select * from survey_results;'''
#
# with psycopg2.connect(
#         database="spacetraders", user=sql_account, password=sql_pw,
#         host='127.0.0.1', port='5432') as conn:
#     with conn.cursor() as curs:
#         curs.execute(sql1)
#         results = curs.fetchall()
#
# try:
#     pass
#     # connection usage
# finally:
#     conn.close()


from dataclasses import dataclass
from datetime import timedelta, datetime

import arrow
from playhouse.postgres_ext import PostgresqlExtDatabase

from SECRETS import sql_account, sql_pw
from peewee_models import SurveyResult, Deposit

pg_db = PostgresqlExtDatabase(
    "spacetraders", user=sql_account, password=sql_pw, host="localhost", port=5432
)

arrow_now = arrow.utcnow()


@dataclass
class SurveyDepositResult:
    """
    this is somewhat redundant, but the obj that peewee is using is
    not useful for this unless i just want to take a SurveyResult and Deposit
    """

    id: int
    signature: str
    waypoint_symbol: str
    expiration: datetime
    size: str
    time_stamp: datetime
    d_id: int
    svy_deposits: list  # doesn't this need to be a factory template?
    valid: bool or None = None
    # def __post_init__(self):
    #     valid: bool | None

    def check_valid(self):
        """
        set the valid bool
        :return:
        """
        arrow_now = arrow.utcnow()
        zero_time = timedelta(
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        time_left = arrow.get(self.expiration) - arrow_now

        self.valid = True if time_left > zero_time else False
        # let's try without the ternary
        # if time_left > zero_time:
        #     self.valid = True
        # else:
        #     self.valid = False

    def cull_survey_result_from_sql(self):
        """
        maybe shouldn't be here
        :return:
        """
        pass

    def return_a_survey_object(self):
        """
        this should happen after whatever filtering

        i feel like the way i'm handling objects is very suboptimal
        :return: Survey object needed for ExtractResourcesJsonBody
        """
        from space_traders_api_client.models.survey import (
            Survey,
            SurveyDeposit,
            SurveySize,
        )
        from space_traders_api_client.models.extract_resources_json_body import (
            ExtractResourcesJsonBody,
        )

        # todo it's silly to have this as an additional process, i should store the
        # deposit obj
        deposit_list = []
        for item in self.svy_deposits:
            deposit_obj = SurveyDeposit(item)
            deposit_list.append(deposit_obj)

        svy_size = SurveySize(self.size)
        svy = Survey(
            signature=self.signature,
            symbol=self.waypoint_symbol,
            deposits=deposit_list,
            expiration=self.expiration,
            size=svy_size,
        )
        extract_resources_json_body = ExtractResourcesJsonBody(svy)
        return extract_resources_json_body


query = (
    SurveyResult.select(SurveyResult, Deposit)
    .where(SurveyResult.expiration > arrow_now.datetime)
    .join(Deposit)
    .dicts()
)
# for q in query:
#     print(q.items())
# print(query.items())
survey_deposit_result_list = []
survey_deposit_result_dict = {}

for q in query:
    # print(q.values())
    survey_deposit_result_dict[q["id"]] = SurveyDepositResult(*q.values())
    result = SurveyDepositResult(*q.values())
    # survey_deposit_result_list.append(SurveyDepositResult(*q.values()))
    survey_deposit_result_list.append(result)
print(survey_deposit_result_list)
print(survey_deposit_result_dict.items())


for result in survey_deposit_result_list:
    print(result.valid)
    result.check_valid()
    print(result.valid)

print("shouldn't be any nones")
for result in survey_deposit_result_list:
    print(result.valid)

print("checking valid", survey_deposit_result_list[0].valid)


# todo i feel like maybe survey should just be an object i can ser/des as needed
def get_valid_surveys() -> list:
    """
    queries SurveyResult joined with Deposit and returns a list of valid/unexpired survey results
    :return:
    """
    query = (
        SurveyResult.select(SurveyResult, Deposit)
        .where(SurveyResult.expiration > arrow_now.datetime)
        .join(Deposit)
        .dicts()
    )
    zero_time = timedelta(
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    valid_surveys = []
    for q in query:
        time_left = arrow.get(q["expiration"]) - arrow_now
        if time_left > zero_time:
            valid_surveys.append(q)
    return valid_surveys


valid_surveys = get_valid_surveys()
print(valid_surveys)

naive_resource_dict = {
    "PRECIOUS_STONES": 1,
    "SILICON_CRYSTALS": 2,
    "QUARTZ_SAND": 0,
    "ALUMINUM_ORE": 3,
    "AMMONIA_ICE": 1,
    "IRON_ORE": 3,
    "COPPER_ORE": 3,
    "DIAMONDS": 10,
    "SILVER_ORE": 5,
    "GOLD_ORE": 5,
    "PLATINUM_ORE": 5,
    "URANITE_ORE": 10,
    "MERITIUM_ORE": 10,
    "ICE_WATER": -1,
}


def get_naive_survey_weights(valid_surveys: list) -> dict[int]:
    """
    this uses my very halfassed sense of how the resources i've mined so far should be ranked in order to prioritize specific surveys over other ones
    :param valid_surveys: the survey deposit list from a survey
    :return: int survey rank
    """
    survey_rank_dict = {}
    for survey in valid_surveys:
        print(survey)
        deposit_rank_sum = 0
        for deposit in survey["survey_deposits"]:
            deposit_rank_sum = deposit_rank_sum + naive_resource_dict[deposit]
        survey_rank_dict[survey["id"]] = deposit_rank_sum
    return survey_rank_dict


def get_max_ranked_survey_dict() -> tuple:
    """
    right now this just grabs the max value in dict.values and prints k:v
    :return: k:v as tuple
    """
    survey_rank_dict = get_naive_survey_weights(get_valid_surveys())
    print(survey_rank_dict.items())

    for k, v in survey_rank_dict.items():
        if v == max(survey_rank_dict.values()):
            print(f"{k}:{v}")
            return (k, v)


print(get_max_ranked_survey_dict())

# print(get_naive_survey_weights(get_valid_surveys()))
# test_dict = get_naive_survey_weights(get_valid_surveys())
# print(test_dict.items())


# print(get_naive_survey_weights(get_valid_surveys()))
def build_survey_result_dict() -> dict:
    """
    this probably should be a little more-- i should filter out the
    expired surveys before ranking them
    :return:
    """
    survey_result_dict = {}
    for k, v in enumerate(
        SurveyResult.select(SurveyResult, Deposit).join(Deposit).dicts()
    ):
        survey_result_dict[k] = v
    return survey_result_dict
