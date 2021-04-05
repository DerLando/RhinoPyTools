from ui.roomview import RoomView
import Rhino

dialog = RoomView()

dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

if dialog.Result == Rhino.Commands.Result.Success:
    dialog.apply_changes()
    