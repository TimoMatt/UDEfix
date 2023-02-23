from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidgetItem import QDMListWidgetItem
from fixpointtool.content.fpt_mapping import FPTMapping
from nodeeditor.utils import dumpException


class MissingFunctionError(Exception):
    pass


class QListWidgetPopup(QListWidget):
    def __init__(self, popup, index, type, parent=None):
        super().__init__(parent)

        if type == "n-tuple":
            self.itemDoubleClicked.connect(lambda item: QDMContentListWidgetNTuplePopup.launchTuplePopup(popup, index, item))

        elif type == "set":
            self.itemDoubleClicked.connect(lambda item: QDMContentListWidgetNTuplePopup.launchSetPopup(popup, index, item))


class QDMContentListWidgetNTuplePopup(QDialog):

    def __init__(self, tup, types_of_tuple, excluded_mapping=None, parent=None):
        super().__init__(parent)

        self.tup = tup
        self.types_of_tuple = types_of_tuple

        self.accessDicts = AccessDictionaries()

        self.setWindowTitle("Edit tuple")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 100)

        self.content_label = QLabel("Content:")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.content_label)

        mappings = list(self.accessDicts.getDictionaryWithoutTransformation("mappings").keys())
        if excluded_mapping is not None:
            mappings.pop(mappings.index(excluded_mapping))

        self.content = []

        for i in range(len(self.types_of_tuple)):
            current_type = self.types_of_tuple[i]

            content_box = QHBoxLayout()

            if current_type == "string":
                lbl = QLabel("String:")
                lbl.setMargin(4)
                sp = lbl.sizePolicy()
                sp.setHorizontalPolicy(QSizePolicy.Expanding)
                lbl.setSizePolicy(sp)

                le = QLineEdit(self.tup[i])

                self.content.append(le)
                content_box.addWidget(lbl)
                content_box.addWidget(le)
            elif current_type == "number":
                lbl = QLabel("Number:")
                lbl.setMargin(4)
                sp = lbl.sizePolicy()
                sp.setHorizontalPolicy(QSizePolicy.Expanding)
                lbl.setSizePolicy(sp)

                le = QLineEdit(str(self.tup[i]))

                self.content.append(le)
                content_box.addWidget(lbl)
                content_box.addWidget(le)
            elif current_type == "mapping":
                lbl = QLabel("Mapping:")
                lbl.setMargin(4)

                cb = QComboBox()
                cb.addItems(mappings)
                if self.tup[i] is not None:
                    cb.setCurrentText(self.tup[i].name)

                self.content.append(cb)
                content_box.addWidget(lbl)
                content_box.addWidget(cb)
            elif current_type[0] == "n-tuple":
                lbl = QLabel("Tuple:")
                lbl.setMargin(4)

                lw = QListWidgetPopup(self, i, "n-tuple")
                lw.setMaximumHeight(24)
                lw.setMaximumWidth(136)
                newItem = QDMListWidgetItem(self.tup[i], "n-tuple")
                lw.addItem(newItem)

                self.content.append(lw)
                content_box.addWidget(lbl)
                content_box.addWidget(lw)
            elif current_type[0] == "set":
                lbl = QLabel("Set:")
                lbl.setMargin(4)

                lw = QListWidgetPopup(self, i, "set")
                lw.setMaximumHeight(24)
                lw.setMaximumWidth(136)
                newItem = QDMListWidgetItem(self.tup[i], "set")
                lw.addItem(newItem)

                self.content.append(lw)
                content_box.addWidget(lbl)
                content_box.addWidget(lw)

            self.vbox.addLayout(content_box)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.setDefault(False)
        self.save_button.setAutoDefault(False)
        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)
        self.save_button.clicked.connect(self.onSave)
        self.cancel_button.clicked.connect(self.onCancel)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.cancel_button)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

    def launchTuplePopup(self, i, item):
        try:
            default_tuple = []
            for j in range(len(self.types_of_tuple[i][1])):
                if self.types_of_tuple[i][1][j] == "string":
                    default_tuple.append("")
                elif self.types_of_tuple[i][1][j] == "number":
                    default_tuple.append(0)
            pop = QDMContentListWidgetNTuplePopup(tuple(default_tuple), self.types_of_tuple[i][1])
            if pop.exec():
                item.item = pop.tup
                item.overwriteText()
        except Exception as e:
            print(e)

    def launchSetPopup(self, i, item):
        from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
        pop = QDMContentListWidgetInnerSetPopup(item.item, self.types_of_tuple[i][1])
        if pop.exec():
            item.item = pop.set
            item.overwriteText()

    def onSave(self):
        try:
            self.tup = []
            for i in range(len(self.types_of_tuple)):
                if self.types_of_tuple[i] == "string":
                    self.tup.append(self.content[i].text())
                elif self.types_of_tuple[i] == "number":
                    self.tup.append(float(self.content[i].text()))
                elif self.types_of_tuple[i] == "mapping":
                    mappingName = self.content[i].currentText()
                    if mappingName is not "":
                        self.tup.append(FPTMapping(mappingName))
                    else:
                        raise MissingFunctionError()
                elif self.types_of_tuple[i][0] == "n-tuple":
                    self.tup.append(self.content[i].item(0).item)
                elif self.types_of_tuple[i][0] == "set":
                    self.tup.append(self.content[i].item(0).item)
                else:
                    print("WARNING: Non-existing type")
            self.tup = tuple(self.tup)
            self.accept()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning:\nThere are inputs of a wrong type")
            msg.exec()
        except MissingFunctionError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning:\nThere are mappings missing")
            msg.exec()
        except Exception as e:
            dumpException(e)

    def onCancel(self):
        self.reject()
