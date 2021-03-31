class RoomData(object):
    """
    POCO for room components.
    
    """

    def __init__(self, sName, dTargetArea, dActualArea):
        self.name = sName
        self.target_area = dTargetArea
        self.actual_area = dActualArea
