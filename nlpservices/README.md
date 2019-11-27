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
In a virtualenv:
```
pip install -r requirements.txt
```

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

- `Wizard's First Rule (Sword of Truth, nb.1)` not found (although in DB)
- remove possible duplicates in method `top_books` when we call it with 
`use_author=True` 
- deploy with Nginx, Gunicorn (instead of using the development Flask server)
- add logger and add more error checks, warnings 
- finish testing
 
### Improvements

- load data safely ? precompute and push to specific DB ?
- `pickle` python package not secure (only load trusted data - in our case, 
to simplify, we'll assume our data is safe)
- lemmatization (instead of stemming); see Krovetz stemmer/lemmetizer
- discard books with a score too little (as they might not be relevant)
