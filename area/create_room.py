import Rhino
from Rhino.DocObjects import ObjectType
from data.data_access import DataAccess

def create_room(id, sIdentifier, dTargetArea):

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    access.create_room(id, sIdentifier, dTargetArea)

def main():
    # get object
    result, objRef = Rhino.Input.RhinoGet.GetOneObject("Select room geometry", False, ObjectType.Brep | ObjectType.Curve | ObjectType.Surface | ObjectType.Hatch)
    if result != Rhino.Commands.Result.Success:
        return result

    # # get identifier
    # sIdent = ""
    # result = Rhino.Input.RhinoGet.GetString("Specifiy ident", False, sIdent)
    # print(sIdent)
    # if not sIdent: return

    # # get target Area
    # result, dArea = Rhino.Input.RhinoGet.GetNumber("Specify target area", False)
    # if result != Rhino.Commands.Result.Success:
    #     return result

    # call actual function
    # create_room(objRef.ObjectId, sIdent, dArea)
    create_room(objRef.ObjectId, "Test", 100)


if __name__ == "__main__":
    main()