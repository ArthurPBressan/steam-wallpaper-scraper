import os
import re

from steam import SteamClient
from steam.enums import EResult
from bs4 import BeautifulSoup

from scraper import utils

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
    print('Downloading wallpapers from {} ({})'
          .format(game_title, gamecard_url))
    while True:
        response = session.get(gamecard_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if 'There was an error getting trading card information.' in soup.text:
            print('Error on badges page, retrying...')
        else:
            break

    for div in soup.find_all("div", "badge_card_set_card owned"):
        zoom_div = div.find("div", "game_card_ctn with_zoom")
        onclick = zoom_div.attrs['onclick']
        card_title, escaped_url = re.search(r'"(.*)", "(.*)"', onclick)\
            .groups(0)
        url = escaped_url.replace('\\', '')
        card_title = utils.clean_card_title(card_title)
        image_request = session.get(url)
        print('Downloading "{}"'.format(card_title))
        filename = 'wallpapers/{} - {}.jpg'.format(game_title, card_title)
        with open(filename, 'wb') as img_file:
            for chunk in image_request:
                img_file.write(chunk)

os.makedirs('wallpapers/', exist_ok=True)
session = client.get_web_session()
badges_page_url = client.user.steam_id.community_url + '/badges'
response = session.get(badges_page_url)
badges_page_soup = BeautifulSoup(response.content, 'html.parser')

badges_rows = badges_page_soup.find_all('div', 'badge_row is_link')
for row in badges_rows:
    a = row.find('a', 'badge_row_overlay')
    href = a.attrs['href']
    if 'gamecards' in href:
        title = row.find('div', 'badge_title').contents[0]
        title = utils.clean_game_title(title)
        download_wallpapers(title, href, session)
    else:
        print('Skipping url {}'.format(href))

client.logout()
