from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidgetItem import QDMListWidgetItem
from fixpointtool.content.fpt_content_listWidget_inner_n_tuple_popup import QDMContentListWidgetNTuplePopup
from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
from fixpointtool.content.fpt_content_listWidget_inner_tuple_popup import QDMContentListWidgetTuplePopup
from nodeeditor.utils import dumpException

DEBUG = False


class QDMMappingEdit(QWidget):
    def __init__(self, input_type, output_type, mapping, input_tuple_type=None, output_tuple_type=None, input_set_type=None, output_set_type=None, input_set=None, output_set=None, input_mv=None, input_mv_k=None, output_mv=None, output_mv_k=None):
        super().__init__()

        self.accessDict = AccessDictionaries()

        self.input_type = input_type
        self.output_type = output_type
        self.mapping_name = mapping

        self.input_tuple_type = input_tuple_type
        self.output_tuple_type = output_tuple_type
        self.input_set_type = input_set_type
        self.output_set_type = output_set_type
        self.input_set = input_set
        self.output_set = output_set

        self.input_mv = input_mv
        self.input_mv_k = input_mv_k
        self.output_mv = output_mv
        self.output_mv_k = output_mv_k

        if DEBUG:
            print("Domain:", self.input_set)
            print("Codomain:", self.output_set)

        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 1)

        self.setLayout(self.vbox)
        self.setStyleSheet("background-color: #474747")

    def onInputSetClicked(self, item):
        pop = QDMContentListWidgetInnerSetPopup(item.item, self.input_set_type, excluded_mapping=self.mapping_name)
        if pop.exec():
            item.item = pop.set
            item.overwriteText()

    def onOutputSetClicked(self, item):
        pop = QDMContentListWidgetInnerSetPopup(item.item, self.output_set_type, excluded_mapping=self.mapping_name)
        if pop.exec():
            item.item = pop.set
            item.overwriteText()

    def onInputTupleClicked(self, item):
        pop = QDMContentListWidgetNTuplePopup(item.item, self.input_tuple_type, excluded_mapping=self.mapping_name)
        if pop.exec():
            item.item = pop.tup
            item.overwriteText()

    def onOutputTupleClicked(self, item):
        pop = QDMContentListWidgetNTuplePopup(item.item, self.output_tuple_type, excluded_mapping=self.mapping_name)
        if pop.exec():
            item.item = pop.tup
            item.overwriteText()

    def addMapping(self, arg=None, val=None):
        try:
            if DEBUG:
                print(self.input_type)
                print(self.input_tuple_type)
                print(self.input_set_type)
                print(self.output_type)
                print(self.output_tuple_type)
                print(self.output_set_type)

            newMapping = QWidget()
            newMapping.setFixedHeight(32)
            newHBox = QHBoxLayout()
            newMapping.setLayout(newHBox)

            checkBox = QCheckBox()
            checkBox.setFixedSize(15, 23)
            # checkBox.setStyleSheet("background: #666")

            if arg is None and self.input_set is None:
                if self.input_type == "string":
                    arg = ""
                elif self.input_type == "number":
                    arg = 0
                elif self.input_type == "mapping":
                    arg = None
                elif self.input_type == "n-tuple":
                    tup = []
                    for i in range(len(self.input_tuple_type)):
                        if self.input_tuple_type[i] == "string":
                            tup.append("")
                        elif self.input_tuple_type[i] == "number":
                            tup.append(0)
                        elif self.input_tuple_type[i] == "mapping":
                            tup.append(None)
                        elif self.input_tuple_type[i][0] == "n-tuple":
                            innerTup = []
                            for j in range(len(self.input_tuple_type[i][1])):
                                innerTup.append(0 if self.input_tuple_type[i][1][j] == "number" else "")
                            tup.append(tuple(innerTup))
                        elif self.input_tuple_type[i][0] == "set":
                            tup.append(frozenset())
                    arg = tuple(tup)
                elif self.input_type == "set":
                    arg = frozenset()

            if val is None and self.output_set is None:
                if self.output_type == "string":
                    val = ""
                elif self.output_type == "number":
                    val = 0
                elif self.output_type == "mapping":
                    val = None
                elif self.output_type == "n-tuple":
                    tup = []
                    for i in range(len(self.output_tuple_type)):
                        if self.output_tuple_type[i] == "string":
                            tup.append("")
                        elif self.output_tuple_type[i] == "number":
                            tup.append(0)
                        elif self.output_tuple_type[i] == "mapping":
                            tup.append(None)
                        elif self.output_tuple_type[i][0] == "n-tuple":
                            innerTup = []
                            for j in range(len(self.output_tuple_type[i][1])):
                                innerTup.append(0 if self.output_tuple_type[i][1][j] == "number" else "")
                            tup.append(tuple(innerTup))
                        elif self.output_tuple_type[i][0] == "set":
                            tup.append(frozenset())
                    val = tuple(tup)
                if self.output_type == "set":
                    val = frozenset()

            arrow = QLabel("\u21A6")
            arrow.setAlignment(QtCore.Qt.AlignCenter)
            arrow.setFixedHeight(23)
            # arrow.setFixedWidth(24)

            sp = arrow.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            arrow.setSizePolicy(sp)

            arrow.setStyleSheet("font-size: 36px")

            if self.input_set is None and self.input_mv is None:
                if self.input_type == "string" or self.input_type == "number":
                    newInput = QLineEdit(str(arg))
                    newInput.setFixedHeight(23)
                    newInput.setStyleSheet("background:#666")
                elif self.input_type == "n-tuple":
                    newInput = QListWidget()
                    newInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    newInput.setFixedHeight(23)
                    newInput.itemDoubleClicked.connect(self.onInputTupleClicked)
                    newItem = QDMListWidgetItem(arg, "n-tuple")
                    newInput.addItem(newItem)
                elif self.input_type == "set":
                    newInput = QListWidget()
                    newInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    newInput.setFixedHeight(23)
                    newInput.itemDoubleClicked.connect(self.onInputSetClicked)
                    newItem = QDMListWidgetItem(arg, "set")
                    newInput.addItem(newItem)
                elif self.input_type == "mapping":
                    newInput = QComboBox()
                    newInput.setFixedHeight(23)
                    # newInput.setMinimumWidth(100)
                    mappings = list(self.accessDict.getDictionaryWithoutTransformation("mappings").keys())
                    mappings.remove(self.mapping_name)
                    newInput.addItems(mappings)
                    if arg is not None:
                        newInput.setCurrentText(arg.name)
            elif self.input_set is None:
                newInput = QLineEdit(str(arg))
                newInput.setFixedHeight(23)
                newInput.setStyleSheet("background:#666")

                if self.input_mv == "algebra 1":
                    onlyDouble = QDoubleValidator(0.0, float(self.input_mv_k), 5)
                    onlyDouble.setNotation(QtGui.QDoubleValidator.StandardNotation)
                    onlyDouble.setLocale(QtCore.QLocale("en"))
                    newInput.setValidator(onlyDouble)
                    newInput.textChanged.connect(lambda text: self.checkForRange(newInput, text, self.input_mv_k))
                elif self.input_mv == "algebra 2":
                    if len(newInput.text()) > 1 and newInput.text()[-2:] == ".0": newInput.setText(newInput.text()[:-2])
                    onlyInt = QIntValidator(0, int(self.input_mv_k))
                    onlyInt.setLocale(QtCore.QLocale("en"))
                    newInput.setValidator(onlyInt)
                    newInput.textChanged.connect(lambda text: self.checkForRange(newInput, text, self.input_mv_k, type="int"))

            else:
                newInput = QComboBox()
                newInput.setFixedHeight(23)
                # newInput.setMinimumWidth(100)
                items = list(self.accessDict.getDictionaryWithoutTransformation("sets")[self.input_set])
                newList = []
                if self.input_type == "set":
                    for item in items:
                        newList.append(str(set(item)))
                elif self.input_type == "n-tuple" and self.input_tuple_type[0] == "set":
                    for item in items:
                        newList.append(str(tuple([set(innerItem) for innerItem in item])))
                        # newList.append(str(tuple([set(item[0]), set(item[1])])))
                else:
                    for item in items:
                        newList.append(str(item))

                newInput.addItems(newList)

                if arg is not None:
                    if self.input_type == "set":
                        newInput.setCurrentText(str(set(arg)))
                    elif self.input_type == "n-tuple" and self.input_tuple_type == "set":
                        newInput.setCurrentText(str(tuple([set(innerItem) for innerItem in arg])))
                        # newInput.setCurrentText(str(tuple([set(arg[0]), set(arg[1])])))
                    else:
                        newInput.setCurrentText(str(arg))

            if self.output_set is None and self.output_mv is None:
                if self.output_type == "string" or self.output_type == "number":
                    newOutput = QLineEdit(str(val))
                    newOutput.setFixedHeight(23)
                    newOutput.setStyleSheet("background:#666")
                elif self.output_type == "n-tuple":
                    newOutput = QListWidget()
                    newOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    newOutput.setFixedHeight(23)
                    newOutput.itemDoubleClicked.connect(self.onOutputTupleClicked)
                    newItem = QDMListWidgetItem(val, "n-tuple")
                    newOutput.addItem(newItem)
                elif self.output_type == "set":
                    newOutput = QListWidget()
                    newOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    newOutput.setFixedHeight(23)
                    newOutput.itemDoubleClicked.connect(self.onOutputSetClicked)
                    newItem = QDMListWidgetItem(val, "set")
                    newOutput.addItem(newItem)
                elif self.output_type == "mapping":
                    newOutput = QComboBox()
                    newOutput.setFixedHeight(23)
                    # newOutput.setMinimumWidth(100)
                    mappings = list(self.accessDict.getDictionaryWithoutTransformation("mappings").keys())
                    mappings.remove(self.mapping_name)
                    newOutput.addItems(mappings)
                    if val is not None:
                        newOutput.setCurrentText(val.name)
            elif self.output_set is None:
                newOutput = QLineEdit(str(val))
                newOutput.setFixedHeight(23)
                newOutput.setStyleSheet("background:#666")

                if self.output_mv == "algebra 1":
                    onlyDouble = QDoubleValidator(0.0, float(self.output_mv_k), 5)
                    onlyDouble.setNotation(QtGui.QDoubleValidator.StandardNotation)
                    onlyDouble.setLocale(QtCore.QLocale("en"))
                    newOutput.setValidator(onlyDouble)
                    newOutput.textChanged.connect(lambda text: self.checkForRange(newOutput, text, self.output_mv_k))
                elif self.output_mv == "algebra 2":
                    if len(newOutput.text()) > 1 and newOutput.text()[-2:] == ".0": newOutput.setText(newOutput.text()[:-2])
                    onlyInt = QIntValidator(0, int(self.output_mv_k))
                    onlyInt.setLocale(QtCore.QLocale("en"))
                    newOutput.setValidator(onlyInt)
                    newOutput.textChanged.connect(lambda text: self.checkForRange(newOutput, text, self.output_mv_k, type="int"))
            else:
                newOutput = QComboBox()
                newOutput.setFixedHeight(23)
                # newOutput.setMinimumWidth(100)
                items = list(self.accessDict.getDictionaryWithoutTransformation("sets")[self.output_set])
                newList = []
                if self.output_type == "set":
                    for item in items:
                        newList.append(str(set(item)))
                elif self.output_type == "n-tuple" and self.output_tuple_type == "set":
                    for item in items:
                        newList.append(str(tuple([set(innerItem) for innerItem in item])))
                        # newList.append(str(tuple([set(item[0]), set(item[1])])))
                else:
                    for item in items:
                        newList.append(str(item))

                newOutput.addItems(newList)

                if val is not None:
                    if self.output_type == "set":
                        newOutput.setCurrentText(str(set(val)))
                    elif self.output_type == "n-tuple" and self.output_tuple_type == "set":
                        newOutput.setCurrentText(str(tuple([set(innerItem) for innerItem in val])))
                        # newOutput.setCurrentText(str(tuple([set(val[0]), set(val[1])])))
                    else:
                        newOutput.setCurrentText(str(val))

            newInput.setMinimumWidth(105)
            newOutput.setMinimumWidth(105)
            newInput.setMaximumWidth(105)
            newOutput.setMaximumWidth(105)

            newHBox.addWidget(checkBox)
            newHBox.addWidget(newInput)
            newHBox.addWidget(arrow)
            newHBox.addWidget(newOutput)

            self.vbox.addWidget(newMapping)
        except Exception as e:
            dumpException(e)

    def checkForRange(self, input, text, top, type="double"):
        try:
            if type == "double":
                if len(text) > 0:
                    if "," in text:
                        input.setText(text.replace(",", "."))
                    if float(text) > float(top):
                        input.setText(top)
            elif type == "int":
                if len(text) > 0:
                    if "," in text:
                        input.setText(text.replace(",", ""))
                    if int(text) > int(top):
                        input.setText(top)
        except ValueError:
            pass
        except Exception as e:
            dumpException(e)

    def addMappings(self, list_of_arguments, list_of_values):
        for i in range(0, len(list_of_arguments)):
            self.addMapping(list_of_arguments[i], list_of_values[i])

    def deleteCheckedMappings(self):
        toBeDeleted = []
        for i in range(self.vbox.count()):
            children = self.vbox.itemAt(i).widget().children()
            if children[1].isChecked():
                toBeDeleted.append(i)
        toBeDeleted.reverse()

        for index in toBeDeleted:
            self.vbox.removeWidget(self.vbox.itemAt(index).widget())

    def getMappings(self):
        list_of_mappings = []
        for i in range(self.vbox.count()):
            mapping = []
            children = self.vbox.itemAt(i).widget().children()
            if self.input_set is None:
                if self.input_type == "string" or self.input_type == "number":
                    mapping.append(children[2].text())
                elif self.input_type == "mapping":
                    mapping.append(children[2].currentText())
                elif self.input_type == "set" or self.input_type == "n-tuple":
                    mapping.append(children[2].item(0).item)
            else:
                mapping.append(children[2].currentText())

            if self.output_set is None:
                if self.output_type == "string" or self.output_type == "number":
                    mapping.append(children[4].text())
                elif self.output_type == "mapping":
                    mapping.append(children[4].currentText())
                elif self.output_type == "set" or self.output_type == "n-tuple":
                    mapping.append(children[4].item(0).item)
            else:
                mapping.append(children[4].currentText())

            list_of_mappings.append(mapping)

        return list_of_mappings
