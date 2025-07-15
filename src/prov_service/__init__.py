import logging
import connexion

from healthcheck import HealthCheck

from prov_service.config import connex_app, driver


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def neo4j_available():
    try:
        logger.info("Checking Neo4j connection")
        driver.verify_connectivity()
        return True, "Neo4j ok"
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")


def create_app():
    app = connex_app
    app.add_api('openapi.yaml',
                arguments={'title': 'Provenance Service'},
                pythonic_params=True)
    # wrap the flask app and give a heathcheck url
    health = HealthCheck()
    health.add_check(neo4j_available)
    app.add_url_rule(
        "/healthcheck", "healthcheck", 
        view_func=lambda: health.run()
    )


    return app








