import Rhino
from data.data_access import DataAccess
from Rhino.DocObjects import ObjectType

def delete_room(id):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    access.delete_room(id)

def main():
    # get object for room
    result, objRef = Rhino.Input.RhinoGet.GetOneObject("Select room geometry", False, ObjectType.Brep | ObjectType.Curve | ObjectType.Surface | ObjectType.Hatch)
    if result != Rhino.Commands.Result.Success:
        return result

    delete_room(objRef.ObjectId)

if __name__ == "__main__":
    main()