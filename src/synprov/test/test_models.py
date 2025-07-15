import logging
import pytest

from prov_service.models.activity import Activity
from prov_service.models.reference import Reference
from prov_service.graph.models.activity import GraphActivity
from prov_service.graph.models.reference import GraphReference
from prov_service.graph.models.agent import GraphAgent
# from prov_service.graph.builder import ActivityBuilder


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestActivity:

    def test_init(self, mock_graph):
        activity = GraphActivity(name='Activity_1')
        for a in Activity.attribute_map:
            assert hasattr(activity, a)

    def test__find_node_exists(self, mock_graph_data):
        activity = GraphActivity(name='Activity_1')
        a = activity._find_node(graph=mock_graph_data,
                                label='Activity',
                                properties={'name': 'Activity_1'})
        assert a[0]['name'] == 'Activity_1'



class TestReference:

    def test_init(self, mock_graph):
        reference = GraphReference(name='Reference_1')
        for a in Reference.attribute_map:
            assert hasattr(reference, a)
