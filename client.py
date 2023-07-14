import player
from space_traders_api_client import Client, AuthenticatedClient


username = player.username
key = player.key

client = AuthenticatedClient(base_url="https://api.spacetraders.io/v2", token=key)


