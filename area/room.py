from roomdata import RoomData
import Rhino
from Rhino.Geometry import GeometryBase, Brep, Surface, Curve, Hatch, AreaMassProperties, Vector3d
from Rhino.DocObjects import ObjectType

def _is_same_plane_direction(planeA, planeB):
    return planeA.ZAxis.IsParallelTo(planeB.ZAxis) == 1

def _get_plane(brepFace):
    u = brepFace.Domain(0).Min
    v = brepFace.Domain(1).Min

    bSuccess, frame = brepFace.FrameAt(u, v)
    return frame

def _is_valid_brep(brep):
    # single face breps are easy
    if brep.Faces.Count == 1:
        return brep.IsValid and brep.Faces[0].IsPlanar()

    # test if all brep faces are planar
    if not all([face.IsPlanar() for face in brep.Faces]):
        return False

    # TODO: Test if all brep faces share the same plane direction (ZAxis)
    frame = _get_plane(brep.Faces[0])
    return all([_is_same_plane_direction(frame, _get_plane(face)) for face in brep.Faces])


def _is_valid_surface(srf):
    return srf.IsValid and srf.IsPlanar()

def _is_valid_curve(crv):
    return crv.IsValid and crv.IsClosed and crv.IsPlanar()

def _is_valid_hatch(hatch):
    return hatch.IsValid

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

class RoomFactory(object):
    """
    A static factory helper class, to generate
    RoomData from different inputs.
    """

    @staticmethod
    def create_from_geo(geo, sIdentifier, dTargetArea):
        """Creates RoomData from the given geometry.

        Args:
            geo (GeometryBase): The geometry of the room
            sIdentifier (String): The identifier or name of the room
            dTargetArea (double): The area the room should have

        Returns:
            RoomData: The RoomData created
        """

        # validate input
        error_message = "RoomFactory.create_from_geo ERROR: "
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
        return RoomData(sIdentifier, dTargetArea, dArea)
        
