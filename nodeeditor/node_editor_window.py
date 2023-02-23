import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nodeeditor.node_editor_widget import NodeEditorWidget


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.name_author = "Timo Matt"
        self.name_product = "Fixpoint Tool"

        self.initUI()

    def initUI(self):
        self.createActions()
        self.createMenus()

        # create node editor widget
        self.nodeeditor = NodeEditorWidget()
        self.nodeeditor.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.nodeeditor)

        self.createStatusBar()

        # set window property
        # self.setGeometry(200, 200, 800, 600)
        self.setTitle()
        self.show()

    def sizeHint(self):
        return QSize(800, 600)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

    def createActions(self):
        self.actNew = QAction("&New", self, shortcut="Ctrl+N", statusTip="Create new graph", triggered=self.onFileNew)
        self.actOpen = QAction("&Open", self, shortcut="Ctrl+O", statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction("&Save", self, shortcut="Ctrl+S", statusTip="Save File", triggered=self.onFileSave)
        self.actSaveAs = QAction("Save &as...", self, shortcut="Ctrl+A", statusTip="Save file as..", triggered=self.onFileSaveAs)
        self.actNewContent = QAction("New &Content", self, shortcut="Ctrl+Shift+N", statusTip="Create new content", triggered=self.onContentNew)
        self.actOpenContent = QAction("Open &Content", self, shortcut="Ctrl+Shift+O", statusTip="Open content", triggered=self.onContentOpen)
        self.actSaveContent = QAction("Save &Content", self, shortcut="Ctrl+Shift+S", statusTip="Save content", triggered=self.onContentSave)
        self.actSaveContentAs = QAction("Save Content &as...", self, shortcut="Ctrl+Shift+A", statusTip="Save content as..", triggered=self.onContentSaveAs)
        self.actImportContent = QAction("&Import content", self, shortcut="Ctrl+I", statusTip="Import content", triggered=self.onImportContent)
        self.actSettings = QAction("Se&ttings", self, shortcut="Ctrl+Alt+S", statusTip="Open settings", triggered=self.onSettingsOpen)
        self.actExit = QAction("E&xit", self, shortcut="Ctrl+Q", statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction("&Undo", self, shortcut="Ctrl+Z", statusTip="Undo last operation", triggered=self.onEditUndo)
        self.actRedo = QAction("&Redo", self, shortcut="Ctrl+Shift+Z", statusTip="Redo last operation", triggered=self.onEditRedo)
        self.actCut = QAction("Cu&t", self, shortcut="Ctrl+X", statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction("&Copy", self, shortcut="Ctrl+C", statusTip="Copy to clipboard", triggered=self.onEditCopy)
        self.actPaste = QAction("&Paste", self, shortcut="Ctrl+V", statusTip="Paste from clipboard", triggered=self.onEditPaste)
        self.actDelete = QAction("&Delete", self, shortcut="Del", statusTip="Delete selected items", triggered=self.onEditDelete)

    def createMenus(self):
        self.createFileMenu()
        self.createEditMenu()

    def createFileMenu(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu("&File")
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actNewContent)
        self.fileMenu.addAction(self.actOpenContent)
        self.fileMenu.addAction(self.actSaveContent)
        self.fileMenu.addAction(self.actSaveContentAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actImportContent)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actSettings)
        self.fileMenu.addAction(self.actExit)

    def createEditMenu(self):
        menubar = self.menuBar()
        self.editMenu = menubar.addMenu("&Edit")
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

    def setTitle(self):
        title = "Fixpoint Tool - "
        title += self.getCurrentNodeEditorWidget().getUserFriendlyFilename()

        self.setWindowTitle(title)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.getCurrentNodeEditorWidget().scene.isModified()

    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to lose your work?",
                                  "The graph has been modified.\n Do you want to save your changes?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def getFileDialogDirectory(self):
        return 'fixpointtool/graphs'

    def getFileDialogFilter(self):
        return 'Graph (*.json);;All files (*)'

    def onFileNew(self):
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().fileNew()
            self.setTitle()

    def onFileOpen(self):
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, "Open graph from file",
                                                        self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname != "" and os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().fileLoad(fname)
                self.setTitle()

    def onFileSave(self):
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.isFilenameSet(): return self.onFileSaveAs()

            current_nodeeditor.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_nodeeditor.filename, 5000)

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True

    def onFileSaveAs(self):
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, "Save graph to file",
                                                        self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname == "": return False

            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.filename, 5000)

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True

    def onContentNew(self):
        pass

    def onContentOpen(self):
        pass

    def onContentSave(self):
        pass

    def onContentSaveAs(self):
        pass

    def onSettingsOpen(self):
        pass

    def onEditUndo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        try:
            if self.getCurrentNodeEditorWidget():
                self.getCurrentNodeEditorWidget().scene.getView().deleteSelected()
        except Exception as e:
            print(e)

    def onEditCut(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            return self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)

    def readSettings(self):
        settings = QSettings(self.name_author, self.name_product)
        pos = settings.value("pos", QPoint(200, 400))
        size = settings.value("size", QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_author, self.name_product)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())