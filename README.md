# Yaraku assignment

## Architecture

``` 
    --
   |DB|-----------
    --           |
    |         ------------
    |        |NLP service |
    |         ------------ 
    |            |
    |            |
    |-------------  
    |
    |
   --------
  | Webapp |
   --------
    |
    |
   -------                Private cloud/VM
--| Nginx |--------------------------------
   -------                Public internet

```
- The database (DB) is MySQL DB running in a Docker container
- The NLP service is the micro-services expecting an input from the webapp
(book title, optionally the author) and returning a result in JSON format. Each
service runs in its own container, independant from the other parts of
the system. The NLP service has read access to the DB.
- the webapp handles the web application. It has read and write accesses to
the DB (add and delete a book). 
- Nginx serves the webapp and is the only public facing service.

## NLP service

The NLP service is a micro-service running in its own container and serving the
webapp with its results (recommended books).

### Recommend function

The recommend function gives recommendations of book titles based on a given
title and optionally the author's name.

## Web application

The webapp displays the books from the DB entered by the user. A user can add
and delete books and get recommendations using the NLP service. It uses the 
Laravel framework.

_Note: when a user saves (adds) a new book, books are not automatically
recommended. I found simpler for the example to add a **Recommend** button 
instead._

## Database

The database used is a MySQL DB running in a Docker container. It has one 
database containing the books used for training the NLP LSI model used 

## TODO
- proper deployment (Ansible for instance)
- Kubernetes instead of docker-compose
- CI for tests, dockerizing (pushing to own docker hub) with TravisCI or 
gitlab-CI for instance
