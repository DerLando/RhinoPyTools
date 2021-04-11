import Rhino
from Rhino.DocObjects import ObjectType
from Rhino.Input.Custom import OptionDouble
from area.data.data_access import DataAccess
from area.data.room_factory import _is_valid_room_geometry

class GetRoom(Rhino.Input.Custom.GetObject):

    def __init__(self):
        # set env variables for command
        self.GeometryFilter = ObjectType.Brep | ObjectType.Surface | ObjectType.Curve | ObjectType.Hatch

        self.option_double = OptionDouble(100.0, 0.0, 100000.0)
        target_area_index = self.AddOptionDouble("TargetArea", self.option_double, "Specify target Area")

        name_index = self.AddOption("RoomName", "1G_Office_01")

        self.SetCustomGeometryFilter(GetRoom._filter)

        self.SetCommandPrompt("Select geo to generate room for.")

        self.AcceptNothing(False)

    @staticmethod
    def _filter(rhObj, geo, ci):
        return _is_valid_room_geometry(geo)
