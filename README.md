# Yaraku assignment

## Architecture

``` 
    --
   |DB|-----------
    --           |
    |         ------------
    |        |NLP services|
    |         ------------ 
    |            |
   ----          |
  | BE |----------  
   ----  
    |
    |
   ----
  | FE |
   ----
```
- The database (DB) is MySQL DB running in a Docker container
- The NLP services are the micro-services expecting an input from the backend
(BE) (book title, optionally the author) and returning a result in JSON format
(by default). Each services run in their own containers, independant from the 
other parts of the system. They have read access to the DB.
- the backend (BE) handles with the frontend (FE) the web application. The BE 
has read and write accesses to the BD (add and delete a book). 

## NLP services
The NLP services are micro-services running in their containers and serve the
backend with their results (recommended books or grouping of books).

### Recommend function

## Web application


## Database
The database used is a MySQL DB running in a Docker container.


## TODO
- check accesses to DB: more thorough restrictions
