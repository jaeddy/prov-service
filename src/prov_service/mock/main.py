import sys
import time
import logging
import argparse

from random import randrange
from py2neo import NodeMatcher

from prov_service.config import driver
from prov_service.graph.shim import Graph
from prov_service.mock.models.activity import MockActivity
from prov_service.mock.mocker import ActivityMocker
from prov_service.graph.client import GraphClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

graph = Graph(driver)
matcher = NodeMatcher(graph)

# ------------------------------
NUMACTIVITIES = 30
# ------------------------------


def add_activities(kt):
    result = graph.run(
        '''
        MATCH (:Activity)
        RETURN count(*) as count
        '''
    )
    offset = result[0]['count']
    x = []
    for i in range(kt):
        tmp = MockActivity(name='Activity_' + str(i+1+offset),
                           class_idx=0)
        tmp.select_class(randrange(tmp.get_class_count()))
        x.append(tmp)
        time.sleep(0.5)
    return x


def create_mock_graph(graph_client, NUMACTIVITIES):
    # SCRIPT

    # step 1 - Create activities:
    logger.info("Generating table of Activities...")
    activity_array = add_activities(NUMACTIVITIES)

    # step 2 - Create corresponding nodes and relationships
    # for each activity:
    ref_num = 0
    agt_num = 0
    for i in activity_array:
        logger.info("Building Activity '{}' of class '{}'"
                     .format(i.name, i._class))
        act = ActivityMocker(graph_client, i, ref_num, agt_num)
        (rn, an) = act.save()
        ref_num += rn
        agt_num += an


# read input parameters
parser = argparse.ArgumentParser(
    description='Generate sample provenance records.'
)
parser.add_argument('nActivities',
                    metavar='#Activities',
                    type=int,
                    nargs='+',
                    default=30,
                    help='number of Activities')


def main():
    args = parser.parse_args()

    # update reference values if needed
    NUMACTIVITIES = args.nActivities[0]

    gc = GraphClient(graph)
    create_mock_graph(gc, NUMACTIVITIES)


if __name__ == "__main__":
    main()