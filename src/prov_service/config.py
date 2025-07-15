#!/usr/bin/env python3
import logging
import os
import time
import connexion

from neo4j import GraphDatabase, NotificationMinimumSeverity

from prov_service.util import is_open


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


connex_app = connexion.App(__name__, specification_dir='./openapi/')

env_host = os.environ.get('NEO4J_HOST')
neo4j_host = env_host if env_host is not None else '0.0.0.0'
env_port = os.environ.get('NEO4J_PORT')
neo4j_port = env_port if env_port is not None else 7687
env_scheme = os.environ.get('NEO4J_SCHEME')
neo4j_scheme = env_scheme if env_scheme is not None else 'bolt'

neo_user = os.environ['NEO4J_USERNAME']
neo_pass = os.environ['NEO4J_PASSWORD']

while not is_open(neo4j_host, neo4j_port):
    time.sleep(1)
else:
    driver = GraphDatabase.driver(
        f'{neo4j_scheme}://{neo4j_host}:{neo4j_port}',
        auth=(neo_user, neo_pass),
        # notifications_min_severity=NotificationMinimumSeverity.OFF,
    )


