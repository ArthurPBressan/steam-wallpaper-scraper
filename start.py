import click
from steam import SteamClient
from steam.enums import EResult

import scraper


def _user_aborted():
    print()
    print('Aborted by user')


@click.command()
@click.option('--dirname', default=scraper.default_dirname,
              help='Directory name of where the wallpapers will be saved')
def main(dirname):
    client = SteamClient()

    print("Steam Cards Wallpaper Downloader")
    print("-"*20)

    try:
        result = client.cli_login()
    except (EOFError, KeyboardInterrupt):
        _user_aborted()
        raise SystemExit

    if result != EResult.OK:
        print("Failed to login: %s" % repr(result))
        raise SystemExit
    print("-"*20)
    print("Logged on as:", client.user.name)

    try:
        scraper.scrape(client, dirname)
    except KeyboardInterrupt:
        _user_aborted()
    finally:
        client.logout()


if __name__ == '__main__':
    main()
