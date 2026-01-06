import os
import json
from steam_web_api import Steam

KEY = os.environ.get("STEAM_API_KEY")


steam = Steam(KEY)
steamid = "76561198385279682"
steamid1 =  "76561198385279682"
steamid2 =  "76561198366107133"

# arguments: steamid
response = steam.users.get_user_friends_list(steamid)

print(response)

with open("steam/response.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

"""
#documentary
get_user_friends_list
get_owned_games

#for ami in response.get("friends", []):
#    print(ami["personaname"])
"""