from __future__ import print_function

import re

from steam import SteamClient
from steam.enums import EResult
from bs4 import BeautifulSoup

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


def download_wallpapers(game_title, gamecard_url, session):
    print('Downloading wallpapers from {} ({})'.format(game_title, gamecard_url))
    response = session.get(gamecard_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for div in soup.find_all("div", "badge_card_set_card owned"):
        zoom_div = div.find("div", "game_card_ctn with_zoom")
        onclick = zoom_div.attrs['onclick']
        result = re.search(r'\".*\"', onclick).group(0)
        card_title, escaped_url = result.replace('"', '').split(", ")
        url = escaped_url.replace('\\', '')
        image_request = session.get(url)
        filename = '{} - {}.jpg'.format(game_title, card_title)
        with open(filename, 'wb') as img_file:
            for chunk in image_request:
                img_file.write(chunk)

session = client.get_web_session()
badges_page_url = client.user.steam_id.community_url + '/badges'
response = session.get(badges_page_url)
badges_page_soup = BeautifulSoup(response.content, 'html.parser')

badges_rows = badges_page_soup.find_all('div', 'badge_row is_link')
for row in badges_rows:
    a = row.find('a', 'badge_row_overlay')
    href = a.attrs['href']
    if 'gamecards' in href:
        title = row.find('div', 'badge_title').contents[0].strip()
        download_wallpapers(title, href, session)
    else:
        print('Skipping url {}'.format(href))

client.logout()
