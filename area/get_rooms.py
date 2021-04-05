import Rhino
from data.data_access import DataAccess
from Rhino.DocObjects import ObjectType

def get_rooms():

    # get doc 
    doc = Rhino.RhinoDoc.ActiveDoc

    # open data access
    access = DataAccess(doc)

    # create room from id
    return access.get_rooms()

def main():
    for room in get_rooms():
        print(room)

if __name__ == "__main__":
    main()