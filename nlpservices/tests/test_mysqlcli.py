import warnings

import pytest

import nlpservice.mysqlcli


class TestClient:
    """
    Test class for mysqlcli module
    """

    author = "Edgar Allan Poe"
    mysql_client = nlpservice.mysqlcli.Client("localhost", "nlp_recommend",
                                              "example", "db1")

    expected_books = [{
        'title': 'The Tell-Tale Heart and Other Writings'
    }, {
        'title': 'The Complete Stories and Poems'
    }, {
        'title': 'The Cask of Amontillado'
    }, {
        'title': 'The Pit and the Pendulum'
    }, {
        'title': 'The Fall of the House of Usher'
    }, {
        'title': 'The Masque of the Red Death'
    }, {
        'title': 'The Black Cat'
    }, {
        'title': 'The Murders in the Rue Morgue'
    }, {
        'title': 'The Complete Tales and Poems'
    }]

    titles = [
        'The Tell-Tale Heart and Other Writings',
        'The Complete Stories and Poems', 'The Cask of Amontillado',
        'The Pit and the Pendulum', 'The Fall of the House of Usher',
        'The Masque of the Red Death', 'The Black Cat',
        'The Murders in the Rue Morgue', 'The Complete Tales and Poems'
    ]

    expected_filtered_titles = [['tell', 'tale', 'heart', 'write'],
                                ['complet', 'stori', 'poem'],
                                ['cask', 'amontillado'], ['pit', 'pendulum'],
                                ['fall', 'hous', 'usher'],
                                ['masqu', 'red', 'death'], ['black', 'cat'],
                                ['murder', 'rue', 'morgu'],
                                ['complet', 'tale', 'poem']]

    def test_get_author_books(self):
        """
        Test get author books. Requires a MySQL DB to be running
        """
        books = self.mysql_client.get_author_books(self.author)

        assert books == self.expected_books

    def test_bad_db(self):
        """Test with a bad DB"""
        self.mysql_client.database = "bad_db"
        with pytest.raises(Exception):
            self.mysql_client.get_author_books(self.author)

        self.mysql_client.database = "db1"

    def test_bad_table(self):
        """Test with a bad table"""
        with pytest.raises(Exception):
            self.mysql_client.get_title_book("The Murders in the Rue Morgue",
                                             table="bad_table")

    def test_bad_author(self):
        """
        Test with a bad author (not found author). A warning should be triggered.
        """
        with pytest.warns(
                UserWarning,
                match=r"data returned is empty. Author '.*' not found"):
            self.mysql_client.get_author_books("not_an_author_name")

    def test_bad_title(self):
        """
        Test with a bad title (book not found). A warning should be triggered.
        """
        with pytest.warns(UserWarning,
                          match=r"data returned is empty. Book .* not found"):
            self.mysql_client.get_title_book("Från mars -79")
