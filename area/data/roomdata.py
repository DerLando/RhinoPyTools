class RoomData(object):
    """
    POCO for room components.
    
    """

    def __init__(self, id, sName, dTargetArea, dActualArea):
        self.id = id
        self.name = sName
        self.target_area = dTargetArea
        self.actual_area = dActualArea

    def __str__(self):
        return "RoomData for room: {name} \n target_area: {ta} \n actual_area: {aa}".format(name=self.name, ta=self.target_area, aa=self.actual_area)
