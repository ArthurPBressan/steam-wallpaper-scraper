from __future__ import print_function
from steam import SteamClient
from steam.enums import EResult

client = SteamClient()

print("One-off login recipe")
print("-"*20)

result = client.cli_login()

if result != EResult.OK:
    print("Failed to login: %s" % repr(result))
    raise SystemExit

print("-"*20)
print("Logged on as:", client.user.name)
print("Community profile:", client.steam_id.community_url)
print("Last logon:", client.user.last_logon)
print("Last logoff:", client.user.last_logoff)

session = client.get_web_session()
resp = session.get("https://steamcommunity.com/id/harddiskd/gamecards/220200/")

from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.content, 'html.parser')

import re
for div in soup.find_all("div", "badge_card_set_card owned"):
    zoom_div = div.find("div", "game_card_ctn with_zoom")
    onclick = zoom_div.attrs['onclick']
    result = re.search(r'\".*\"', onclick).group(0)
    title, escaped_url = result.replace('"', '').split(", ")
    url = escaped_url.replace('\\', '')
    image_request = session.get(url)
    with open('{}.jpg'.format(title), 'wb') as img_file:
        for chunk in image_request:
            img_file.write(chunk)

client.logout()
