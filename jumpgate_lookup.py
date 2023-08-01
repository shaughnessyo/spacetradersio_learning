### dealing with the query through psycopg2 instead of pandas
from SECRETS import sql_account, sql_pw
import psycopg2.extras

conn = psycopg2.connect(
    database="spacetraders", user=sql_account, password=sql_pw,
    host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()


def build_jumpgate_lookup_dict() -> dict:
    """
    grabs system + systems in range of system waypoint jumpgate from postgresql and return a dictionary
    so that you can look up jumpgate systems from system symbol
    :return:
    """

    sql1 = '''select * from system_waypoints;'''
    cursor.execute(sql1)
    results = cursor.fetchall()


    jumpgate_lookup_dict = {}
    for row in results:
        if row[3] == "JUMP_GATE":

            sys_symbol = row[1]
            jg_split = row[4].split(',')

            jg_cleaned = []
            for jg in jg_split:
                jg_cleaned.append(jg.replace('{', '').replace('}', ''))
            jumpgate_lookup_dict[sys_symbol] = jg_cleaned


    conn.commit()
    conn.close()
    return jumpgate_lookup_dict

def jumpgate_lookup(system_symbol:str) -> list[str]:
    """
    lookup a ship's current system location in the jumpgate dict

    :param system_symbol: likely going to be Ship.nav_location
    :return:
    """
    jumpgate_dict = build_jumpgate_lookup_dict()
    jumpgate_systems = jumpgate_dict[system_symbol]
    counter=0
    jumpgate_choice_dict = {}
    for item in jumpgate_systems:
        # print(counter, item)
        jumpgate_choice_dict[counter] = item
        counter+=1
    return jumpgate_choice_dict
# print(jumpgate_lookup("X1-JF24"))