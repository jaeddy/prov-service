import uuid
import json

from prov_service.models.activity import Activity
from prov_service.mock.dict import ActivityClasses
from prov_service.util import get_datetime


class MockActivity(Activity):

    def __init__(self, name='', class_idx=0):
        super().__init__(name=name)
        self.id = str(uuid.uuid1())
        self._class = ActivityClasses[class_idx]
        self.created_at = get_datetime()
        self.label = 'Activity'
        self.openapi_types.update({'label': str})

    def select_class(self, class_idx):
        self._class = ActivityClasses[class_idx]

    def get_class_count(self):
        return len(ActivityClasses)

