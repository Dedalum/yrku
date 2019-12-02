# NLP recommend function

## Table of contents

- [Tools](#tools)
- [Development](#development)
- [Usage](#usage)
- [TODO](#todo)

## Tools
The Makefile allows to perform tasks:
```
init                           Install dependencies
test                           Run tests
dockerize                      Dockerize
help                           Display this message
```

## Development

### Setup
In a virtualenv:
```
pip install -r requirements.txt
```

### API and recommend function

The recommend function returns book recommendations based on a given title
and optionally an author's name:

1. Generate an LSI model, trained with data from a specific training list of 
books in the DB
2. Run the API (in Flask) and serve request for recommendations. Responses are 
lists of book titles and their authors in JSON format.


## Usage

The app expects a configuration file in the same directory called 
`config.ini`.

### Configuration file

The configuration file `config.ini.example` provides an example of the
configuration: 
```
[DEFAULT]

[mysql]
host = localhost
user = nlp-recommend
password = example
db = db1
```

### Structure

```
nlpservice/recommend.py     # recommend module: main module for computing the
                            LSI model and recommending books
nlpservice/mysqlci.py       # MySQL client module
nlpservice/helpers.py       # helpers modules: contains functions to clean and
                            tokenize data
app.py                      # main app, running a simple Flask API
config.ini                  # configuration file

```

## TODO

- add logger and add more error checks, warnings 
- deploy with Nginx, Gunicorn (instead of using the development Flask server)
 
### Ideas and improvements

- `pickle` python package not secure (only load trusted data - in our case, 
to simplify, we'll assume our data is safe)
- lemmatization (instead of stemming); see Krovetz stemmer/lemmetizer
- discard books with a score too little (as they might not be relevant)
