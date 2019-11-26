"""helpers functions for NLP packages"""

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def prefilter_data(titles_list):
    """
    Tokenize book titles with a stemmer, remove stop words, lemmetize. We
    assume text is in English.

    Args
        data (list of strings): list of book titles to filter

    Returns:
        list of list of strings: the lemmetized and filtered titles
    """

    # intialise tokenizer, keep words only and remove digits
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')

    # we use English stopwords
    en_stop = set(stopwords.words('english'))

    # create Porter stemmer
    p_stemmer = PorterStemmer()

    # list for tokenized documents in loop
    filtered_titles = []

    for title in titles_list:
        # clean and tokenize titles
        raw_title = title.lower()
        tokens = tokenizer.tokenize(raw_title)

        # remove (English) stop words from tokens
        tokens = [t for t in tokens if t not in en_stop]

        # stem tokens
        tokens = [p_stemmer.stem(i) for i in tokens]

        filtered_titles.append(tokens)

    return filtered_titles
