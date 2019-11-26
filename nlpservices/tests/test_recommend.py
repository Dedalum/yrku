"""Test for helpers functions"""
import os
import shutil

import pytest
from gensim.test.utils import common_corpus, common_dictionary, common_texts

import nlpservice.helpers
import nlpservice.recommend


class TestRecommender:
    """
    Test class for Recommender class
    """

    books = [
        'French cuisine', 'A tour around France',
        'French literature, poems and other arts', 'Voltaire was French',
        'Voltaire died in Sweden', 'Dragons are not big lizzards',
        'Dragons and dungeons', 'Castles have dungeons, sometimes dragons'
    ]

    data_dir = "test_nlprecommend_data"

    def test_pre_setup(self):
        """
        Test generating pre-setup (documents, dictionary and corpus) and save
        it to files, then load it from the same files.
        """
        # pre-setup
        recommender = nlpservice.recommend.Recommender(data_dir=self.data_dir)
        recommender.pre_setup(docs=self.books)

        # Load from files pre-setup
        recommender.pre_setup(docs=self.books)

    def test_ideal_nb_topics(self):
        """"
        Test finding the ideal number of topics to be used in our LSI model.
        """
        # pre-setup
        recommender = nlpservice.recommend.Recommender(data_dir=self.data_dir)
        recommender.pre_setup(docs=self.books)

        ideal_nb_topics = recommender.ideal_nb_topics(2, 15)
        assert 15 >= ideal_nb_topics >= 2

    def test_setup(self):
        """
        Test loading the LSI model, the vectors and the similarities matrix,
        saving it to files and then reload these from the same files.
        """
        recommender = nlpservice.recommend.Recommender(data_dir=self.data_dir)
        recommender.pre_setup(docs=self.books)

        recommender.setup()

    def test_top_books(self):

        # Pre-setup, optimize the number of topics and final setup
        recommender = nlpservice.recommend.Recommender(data_dir=self.data_dir)
        recommender.pre_setup(docs=self.books)
        ideal_nb_topics = recommender.ideal_nb_topics(2, 15)
        recommender.setup(ideal_nb_topics)

        # search for top 5 most similar books to the title "The Murders in the
        # Rue Morgue"
        title = "Dragons and dungeons"
        top_books = recommender.top_books(title)

        print("Top books for %s" % title)
        for book in top_books:
            print("%s: %s" % (book[0], book[1]))

    @pytest.fixture(scope="session", autouse=True)
    def clean_up(self, request):
        def _end():
            shutil.rmtree(self.data_dir)  # clean-up...

        request.addfinalizer(_end)
