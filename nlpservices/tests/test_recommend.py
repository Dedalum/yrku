"""Test for helpers functions"""
import shutil

import pytest

import nlpservice.helpers
import nlpservice.recommend


class TestRecommender:
    """
    Test class for Recommender class
    """

    books = [
        'French cuisine', 'A tour around France',
        'French literature, poems and other arts in 19th cent.',
        'Voltaire was French', 'Voltaire died in Sweden',
        'Dragons are not big lizzards', 'Dragons and dungeons',
        'Castles have dungeons, sometimes dragons', 'Bear-man-pig-moose'
    ]

    data_dir = "test_nlprecommend_data"

    def test_pre_setup(self):
        """
        Test generating pre-setup (documents, dictionary and corpus) and save
        it to files, then load it from the same files.
        """
        # pre-setup
        try:
            recommender = nlpservice.recommend.Recommender(
                "", "", "", "", data_dir=self.data_dir)
            recommender.pre_setup(docs=self.books)

            # Load from files pre-setup
            recommender.pre_setup(docs=self.books)
        except Exception as err:
            pytest.fail("failed test: %s" % err)

    def test_ideal_nb_topics(self):
        """"
        Test finding the ideal number of topics to be used in our LSI model.
        """
        # pre-setup
        try:
            recommender = nlpservice.recommend.Recommender(
                "", "", "", "", data_dir=self.data_dir)
            recommender.pre_setup(docs=self.books)

            ideal_nb_topics = recommender.ideal_nb_topics(2, 15)
            assert 15 >= ideal_nb_topics >= 2
        except Exception as err:
            pytest.fail("failed test: %s" % err)

    def test_setup(self):
        """
        Test loading the LSI model, the vectors and the similarities matrix,
        saving it to files and then reload these from the same files.
        """
        try:
            recommender = nlpservice.recommend.Recommender(
                "", "", "", "", data_dir=self.data_dir)
            recommender.pre_setup(docs=self.books)

            recommender.setup()
        except Exception as err:
            pytest.fail("failed test: %s" % err)

    def test_top_books(self):
        """
        Test top books recommendation, using the title only
        """
        # Pre-setup, optimize the number of topics and final setup
        # for the test, we do not use MySQL to load the data here so fill it
        # with empty strings
        try:
            recommender = nlpservice.recommend.Recommender(
                "", "", "", "", data_dir=self.data_dir)
            recommender.pre_setup(docs=self.books)
            ideal_nb_topics = recommender.ideal_nb_topics(2, 15)
            recommender.setup(nb_topics=ideal_nb_topics)

            title = "French literature, poems and other arts in 19th cent."
            top_books = recommender.top_books(title, top_nb_docs=3)

            print("Top books for %s" % title)
            for book in top_books:
                print(book)

        except Exception as err:
            pytest.fail("failed test: %s" % err)

    @pytest.fixture(scope="session", autouse=True)
    def clean_up(self, request):
        """Clean up created files and directories for testing purposes"""
        def _end():
            shutil.rmtree(self.data_dir)

        request.addfinalizer(_end)
