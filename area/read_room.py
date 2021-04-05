import Rhino
from data.data_access import DataAccess
from Rhino.DocObjects import ObjectType

def read_room(id):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    return access.read_room(id)

def main():
    # get object for room
    result, objRef = Rhino.Input.RhinoGet.GetOneObject("Select room geometry", False, ObjectType.Brep | ObjectType.Curve | ObjectType.Surface | ObjectType.Hatch)
    if result != Rhino.Commands.Result.Success:
        return result

    room = read_room(objRef.ObjectId)

    print(room)

if __name__ == "__main__":
    main()