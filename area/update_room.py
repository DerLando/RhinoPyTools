import Rhino
from data.data_access import DataAccess
from Rhino.DocObjects import ObjectType

def update_room(id, sIdentifier=None, dTargetArea=None):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    access.update_room(id, sIdentifier, dTargetArea)

def main():
    # get object for room
    result, objRef = Rhino.Input.RhinoGet.GetOneObject("Select room geometry", False, ObjectType.Brep | ObjectType.Curve | ObjectType.Surface | ObjectType.Hatch)
    if result != Rhino.Commands.Result.Success:
        return result

    update_room(objRef.ObjectId, "updated", 400)

if __name__ == "__main__":
    main()