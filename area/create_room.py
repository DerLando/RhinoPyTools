import Rhino
from Rhino.DocObjects import ObjectType
from data.data_access import DataAccess
from get_room import GetRoom

def create_room(id, sIdentifier, dTargetArea):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    access.create_room(id, sIdentifier, dTargetArea)

def main():
    # get object
    gr = GetRoom()

    gr.get_room()

    if gr.CommandResult() != Rhino.Commands.Result.Success:
        return gr.Result

    create_room(gr.Object(0).ObjectId, gr.room_name, gr.target_area)


if __name__ == "__main__":
    main()