from scraper import utils


class TestCleanGameTitle():

    def test_strip_foil(self):
        title = 'Just Cause 3 \t- Foil Badge \t\t\t'
        assert 'Just Cause 3' == utils.clean_game_title(title)

    def test_do_not_change_clean_titles(self):
        title = 'Just Cause 3'
        assert title == utils.clean_game_title(title)

    def test_clean_non_foil(self):
        title = 'Just Cause 3 \t\t\t\t\t'
        assert 'Just Cause 3' == utils.clean_game_title(title)


class TestCleanCardTitle():

    def test_removes_backslashes(self):
        title = 'TALOS\\/SOMA'
        assert 'TALOS-SOMA' == utils.clean_card_title(title)

    def test_strips_title(self):
        title = '\t    Card   \t'
        assert 'Card' == utils.clean_card_title(title)

    def test_unicode_names(self):
        title = 'General Jos\u00e9 de San Mart\u00edn'
        assert 'General José de San Martín' == utils.clean_card_title(title)
