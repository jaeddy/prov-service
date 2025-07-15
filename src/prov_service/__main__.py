#!/usr/bin/env python3
import os
import logging

import connexion
import click

from prov_service import create_app
from prov_service.config import driver
from prov_service.graph.shim import Graph
from prov_service.graph.client import GraphClient
from prov_service.mock.main import create_mock_graph


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
graph = Graph(driver)

def init_db(num_activities=30):
    graph.delete_all()
    logger.info("Populating mock graph")
    create_mock_graph(GraphClient(graph), num_activities)


@click.command()
@click.option(
    '--mock_db',
    flag_value=True,
    show_default=True,
    help=("Initialize Neo4j database with mock graph records")
)
@click.option(
    '--db_size',
    default=50,
    show_default=True,
    help=("Number of mock activity records to create in the "
          "graph database (ignored if 'init_db' is False).")
)
def main(mock_db, db_size):
    app = create_app()

    if mock_db:
        init_db(db_size)

    env_host = os.environ.get('FLASK_HOST')
    flask_host = env_host if env_host is not None else 'localhost'
    app.run(host=flask_host, port=8080)


if __name__ == '__main__':
    main()
