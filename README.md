# Provenance Service

Lightweight implementation of the Synapse Activity services, based on the PROV spec.

> [!CAUTION]
> This project is exploratory in nature and under construction.

## Overview

This is an OpenAPI-enabled (and documented) Flask server. The app uses the [**Connexion**](https://github.com/zalando/connexion) library with Flask to connect the underlying API specification to server routes and operations. The [**`neo4j`**](https://github.com/neo4j/neo4j-python-driver) driver library for Python is used to manage operations between RESTful API requests/responses and a Neo4j database.


## Requirements

+ Python 3.9+ (should be taken care of with `uv`)
+ uv (see [installation instructions](https://docs.astral.sh/uv/getting-started/installation/))
+ docker (optional but recommended)

You should have access to a local installation of Neo4j, serving at `bolt://localhost/7687`.

<sup>*</sup>*You can set up a Neo4j database instance using the provided `docker-compose.yml` file, following the instructions below.

You'll also need to set two environment variables based on your Neo4j configuration (the Flask app uses these to connect to the database):

```shell
export NEO4J_USERNAME=<username> # must be 'neo4j'
export NEO4J_PASSWORD=<password>
```

### Running Neo4j with Docker

To run Neo4j in a Docker container, execute the following from the root directory (do this _**after**_ setting the environment variables above):

```shell
docker-compose up
```

> [!NOTE]
> In order to use the container to establish a Neo4j database connection, you should have [Docker Compose](https://docs.docker.com/compose/overview/) installed.

After running this command, the URLs in the sections below should work.


## Usage

To run the server, you can use this command (from the root directory):

```shell
uv run prov-service
```

> [!WARNING]
> The `--mock_db` option is not currently working as expected: the graph database will still be populated with representative activities, but each activity will be fully disconnected from the others.

To initialize the graph database with mock activity records, you can run the app with additional parameters:
```shell
uv run prov-service --mock_db --db_size 30
```

To view the full set of parameters:
```shell
uv run prov-service --help
```

```shell
Usage: prov-service [OPTIONS]

Options:
  --mock_db          Initialize Neo4j database with mock graph records
                     [default: False]
  --db_size INTEGER  Number of mock activity records to create in the graph
                     database (ignored if 'init_db' is False).  [default: 50]
  --help             Show this message and exit.
```

### Swagger UI

You can also interact with the graph database through RESTful API queries. The service provides a Swagger UI endpoint to test requests through the browser:

```
http://localhost:8080/rest/v1/ui/
```

*If the above URL doesn't work, try this instead:*

```
http://0.0.0.0:8080/rest/v1/ui/
```

![provenance swagger ui](img/swaggerui.png)


The OpenAPI definition lives here:

```
http://localhost:8080/rest/openapi.json
```

### Neo4j Browser

If you have the **Neo4j Desktop** application installed, you should be able to view and explore the graph database using Cypher queries. For example, to view all nodes and relationships:

```cypher
MATCH (n) RETURN n LIMIT 1000
```

Assuming that you populated the graph database with mock/example records as described above, you should see something that looks like this (minus the custom colors):

![example provenance graph](img/mockprov.png)









