FROM python:3.8.0-slim

ADD app.py /
ADD nlpservice/*.py /nlpservice/
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords')"

VOLUME /nlprecommend_data
VOLUME /config.ini

CMD [ "python", "app.py" ]
