import Rhino
import scriptcontext as sc
from data.data_access import DataAccess

class MainViewModel(object):

    def __init__(self):
        self._doc = sc.doc.ActiveDoc
        
        access = DataAccess(self._doc)

        self._rooms = access.get_rooms()

    def apply_changes(self):

        access = DataAccess(self._doc)

        for room in self._rooms:
            access.update_room(room.id, room.name, room.target_area)
