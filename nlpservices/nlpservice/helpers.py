"""helpers functions for NLP packages"""

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def prefilter_data(titles_list):
    """
    Tokenize book titles with a stemmer, remove stop words, lemmetize. We
    assume text is in English.

    Args
        data (list of str): list of book titles to filter

    Returns:
        list of list of str: the lemmetized and filtered titles
    """

    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words('english'))
    p_stemmer = PorterStemmer()

    filtered_titles = []

    for title in titles_list:
        raw_title = title.lower()
        tokens = tokenizer.tokenize(raw_title)
        tokens = [t for t in tokens if t not in en_stop]
        tokens = [p_stemmer.stem(i) for i in tokens]

        filtered_titles.append(tokens)

    return filtered_titles
