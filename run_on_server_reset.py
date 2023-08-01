"""
COME BACK TO THIS

first, go get the new bundled json
https://spacetraders.stoplight.io/docs/spacetraders/11f2735b75b02-space-traders-api

then use openapi-generator to generate a python api client library from the bundled json

merge your modified api calls (doing it manually now, but it wouldn't be hard to automate)
"""
from client import client
from data_decode import data_decode
from space_traders_api_client.api.default import register
from space_traders_api_client.models.register_json_body import RegisterJsonBody
from space_traders_api_client.models.faction_symbols import FactionSymbols

# AEGIS = "AEGIS"
# ANCIENTS = "ANCIENTS"
# ASTRO = "ASTRO"
# COBALT = "COBALT"
# CORSAIRS = "CORSAIRS"
# COSMIC = "COSMIC"
# CULT = "CULT"
# DOMINION = "DOMINION"
# ECHO = "ECHO"
# ETHEREAL = "ETHEREAL"
# GALACTIC = "GALACTIC"
# LORDS = "LORDS"
# OBSIDIAN = "OBSIDIAN"
# OMEGA = "OMEGA"
# QUANTUM = "QUANTUM"
# SHADOW = "SHADOW"
# SOLITARY = "SOLITARY"
# UNITED = "UNITED"
# VOID = "VOID"

faction_symbol = FactionSymbols("ECHO")
json_body = RegisterJsonBody(faction_symbol, "JUMBO")

# i should log this api call since it would be a good indicator of when a survey reset happened? or a new agent began?
# i dunno
response = register.sync_detailed(json_body=json_body, client=client)
if response.status_code in [200, 201]:
    print(data_decode(response.content))


#july23 client token
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiSlVNQk8iLCJ2ZXJzaW9uIjoidjIiLCJyZXNldF9kYXRlIjoiMjAyMy0wNy0yMyIsImlhdCI6MTY5MDE0MzQ3Miwic3ViIjoiYWdlbnQtdG9rZW4ifQ.tG1gbo9kpJfUWOeE5Et0ym6ElRf5nP2uzGyvRW2VmoJxoZzM9UBoqm-hXaxRBAjAILrM6nRDlLZq00sDU4aOpyq2mCDRKL1xTwMdQhn7ZCcxEIc-G22TbzD6dZSjkIydCIdBwSN8q-w3u89nwvgBXoqXmMJ3WcQxmZOVtxzHsdjh1nOmXp_-e_zorCCz-VdEG29AFeaxWmt9x5DCP4eK8iH8qTuIMb-Dob51h51GaWbNKt9po2SUsoPsBm8YrtK0I2tWJW8pug1rfniF-bP1ymYsRZYXBsP6ouYhP1yqUvnbtpqRAkYXrqjPI7d2dR7_j6yV5teKGQKScA6SgP86tw"

# july31 token
"agent": {
    "accountId": "clkqvttpbo18cs60cutxcrrtn",
    "symbol": "JUMBO",
    "headquarters": "X1-NU72-83580E",
    "credits": 150000,
    "startingFaction": "VOID"



# curl --request POST \
#  --url 'https://api.spacetraders.io/v2/register' \
#  --header 'Content-Type: application/json' \
#  --data '{
#     "symbol": "jumbo",
#     "faction": "COSMIC"
#    }'
"token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiSlVNQk8iLCJ2ZXJzaW9uIjoidjIiLCJyZXNldF9kYXRlIjoiMjAyMy0wNy0yOSIsImlhdCI6MTY5MDgwODY3NSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.WPoJgzqXsd9PsEEUDWRyd0mitf5H6eFyycaXveZxPLe3snqIi_vROmEiaNM-iKOqUGUqnUJL77HBX0wX9UJxvqog7hqO512BXFeJ8mcrXrY5MTL3dUCOeBZ5qc62SbK0Xa9YvTJtguRK7-JFuVMwcdzxOkSGsvlLYcDkVQrgBcsyar5LiatsupFEqNw9lZ5GpLp2W5twYXNriWTKcTE6QiX6PhqGHJ-HhLwbmejycAGhHYSZxBNDPqUC1CEIrpQPZ8_yDdrNQUt_Hqb77VeeuQH383WV2BPFXHTIdeTwlxGd6kZZiH1FUOEKV_NNKfOGt_DmB-JQS3o2Tf4bu19mnQ",
