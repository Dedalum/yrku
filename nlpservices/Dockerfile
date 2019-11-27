FROM python:3

ADD app.py /
ADD nlpservice/*.py /nlpservice/
ADD requirements.txt /
RUN pip install -r requirements.txt

VOLUME /nlprecommend_data

CMD [ "python", "app.py" ]
