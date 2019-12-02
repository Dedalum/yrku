# Webapp

This webapp uses php framework Laravel. It allows for handling book lists:
- adding a new book
- delete a book
- display all books
- export all books in CSV or XML format, optionally filtering out the author or
the titles
- display a specific book and recommendations for it

_Note: the database used for the webapp is different than the one used in the NLP
service, where only a list of books used for training the LSI model is present.
The LSI model therefore does not update according to given input from the 
webapp._

## Table of contents

- [Tools](#tools)
- [Development](#development)
- [Usage](#usage)
- [TODO](#todo)

## Tools
The Makefile allows to perform tasks:
```
init                           Install dependencies
dockerize                      Dockerize
help                           Display this message
```

## Usage

The app uses the `.env` for Laravel envrionment variables, including the
connection to MySQL DB, and `config/nlp_api.php` for configuring variables
related to the NLP services API.

### Routes

```
/               # Home
/books          # Books: displays all saved books, has the export button, the
                add button. Each book has an icon for deleting it and clicking
                on the title brings to its specific page.
/book/{id}      # Displays the information on a specific book. A recommend button
                alllows for requesting a book recommendation.
/login          # Login in order to get access to the book functionalities.

```

### NLP API config file

The configuration file `config/nlp_api.php`: 
```
<?php
return [
    'host' => 'http://localhost:5000'   // the host and port for the NLP API
];
```

## TODO

- more complete testing: the XML/CSV exports downloaded files have to be checked
but cannot manage to get the downloaded file
(`Storage::disk('local')->assertExists($dir)` gives no suche file in that path);
see dusk tests


