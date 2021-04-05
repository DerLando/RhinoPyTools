from data.roomdata import RoomData
from data.room_factory import RoomFactory
from Rhino import RhinoDoc
from distutils.util import strtobool

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

    def _room_exists(self, attrs):
        return bool(strtobool(attrs.GetUserString(ROOM_USER_KEY)))

    def _room_name(self, attrs):
        return attrs.GetUserString(ROOM_IDENTIFIER_KEY)

    def _room_target_area(self, attrs):
        return float(attrs.GetUserString(ROOM_TARGET_AREA_KEY))

    def create_room(self, id, sIdentifier, dTargetArea):
        # get geometry
        geo = self._get_geo(id)

        # create room object
        room = RoomFactory.create_from_geo(geo, sIdentifier, dTargetArea)

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
        # error handling
        error = "DataAccess.read_room ERROR: "

        # try to retrieve attrs for id from doc
        attrs = self._get_attributes(id)
        if not attrs:
            print(error + "could not find attributes for id: " + str(id))
            return

        # try to retrieve geo from doc
        geo = self._get_geo(id)
        if not geo:
            print(error + "could not find geo for id: " + str(id))

        # check if a room exists
        bExists = self._room_exists(attrs)
        if not bExists:
            print(error + "No room exists for id: " + str(id))

        # retrieve room fields from doc
        sIdentifier = self._room_name(attrs)
        dTargetArea = self._room_target_area(attrs)

        # create room object
        room = RoomFactory.create_from_geo(geo, sIdentifier, dTargetArea)

        # check if we could create a valid room, error out if not
        if not room:
            print("DataAccess.read_room ERROR: Could not read a valid room for id: " + str(id))
            return
        
        return room

    def update_room(self, id, sIdentifier=None, dTargetArea=None):
        pass

    def delete_room(self, id):
        pass
