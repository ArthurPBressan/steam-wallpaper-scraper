from scraper import utils


class TestCleanTitle():

    def test_strip_foil(self):
        title = 'Just Cause 3 \t- Foil Badge \t\t\t'
        assert 'Just Cause 3' == utils.clean_title(title)

    def test_do_not_change_clean_titles(self):
        title = 'Just Cause 3'
        assert title == utils.clean_title(title)

    def test_clean_non_foil(self):
        title = 'Just Cause 3 \t\t\t\t\t'
        assert 'Just Cause 3' == utils.clean_title(title)
