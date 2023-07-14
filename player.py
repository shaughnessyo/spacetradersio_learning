from dataclasses import dataclass, field
from key import key

@dataclass
class Player:
    base_url: str
    username: str
    key: str
    headers: dict


username = "clj1qi3rg0ozcs60ds8dqat8g"
base_url = "https://api.spacetraders.io/v2/"
headers = { \
    "Accept": "application/json",
    "Authorization": f"Bearer {key}"
}

player = Player(base_url, username, key, headers)


