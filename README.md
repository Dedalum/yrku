# Yaraku assignment

## Table of contents

- [Tools](#tools)
- [Development](#development)
- [TODO](#todo)

## Tools

### Deploy

The `deploy` directory contains the tools and directories used for a deployment
with Docker. Once in that directory, here are the steps to deploy the whole
stack: 
1. Copy the `.env.example` file to a file named `.env`. The default values of
the example file allow to run the stack without any changes.
2. Run the script `setup.sh`:
    1. Build the Docker images: `./setup.sh build_images`
    2. Generate the configuration files and start the DB: `./setup pre_setup`
    3. **Wait 20 seconds until the DB is ready**, then import the training the data
    `./setup.sh prepare_db`
    4. Start all other services: `./setup.sh start_all`
    5. Finally, setup the webapp: `./setup.sh setup_webapp`

The webapp is then accessible at the URL `localhost`. The content of the webapp
is accessible after logging in using the email and password defined in the 
`.env` file (defaulting to `admin@example.com` and password `example`).

## Development

### Architecture

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
service runs in its own container, independent from the other parts of
the system. The NLP service has read access to the DB.
- the webapp handles the web application. It has read and write accesses to
the DB (add and delete a book). 
- Nginx serves the webapp and is the only public facing service.

### NLP service

The NLP service is a micro-service running in its own container and serving the
webapp with its results (recommended books).

#### Recommend function

The recommend function gives recommendations of book titles based on a given
title and optionally the author's name.

### Web application

The webapp displays the books from the DB entered by the user. A user can add
and delete books and get recommendations using the NLP service. It uses the 
Laravel framework.

_Note: when a user saves (adds) a new book, books are not automatically
recommended. I found simpler for the example to add a **Recommend** button 
instead._

### Database

The database used is a MySQL DB running in a Docker container. It has one 
database containing the books used for training the NLP LSI model used 

## TODO

### Ideas and improvements

- deployment with a specific tool such as Ansible for instance
- Kubernetes instead of docker-compose
- CI for tests, dockerizing (pushing to own docker hub) with TravisCI or 
gitlab-CI for instance
- Letsencrypt for nginx
