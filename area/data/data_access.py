from data.roomdata import RoomData
from data.room_factory import RoomFactory
from Rhino import RhinoDoc
from distutils.util import strtobool

ROOM_USER_KEY = "LPYT_AC_Enabled"
ROOM_IDENTIFIER_KEY = "LPYT_AC_RoomIdentifier"
ROOM_TARGET_AREA_KEY = "LPYT_AC_TargetArea"

class _RoomAttributes(object):
    """
    Helper class to map to and from ObjectAttributes
    """

    def __init__(self, attrs):
        self._attrs = attrs

    @property
    def exists(self):
        return bool(strtobool(self._attrs.GetUserString(ROOM_USER_KEY)))

    @exists.setter
    def exists(self, bExists):
        # TODO: Handle failure here as SetUserString returns a bool
        self._attrs.SetUserString(ROOM_USER_KEY, str(bExists))

    @property
    def identifier(self):
        return self._attrs.GetUserString(ROOM_IDENTIFIER_KEY)

    @identifier.setter
    def identifier(self, sIdentifier):
        # TODO: Handle failure here as SetUserString returns a bool
        self._attrs.SetUserString(ROOM_IDENTIFIER_KEY, sIdentifier)

    @property
    def target_area(self):
        return float(self._attrs.GetUserString(ROOM_TARGET_AREA_KEY))

    @target_area.setter
    def target_area(self, dTargetArea):
        # TODO: Handle failure here as SetUserString returns a bool
        self._attrs.SetUserString(ROOM_TARGET_AREA_KEY, str(dTargetArea))

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
        room = RoomFactory.create_from_geo(geo, sIdentifier, dTargetArea)

        # check if we could create a valid room, error out if not
        if not room:
            print("DataAccess.create_room ERROR: Could not create a valid room for id: " + str(id))
            return

        # get object attributes and set flags
        attrs = self._get_attributes(id)
        if not attrs: return

        # set flags on attrs
        room_attrs = _RoomAttributes(attrs)
        room_attrs.exists = True
        room_attrs.identifier = sIdentifier
        room_attrs.target_area = dTargetArea
        

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
            return

        # create room_attrs helper
        room_attrs = _RoomAttributes(attrs)

        # check if a room exists
        if not room_attrs.exists:
            print(error + "No room exists for id: " + str(id))
            return

        # create room object
        room = RoomFactory.create_from_geo(geo, room_attrs.identifier, room_attrs.target_area)

        # check if we could create a valid room, error out if not
        if not room:
            print("DataAccess.read_room ERROR: Could not read a valid room for id: " + str(id))
            return
        
        return room

    def update_room(self, id, sIdentifier=None, dTargetArea=None):
        # error handling
        error = "DataAccess.update_room ERROR: "

        # try to retrieve attrs for id from doc
        attrs = self._get_attributes(id)
        if not attrs:
            print(error + "could not find attributes for id: " + str(id))
            return

        # create attr mapping
        room_attrs = _RoomAttributes(attrs)

        # check if a room exists
        if not room_attrs.exists:
            print(error + "No room exists for id: " + str(id))
            return

        if sIdentifier:
            room_attrs.identifier = sIdentifier

        if dTargetArea:
            room_attrs.target_area = dTargetArea

        return

    def delete_room(self, id):
        # error handling
        error = "DataAccess.delete_room ERROR: "

        # try to retrieve attrs for id from doc
        attrs = self._get_attributes(id)
        if not attrs:
            print(error + "could not find attributes for id: " + str(id))
            return

        # create mapping
        room_attrs = _RoomAttributes(attrs)

        # set exits to false, deleting the room from queries
        room_attrs.exists = False

