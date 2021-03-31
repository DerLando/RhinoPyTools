from roomdata import RoomData
from room import Room
from Rhino import RhinoDoc

ROOM_USER_KEY = "LPYT_AC_Enabled"
ROOM_IDENTIFIER_KEY = "LPYT_AC_RoomIdentifier"
ROOM_TARGET_AREA_KEY = "LPYT_AC_TargetArea"

class DataAccess(object):
    """
    Data Access layer for rooms.
    Exposes CRUD Api
    """

    def __init__(self, doc):
        self.doc = doc

    def _get_obj(self, id):
        # find objRef in RhinoDoc for given id
        obj = self.doc.Objects.FindId(id)
        if not obj:
            print("DataAccess._get_ref ERROR: Could not find ref for id: " + str(id))
        
        return obj

    def _get_geo(self, id):
        obj = self._get_obj(id)
        if not obj: return

        return obj.Geometry

    def _get_attributes(self, id):
        obj = self._get_obj(id)
        if not obj: return

        return obj.Attributes

    def create_room(self, id, sIdentifier, dTargetArea):
        # get geometry
        geo = self._get_geo(id)

        # create room object
        room = Room.create_from_geo(geo, sIdentifier, dTargetArea)

        # check if we could create a valid room, error out if not
        if not room:
            print("DataAccess.create_room ERROR: Could not create a valid room for id: " + str(id))
            return

        # get object attributes and set flags
        attrs = self._get_attributes(id)
        if not attrs: return

        bSuccess = attrs.SetUserString(ROOM_USER_KEY, str(True))
        bSuccess = attrs.SetUserString(ROOM_IDENTIFIER_KEY, sIdentifier)
        bSuccess = attrs.SetUserString(ROOM_TARGET_AREA_KEY, str(dTargetArea))

        

    def read_room(self, id):
        pass

    def update_room(self, id, sIdentifier=None, dTargetArea=None):
        pass

    def delete_room(self, id):
        pass
