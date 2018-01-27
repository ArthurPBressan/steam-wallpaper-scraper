def clean_game_title(game_title):
    return game_title.replace('- Foil Badge', '').strip()


def clean_card_title(card_title):
    return card_title.replace(r'\\', '-').strip()
