"""Recommend module for recommending books based on given title"""
import errno
import json
import os
import pickle
import warnings

import gensim

import nlpservice.helpers
import nlpservice.mysqlcli


class Recommender:
    """
    Recommender class for generating the LSI model and returning book 
    recommendations
    """
    def __init__(self,
                 mysql_host,
                 mysql_user,
                 mysql_password,
                 mysql_db,
                 data_dir="nlprecommend_data"):
        """
        Args:
            data_dir (string): directory where the results are to be saved
        """
        self.data_dir = data_dir
        self.corpus_filename = "%s/corpus.mm" % self.data_dir
        self.dictionary_filename = "%s/docs.dictionary" % self.data_dir
        self.lsi_model_filename = "%s/lsi_model.model" % self.data_dir
        self.doc_to_id_filename = "%s/doc_to_id" % self.data_dir
        self.id_to_doc_filename = "%s/id_to_doc" % self.data_dir
        self.similarities_filename = "%s/docs.similarities" % self.data_dir
        self.vectors_filename = "%s/docs.vectors" % self.data_dir

        self.docs = None
        self.docs_clean = None
        self.doc_to_id = {}
        self.id_to_doc = {}
        self.corpus = None
        self.dictionary = None
        self.lsi_model = None
        self.vectors = None
        self.similarities = None

        self._create_data_dir()

        self.mysqlcli = nlpservice.mysqlcli.Client(mysql_host, mysql_user,
                                                   mysql_password, mysql_db)

    def _create_data_dir(self):
        """
        Create the data directory for saving the generated files

        Raises:
            error: unless the directory already exists (error ``errno.EEXIST``)
        """
        try:
            os.mkdir(self.data_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    def _load_docs(self, docs=None):
        """
        Load the documents from the MySQL DB, unless the documents are already
        passed.

        Args: 
            docs (list of strings): optional, pass the documents directly as 
            an arg instead of querying the DB
        """

        if docs is not None:
            self.docs = docs
        else:
            # keep only the titles from the SQL result
            docs_dict = self.mysqlcli.get_all_books()
            self.docs = [doc['title'] for doc in docs_dict]

        self.docs_clean = nlpservice.helpers.prefilter_data(self.docs)

    def _gen_corpus(self, save=True):
        """ 
        Create the document-term matrix (corpus) from the given titles.

        Args:
            save (bool): defaults to true, save the generated corpus to a file
        """

        self.corpus = [
            self.dictionary.doc2bow(filtered_title)
            for filtered_title in self.docs_clean
        ]

        if save:
            self._save_corpus()

    def _load_corpus(self):
        """
        Load corpus (the documents/terms matrix) from a file. If the corpus
        file does not exist, generate it, including other necessary data, using
        by default the data from the MySQL database.
        """
        if os.path.exists(self.corpus_filename):
            self.corpus = gensim.corpora.MmCorpus(self.corpus_filename)
            self._load_doc_id_maps()
        else:
            self._gen_corpus(self.docs_clean)
            self._gen_doc_id_maps(self.docs)

    def _save_corpus(self):
        """ 
        Save corpus (the document/term matrix) to a file
        """
        gensim.corpora.MmCorpus.serialize(self.corpus_filename, self.corpus)

    def _gen_doc_id_maps(self, save=True):
        """
        Generate doc/ID mappings 

        Args:
            save (bool): defaults to true, save the generated doc/ID maps to a
            file 
        """
        self.doc_to_id = dict(zip(self.docs, range(len(self.docs))))
        self.id_to_doc = dict(zip(range(len(self.docs)), self.docs))
        if save:
            self._save_doc_id_maps()

    def _load_doc_id_maps(self):
        """
        Try to load the doc-ID mapping files. If it does not exist, generate it 
        directly.
        """
        if os.path.exists(self.doc_to_id_filename) and os.path.exists(
                self.id_to_doc_filename):
            doc_to_id_file = open(self.doc_to_id_filename, "rb")
            self.doc_to_id = pickle.load(doc_to_id_file)
            doc_to_id_file.close()

            id_to_doc_file = open(self.id_to_doc_filename, "rb")
            self.id_to_doc = pickle.load(id_to_doc_file)
            id_to_doc_file.close()
        else:
            self._gen_doc_id_maps(self.docs)

    def _save_doc_id_maps(self):
        """
        Save the two doc-ID mappings to files
        """
        doc_to_id_file = open(self.doc_to_id_filename, "wb")
        pickle.dump(self.doc_to_id, doc_to_id_file)
        doc_to_id_file.close()

        id_to_doc_file = open(self.id_to_doc_filename, "wb")
        pickle.dump(self.id_to_doc, id_to_doc_file)
        id_to_doc_file.close()

    def _gen_dictionary(self, save=True):
        """
        Generate the dictionary of terms contained in the clean data

        Args:
            save (bool): defaults to true, save the generated dictionary to a
            file
        """
        self.dictionary = gensim.corpora.Dictionary(self.docs_clean)

        if save:
            self._save_dictionary()

    def _save_dictionary(self):
        """
        Save the dictionary to a file
        """
        self.dictionary.save(self.dictionary_filename)

    def _load_dictionary(self):
        """
        Load the dictionary from file or generate it if the file does not exist
        """
        if os.path.exists(self.dictionary_filename):
            self.dictionary = gensim.corpora.Dictionary.load(
                self.dictionary_filename)
        else:
            self._gen_dictionary()

    def _gen_lsi_model(self, nb_topics=5, save=True):
        """
        Generate LSI model

        Args:
            nb_topics (int): number of topics to generate
            save (bool): defaults to true, save the generated LSI model to a
            file
        """
        tfidf_model = gensim.models.TfidfModel(self.corpus,
                                               id2word=self.dictionary)

        self.lsi_model = gensim.models.LsiModel(tfidf_model[self.corpus],
                                                id2word=self.dictionary,
                                                num_topics=nb_topics)

        if save:
            self._save_lsi_model()

    def _save_lsi_model(self):
        """
        Save LSI model to a file
        """
        self.lsi_model.save(self.lsi_model_filename)

    def _load_lsi_model(self, nb_topics=5):
        """
        Load LSI model from a file or generate it if the file does not exist
        """
        if os.path.exists(self.lsi_model_filename):
            self.lsi_model = gensim.models.LsiModel.load(
                self.lsi_model_filename)
        else:
            self._gen_lsi_model(nb_topics=nb_topics)

    def _gen_vectors(self, save=True):
        """
        Generate the vectors for each document

        Args:
            save (bool): defaults to true, save the generated vectors to a
            file
        """
        self.vectors = [self.lsi_model[title_bow] for title_bow in self.corpus]

        if save:
            self._save_vectors()

    def _load_vectors(self):
        """
        Load the vectors from a file or generate them if the file does not
        exist.
        """
        if os.path.exists(self.vectors_filename):
            vectors_file = open(self.vectors_filename, "rb")
            self.vectors = pickle.load(vectors_file)
            vectors_file.close()
        else:
            self._gen_vectors()

    def _save_vectors(self):
        """
        Save the vectors to a file
        """
        vectors_file = open(self.vectors_filename, "wb")
        pickle.dump(self.vectors, vectors_file)
        vectors_file.close()

    def _gen_similarities(self, save=True):
        """
        Generate the similarities matrix from the corpus

        Args:
            save (bool): defaults to true, save the generated similarities
            matrix to a file
        """
        # corpus_lfi = self.lsi_model[self.corpus]
        self.similarities = gensim.similarities.MatrixSimilarity(
            self.lsi_model[self.corpus])

        if save:
            self._save_similarities()

    def _load_similarities(self):
        """
        Load the similarities matrix from a file or generate it if it does not
        exist
        """
        if os.path.exists(self.similarities_filename):
            self.similarities = gensim.similarities.MatrixSimilarity.load(
                self.similarities_filename)
        else:
            self._gen_similarities()

    def _save_similarities(self):
        """
        Save the similarities matrix to a file
        """
        self.similarities.save(self.similarities_filename)

    def pre_setup(self, docs=None):
        """
        Load the documents, the dictionary and the corpus

        Args:
            docs (list of strings): optional, pass the documents directly as 
            an arg instead of querying the DB
        """

        print("Presetting...")
        self._load_docs(docs=docs)
        self._load_dictionary()
        self._load_corpus()

    def setup(self, nb_topics=5):
        """
        Load the LSI model, the vectors and the similarities matrix.

        Args:
            nb_topics (int): number of topics for the LSI model
        """
        print("Final setting up")

        self._load_lsi_model(nb_topics=nb_topics)
        self._load_vectors()
        self._load_similarities()

    def _vector(self, doc):
        """
        Lookup a doc if it has been vectorised and calculate it otherwise.

        Args:
            doc (string): the document

        Returns:
            vector
        """
        if doc in self.doc_to_id:
            doc_id = self.doc_to_id[doc]
            return self.vectors[doc_id]

        prefiltered_doc = nlpservice.helpers.prefilter_data([doc])

        if len(prefiltered_doc) != 1:
            raise ValueError("error with vector for doc '%s'" % doc)

        doc_bow = self.dictionary.doc2bow(prefiltered_doc[0])
        return self.lsi_model[doc_bow]

    def top_books(self, doc, author=None, top_nb_docs=10):
        """
        Get top most similar documents based on given document.

        Args:
            doc (string): document to be compared to
            top_nb_docs (int): the number of top documents to recommend
    
        Returns:
            list of strings: top documents recommended
        """

        vector = self._vector(doc)
        similarities_vector = self.similarities.get_similarities(vector)

        # sort top `top_nb_docs` books following their degree of similarity
        # with our document and get their titles
        # discard the first document of the list as it is the one we are
        # comparing to
        top_books = []
        for book_id, weight in sorted(
                enumerate(similarities_vector),
                key=lambda weight: -weight[1])[1:top_nb_docs + 1]:

            top_books.append((self.id_to_doc[book_id], weight.item()))

        if author is not None:
            with warnings.catch_warnings() as w:
                books = self._same_author_books(author)
                same_author = [(book, 0) for book in books]
                same_author += top_books
                top_books = same_author
                print(w)

        return top_books

    def append_author(self, top_books):
        """
        Get the author's name for each book in the given list of titles.
        
        Args:
            top_books (dict): titles and their weight
            (result from top_books) to query for the author
        
        Returns:
            dict: titles, their author, their weight
        """
        books = []
        for title, weight in top_books:
            author = self.mysqlcli.get_book_author(title)
            if author == "":
                author = "not_found"
                warnings.warn(("author for title %s not found" % title),
                              UserWarning)

            books.append({'title': title, 'author': author, 'weight': weight})

        return books

    def _same_author_books(self, author):
        """
        Search for books with the same author in the MySQL DB
        
        Args:
            author (string): the author's name 

        Returns:
            list of strings: the list of books with the same author
        """
        books = self.mysqlcli.get_author_books(author)
        books = [book["title"] for book in books]
        # books.remove(title)

        return books

    def ideal_nb_topics(self, min_nb_topics, max_nb_topics):
        """
        Compute the coherance value for several number of topics and return the
        ideal number of topics to be used in the LSI model. 

        Args:
            min_nb_topics (int): minimum number of topics to test with
            max_nb_topics (int): maximum number of topics to test with

        Returns:
            int: the ideal number of topics
        """

        print("Calculating the ideal number of topics...")

        coherence_values = []
        model_list = []

        for nb_topics in range(min_nb_topics, max_nb_topics):
            model = gensim.models.LsiModel(self.corpus,
                                           num_topics=nb_topics,
                                           id2word=self.dictionary)
            model_list.append(model)
            coherencemodel = gensim.models.coherencemodel.CoherenceModel(
                model=model,
                texts=self.docs_clean,
                dictionary=self.dictionary,
                coherence='c_v')
            coherence_values.append(
                (nb_topics, coherencemodel.get_coherence()))

        ideal_nb_topics = sorted(coherence_values, key=lambda x: -x[1])[0][0]

        return ideal_nb_topics

    @staticmethod
    def jsonify_recommender_result(books):
        """
        Convert the recommender top_books method's result to a JSON string.

        Args:
            books (dict): the top books recommended by the top_books method

        Returns:
            string: books in JSON format
        """

        return json.dumps(books)
