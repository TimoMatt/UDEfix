from os import listdir

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_mapping import FPTMapping
from fixpointtool.fpt_import_dialog import FPTImportDialog
from fixpointtool.fpt_settings_dialog import FPTSettingsDialog
from nodeeditor.utils import dumpException, pp
from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from fixpointtool.fpt_sub_window import FPTSubWindow
from fixpointtool.fpt_drag_listbox import QDMDragListBox
from fixpointtool.fpt_conf import *
from fixpointtool.content.fpt_content_widget import QDMContentWidget
from fixpointtool.content.fpt_content import AccessDictionaries

DEBUG = False


def getContentDialogFilter():
    return 'Content (*.json);;All files (*)'


def getContentDialogDirectory():
    return 'fixpointtool/content'


class FPTWindow(NodeEditorWindow):
    listOfFPTWindows = []

    def initUI(self):
        self.name_author = "Timo Matt"
        self.name_product = "Fixpoint Tool"

        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

        self.content_file = config['all']['content']
        self.content_filename = os.path.join(os.path.join(os.path.dirname(__file__), "content"), self.content_file)

        self.content_changed = False

        # self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss")
            # self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")

        # if DEBUG:
        #     print("Registered nodes:")
        #     pp(FPT_NODES)

        self.accessDicts = AccessDictionaries()
        self.accessDicts.updateDictionariesFromJSONFile(self.content_filename)
        # self.accessDicts.saveDictionariesInJSONFile(self.content_filename)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()
        self.createContentsDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("Fixpoint Tool")

        FPTWindow.listOfFPTWindows.append(self)

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            if self.content_changed:
                res = QMessageBox.warning(self, "About to lose your work?",
                                          "The content has been modified.\n Do you want to save your changes?",
                                          QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

                if res == QMessageBox.Cancel:
                    event.ignore()
                    return
                if res == QMessageBox.Save:
                    self.onContentSave()

            self.writeSettings()
            event.accept()
            # hacky fix
            import sys
            sys.exit(0)

    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def onContentNew(self):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            return

        fname = os.path.join(os.path.dirname(__file__), os.path.join("content", FPTWindow.getNewContentName()))

        if fname != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

            if self.content_filename != fname:
                if self.content_changed:
                    res = QMessageBox.warning(self, "About to lose your work?",
                                              "The content has been modified.\n Do you want to save your changes?",
                                              QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

                    if res == QMessageBox.Cancel:
                        return False
                    if res == QMessageBox.Save:
                        self.onContentSave()

                self.content_file = os.path.basename(fname)
                self.content_filename = fname

                config['all']['content'] = self.content_file
                with open(os.path.join(os.path.dirname(__file__), "config.ini"), 'w') as configfile:
                    config.write(configfile)

                # delete function references
                FPTMapping.listOfInvalidFPTMappings.clear()
                FPTMapping.dictOfFPTMappings.clear()
                FPTMapping.dictOfMappings.clear()

                for key in self.accessDicts.getDictionaryWithoutTransformation("mappings"):
                    self.accessDicts.deleteElementFromDictionary("mappings", key)
                for key in self.accessDicts.getDictionaryWithoutTransformation("relations"):
                    self.accessDicts.deleteElementFromDictionary("relations", key)
                for key in self.accessDicts.getDictionaryWithoutTransformation("sets"):
                    self.accessDicts.deleteElementFromDictionary("sets", key)

                self.accessDicts.saveDictionariesInJSONFile(self.content_filename)
                self.accessDicts.updateDictionariesFromJSONFile(self.content_filename)

                self.contentWidget.setsListWidget.connectWithDictionary()
                self.contentWidget.allMappingsListWidget.connectWithDictionary()
                self.contentWidget.relationsListWidget.connectWithDictionary()

                self.content_changed = False

    def onContentOpen(self):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            return

        fname, filter = QFileDialog.getOpenFileName(self, "Open content from file", getContentDialogDirectory(), getContentDialogFilter())
        if fname != "" and os.path.isfile(fname):
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

            if self.content_filename != fname:
                if self.content_changed:
                    res = QMessageBox.warning(self, "About to lose your work?",
                                              "The content has been modified.\n Do you want to save your changes?",
                                              QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

                    if res == QMessageBox.Cancel:
                        return False
                    if res == QMessageBox.Save:
                        self.onContentSave()

                self.content_file = os.path.basename(fname)
                self.content_filename = fname

                config['all']['content'] = self.content_file
                with open(os.path.join(os.path.dirname(__file__), "config.ini"), 'w') as configfile:
                    config.write(configfile)

                # delete function references
                FPTMapping.listOfInvalidFPTMappings.clear()
                FPTMapping.dictOfFPTMappings.clear()
                FPTMapping.dictOfMappings.clear()

                self.accessDicts.updateDictionariesFromJSONFile(self.content_filename)

                self.contentWidget.setsListWidget.connectWithDictionary()
                self.contentWidget.allMappingsListWidget.connectWithDictionary()
                self.contentWidget.relationsListWidget.connectWithDictionary()

                self.content_changed = False

    def onContentSave(self):
        self.accessDicts.saveDictionariesInJSONFile(self.content_filename)
        self.content_changed = False

        self.statusBar().showMessage("Successfully saved content as %s" % self.content_filename, 5000)

    def onContentSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, "Save content to file", getContentDialogDirectory(), getContentDialogFilter())

        if fname == "": return False

        self.content_file = os.path.basename(fname)
        self.content_filename = fname

        self.accessDicts.saveDictionariesInJSONFile(self.content_filename)

        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

        config['all']['content'] = self.content_file

        with open(os.path.join(os.path.dirname(__file__), "config.ini"), 'w') as configfile:
            config.write(configfile)

        self.content_changed = False

        self.statusBar().showMessage("Successfully saved content as %s" % self.content_filename, 5000)

    def onImportContent(self):
        importWindow = FPTImportDialog()
        importWindow.exec()
        self.contentWidget.setsListWidget.connectWithDictionary()
        self.contentWidget.allMappingsListWidget.connectWithDictionary()
        self.contentWidget.relationsListWidget.connectWithDictionary()

    def onSettingsOpen(self):
        settingsWindow = FPTSettingsDialog()
        if settingsWindow.exec():
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

            # if config['all']['content'] != settingsWindow.content_directory_button.text():
            #     reply = QMessageBox.question(self, 'Window Close', 'Save content?', QMessageBox.Yes | QMessageBox.No,
            #                                  QMessageBox.No)
            #     if reply == QMessageBox.Yes:
            #         print("Content saved in", self.content_filename)
            #         self.accessDicts.saveDictionariesInJSONFile(self.content_filename)
            #
            #     self.mdiArea.closeAllSubWindows()
            #     if self.mdiArea.currentSubWindow():
            #         return

            # config['all']['content'] = settingsWindow.content_directory_button.text()
            config['all']['mv-algebra'] = settingsWindow.mv_algebra_comboBox.currentText()
            config['all']['k'] = settingsWindow.mv_algebra_k_lineEdit.text()

            with open(os.path.join(os.path.dirname(__file__), "config.ini"), 'w') as configfile:
                config.write(configfile)

            # self.content_file = config['all']['content']
            # self.content_filename = os.path.join(os.path.join(os.path.dirname(__file__), "content"), self.content_file)
            #
            # # delete function references
            # FPTMapping.listOfInvalidFPTMappings.clear()
            # FPTMapping.dictOfFPTMappings.clear()
            # FPTMapping.dictOfMappings.clear()
            #
            # self.accessDicts.updateDictionariesFromJSONFile(self.content_filename)
            #
            # self.contentWidget.setsListWidget.connectWithDictionary()
            # self.contentWidget.allMappingsListWidget.connectWithDictionary()
            # self.contentWidget.relationsListWidget.connectWithDictionary()

            updateMVAlgebra()

    def getCurrentNodeEditorWidget(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, "Open graph from file",
                                                      self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # create new subWindow and open the file
                        nodeeditor = FPTSubWindow(self)
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def about(self):
        QMessageBox.about(self, "About Fixpoint Tool",
                          "<b>TODO</b>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        # self.helpMenu = self.menuBar().addMenu("&Help")
        # self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_functions = self.windowMenu.addAction("Basic functions Toolbar")
        toolbar_functions.setCheckable(True)
        toolbar_functions.triggered.connect(self.onWindowNodesToolbar)
        toolbar_functions.setChecked(self.functionsDock.isVisible())

        toolbar_content = self.windowMenu.addAction("Content Toolbar")
        toolbar_content.setCheckable(True)
        toolbar_content.triggered.connect(self.onWindowContentToolbar)
        toolbar_content.setChecked(self.contentDock.isVisible())

        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.functionsDock.isVisible():
            self.functionsDock.hide()
        else:
            self.functionsDock.show()

    def onWindowContentToolbar(self):
        if self.contentDock.isVisible():
            self.contentDock.hide()
        else:
            self.contentDock.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListBox()

        self.functionsDock = QDockWidget("Basic functions")
        self.functionsDock.setWidget(self.nodesListWidget)
        self.functionsDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.functionsDock)

    def createContentsDock(self):
        self.contentWidget = QDMContentWidget(self)

        self.contentDock = QDockWidget("Content")
        self.contentDock.setWidget(self.contentWidget)
        self.contentDock.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.contentDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else FPTSubWindow(self)
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    @staticmethod
    def getNewContentName():
        onlyfiles = [f for f in listdir(getContentDialogDirectory()) if os.path.isfile(os.path.join(getContentDialogDirectory(), f))]
        newContentName = "content_"
        counter = 1
        while True:
            if newContentName + str(counter) + ".json" not in onlyfiles:
                return newContentName + str(counter) + ".json"
            counter += 1
