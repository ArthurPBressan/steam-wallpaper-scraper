import os
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

from scraper import utils


def scrape(client):
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
        _, ext = os.path.splitext(url)
        card_title = utils.clean_card_title(card_title)
        filename = '{} - {}{}'.format(game_title, card_title, ext)
        path = 'wallpapers/{}'.format(filename)

        if os.path.exists(path):
            print('Skipping "{}"'.format(card_title))
            continue

        print('Downloading "{}"'.format(card_title))
        image_request = session.get(url, stream=True)
        total_size = int(image_request.headers.get('content-length', 0))
        with tqdm(total=total_size,   unit='B', unit_scale=True) as pbar:
            with open(path, 'wb') as img_file:
                for chunk in image_request:
                    img_file.write(chunk)
                    pbar.update(len(chunk))
