import Rhino
from Rhino.DocObjects import ObjectType
from Rhino.Input.Custom import OptionDouble
from data.data_access import DataAccess
from data.room_factory import _is_valid_room_geometry
from Rhino.Input import GetResult

class GetRoom(Rhino.Input.Custom.GetObject):

    def __init__(self):
        self._room_name = "1g_Office_01"

        # set env variables for command
        self.GeometryFilter = ObjectType.Brep | ObjectType.Surface | ObjectType.Curve | ObjectType.Hatch

        self.option_double = OptionDouble(100.0, 0.0, 100000.0)
        target_area_index = self.AddOptionDouble("TargetArea", self.option_double, "Specify target Area")

        self.name_index = self.AddOption("RoomName", self._room_name)

        self.SetCustomGeometryFilter(GetRoom._filter)

        self.SetCommandPrompt("Select geo to generate room for.")

        #self.AcceptNothing(False)

    def get_room(self):

        while True:
            self.Get()

            if self.Result() == GetResult.Object | GetResult.Cancel:
                return

            if self.Result() == GetResult.Option:
                option = self.Option()
                if option.Index == self.name_index:
                    self.room_name = option.StringOptionValue

            return

    @staticmethod
    def _filter(rhObj, geo, ci):
        return _is_valid_room_geometry(geo)

    @property
    def target_area(self):
        return self.option_double.CurrentValue

    @property
    def room_name(self):
        return self._room_name

    @room_name.setter
    def room_name(self, value):
        self._room_name = value
