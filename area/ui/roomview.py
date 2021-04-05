import Rhino
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
from ui.mainviewmodel import MainViewModel

class RoomView(Rhino.UI.Forms.CommandDialog):

    def __init__(self):
        self._model = MainViewModel()
        self.Title = "Rooms"
        self.Size = drawing.Size(400,800)
        self.ShowHelpButton = False
        self.Content = self.__create_layout()

    def __create_layout(self):
        layout = forms.TableLayout()
        layout.Padding = drawing.Padding(4)
        layout.Spacing = drawing.Size(4, 4)

        grid = self.__create_grid()
        row = forms.TableRow(grid)
        row.ScaleHeight = True
        layout.Rows.Add(row)

        return layout

    def __create_grid(self):
        grid = forms.GridView()
        grid.Size = drawing.Size(300, 400)
        grid.ShowHeader = True

        # name column
        column_name = forms.GridColumn()
        column_name.HeaderText = "Name"
        column_name.Editable = True
        column_name.DataCell = forms.TextBoxCell(0)
        grid.Columns.Add(column_name)

        # target area column
        column_target = forms.GridColumn()
        column_target.HeaderText = "Target Area"
        column_target.Editable = True
        column_target.DataCell = forms.TextBoxCell(1)
        grid.Columns.Add(column_target)

        # actual area column
        column_area = forms.GridColumn()
        column_area.HeaderText = "Area"
        column_area.Editable = False
        column_area.DataCell = forms.TextBoxCell(2)
        grid.Columns.Add(column_area)

        # data store
        self.__set_datastore(grid)
        
        return grid

    def __set_datastore(self, control):
        names = []
        targetAreas = []
        actualAreas = []

        for room in self._model._rooms:
            names.append(room.name)
            targetAreas.append(room.target_area)
            actualAreas.append(room.actual_area)

        self._collection = [list(i) for i in zip(names, targetAreas, actualAreas)]

        control.DataStore = self._collection

    def get_collection(self):
        return self._collection

    def _update_model(self):
        for i in range(len(self._collection)):
            self._model._rooms[i].name = self._collection[i][0]
            self._model._rooms[i].target_area = float(self._collection[i][1])

    def apply_changes(self):
        # update model
        self._update_model()

        # apply changes
        self._model.apply_changes()
