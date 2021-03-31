from roomdata import RoomData
import Rhino
from Rhino.Geometry import GeometryBase, Brep, Surface, Curve, Hatch, AreaMassProperties
from Rhino.DocObjects import ObjectType

def _is_valid_brep(brep):
    pass

def _is_valid_surface(srf):
    pass

def _is_valid_curve(crv):
    return crv.IsValid and crv.IsClosed and crv.IsPlanar()

def _is_valid_hatch(hatch):
    pass

def _is_valid_room_geometry(geo):
    # test the different geo types
    if geo.ObjectType == ObjectType.Brep:
        return _is_valid_brep(geo)

    if geo.ObjectType == ObjectType.Surface:
        return _is_valid_surface(geo)

    if geo.ObjectType == ObjectType.Curve:
        return _is_valid_curve(geo)

    if geo.ObjectType == ObjectType.Hatch:
        return _is_valid_hatch(geo)

    return False

def _calculate_area(geo):
    # calculate amp
    amp = AreaMassProperties.Compute(geo)

    # test result
    error_message = "Room._calculate_area ERROR: "
    if not amp:
        print(error_message + "Invalid area")
        return

    # TODO: Handle AreaError property to introduce certainty

    return amp.Area

class Room(object):

    def __init__(self, poco):
        self.poco = poco

    @staticmethod
    def create_from_geo(geo, sIdentifier, dTargetArea):

        # validate input
        error_message = "Room.create_from_geo ERROR: "
        if not geo:
            print(error_message + "No valid geo")
            return
        elif not isinstance(geo, GeometryBase):
            print(error_message + "No valid geo")
            return
        elif not geo.IsValid:
            print(error_message + "No valid geo")
            return
        elif not _is_valid_room_geometry(geo):
            print(error_message + "No valid geo")
            return
        
        # calculate area
        dArea = _calculate_area(geo)

        if not dArea:
            return

        # create room poco
        poco = RoomData(sIdentifier, dTargetArea, dArea)

        return Room(poco)
        
