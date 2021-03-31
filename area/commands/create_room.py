import Rhino
from Rhino.DocObjects import ObjectType
from data_access import DataAccess

def create_room(id, sIdentifier, dTargetArea):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # oben data access
    access = DataAccess(doc)

    # create room from id
    access.create_room(id, sIdentifier, dTargetArea)

def main():
    # get object
    result, objRef = Rhino.RhinoGet.GetOneObject("Select room geometry", False, ObjectType.Brep | ObjectType.Curve | ObjectType.Surface | ObjectType.Hatch)
    if result != Rhino.Commands.Result.Success:
        return result

    # get identifier
    result, sIdent = Rhino.RhinoGet.GetString("Specifiy ident", False)
    if result != Rhino.Commands.Result.Success:
        return result

    # get target Area
    result, dArea = Rhino.RhinoGet.GetNumber("Specify target area", False)
    if result != Rhino.Commands.Result.Success:
        return result

    # call actual function
    create_room(objRef.ObjectId, sIdent, dArea)


if __name__ == "__main__":
    main()