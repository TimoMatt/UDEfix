import copy

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import chain, combinations

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidgetItem import QDMListWidgetItem
from fixpointtool.content.fpt_content_listWidget_inner_n_tuple_popup import QDMContentListWidgetNTuplePopup
from fixpointtool.content.fpt_content_listWidget_inner_tuple_type_popup import QDMContentListWidgetTupleTypePopup
from fixpointtool.content.fpt_content_listWidget_mapping_popup import QDMContentListWidgetMappingPopup
from fixpointtool.content.fpt_content_listWidget_inner_set_popup import QDMContentListWidgetInnerSetPopup
from fixpointtool.content.fpt_content_listWidget_inner_tuple_popup import QDMContentListWidgetTuplePopup
from fixpointtool.content.fpt_mapping import FPTMapping
from fixpointtool.content.fpt_set import FPTSet
from fixpointtool.content.fpt_tuple import FPTTuple
from nodeeditor.utils import dumpException


class QDMContentListWidgetSetPopup(QDialog):
    # LIST_OF_TYPES = ["string", "number",  "mapping", "2-tuple", "k-tuple", "set_new", "set", "union", "intersection", "complement", "power set", "cross product", "n elements"]
    # LIST_OF_SET_TYPES = ["string", "number", "mapping", "2-tuple"]
    # LIST_OF_SET_NEW_TYPES = ["string", "number", "mapping", "k-tuple", "set_new"]
    # LIST_OF_TUPLE_TYPES = ["string", "number", "mapping", "2-tuple", "set"]

    LIST_OF_TYPES = ["string", "number", "mapping", "n-tuple", "set", "union", "intersection", "complement", "power set", "cross product", "n elements"]
    LIST_OF_SET_TYPES = ["string", "number", "mapping", "n-tuple"]
    LIST_OF_SET_NEW_TYPES = ["string", "number", "mapping"]
    LIST_OF_TUPLE_TYPES = ["string", "number", "mapping", "n-tuple", "set"]

    def __init__(self, name, dict, type_of_set, parent):
        super().__init__(parent)

        self.accessDicts = AccessDictionaries()
        self.dictionaryName = dict
        self.keyName = name
        self.contentOfDict = self.accessDicts.getDictionaryWithoutTransformation(self.dictionaryName)[self.keyName]

        self.setWindowTitle("Edit content")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 400)

        self.type_of_inner_set = "string"
        self.types_of_inner_tuple = ["string", "string"]
        self.size_of_inner_tuple = 2
        self.size_of_inner_set_tuple = 2
        if type_of_set == str:
            self.type_of_set = "string"
        elif type_of_set == int or type_of_set == float:
            self.type_of_set = "number"
        elif type_of_set == tuple:
            self.type_of_set = "n-tuple"
            for elem in self.accessDicts.getDictionaryWithoutTransformation(self.dictionaryName)[name]:
                self.types_of_inner_tuple = []
                self.size_of_inner_tuple = len(elem)
                for tupleElem in elem:
                    if type(tupleElem) == str:
                        self.types_of_inner_tuple += ["string"]
                    elif type(tupleElem) == int or type(tupleElem) == float:
                        self.types_of_inner_tuple += ["number"]
                    elif type(tupleElem) == frozenset or type(tupleElem) == set:
                        innerType = str
                        if len(tupleElem) > 0:
                            innerType = type(list(tupleElem)[0])
                        innerType = "string" if innerType == str else "number"
                        self.types_of_inner_tuple += [tuple(["set", innerType])]
                    elif type(tupleElem) == tuple:
                        self.types_of_inner_tuple += [tuple(["n-tuple", ["string" if type(innerTupleElem) == str else "number" for innerTupleElem in tupleElem]])]
                    elif type(tupleElem) == FPTMapping:
                        self.types_of_inner_tuple += ["mapping"]
                break
        elif type_of_set == frozenset or type_of_set == set:
            self.type_of_set = "set"
            for elem in self.accessDicts.getDictionaryWithoutTransformation(self.dictionaryName)[name]:
                if len(elem) > 0:
                    for innerElem in elem:
                        if type(innerElem) == str:
                            self.type_of_inner_set = "string"
                        elif type(innerElem) == int or type(innerElem) == float:
                            self.type_of_inner_set = "number"
                        elif type(innerElem) == tuple:
                            self.size_of_inner_set_tuple = len(innerElem)
                            self.type_of_inner_set = tuple(["n-tuple", ["string" if type(innerTupleElem) == str else "number" for innerTupleElem in innerElem]])
                        elif type(innerElem) == FPTMapping:
                            self.type_of_inner_set = "mapping"
                        break
                    break
        elif type_of_set == FPTMapping:
            self.type_of_set = "mapping"
        else:
            self.type_of_set = "string"

        self.name_label = QLabel("Name:")
        self.content_label = QLabel("Content:")
        self.type_label = QLabel("Type:")

        self.name_textEdit = QLineEdit(self.keyName)
        self.name_textEdit.setFixedHeight(23)
        self.name_textEdit.textChanged.connect(self.onNameChanged)

        self.subcontent_listWidget = QListWidget()
        self.subcontent_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectSetOfDictionary()

        self.type_comboBox = QComboBox()
        self.type_comboBox.addItems(QDMContentListWidgetSetPopup.LIST_OF_TYPES)
        self.type_comboBox.setCurrentText(self.type_of_set)
        self.type_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.setType_label = QLabel("Set type:")
        self.setType_label.setMargin(4)

        self.setType_comboBox = QComboBox()
        self.setType_comboBox.addItems(QDMContentListWidgetSetPopup.LIST_OF_SET_TYPES)
        if type(self.type_of_inner_set) == tuple:
            self.setType_comboBox.setCurrentText(self.type_of_inner_set[0])
        else:
            self.setType_comboBox.setCurrentText(self.type_of_inner_set)
        self.setType_comboBox.currentIndexChanged.connect(self.onInnerTypeChanged)

        self.setTypeBox = QHBoxLayout()
        self.setTypeBox.addWidget(self.setType_label)
        self.setTypeBox.addWidget(self.setType_comboBox)

        self.inner_tuple_n_label = QLabel("n")
        self.inner_tuple_n_label.setMargin(8)

        sp = self.inner_tuple_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.inner_tuple_n_label.setSizePolicy(sp)

        onlyInt = QIntValidator(2, 9)

        self.inner_tuple_n_lineEdit = QLineEdit()
        self.inner_tuple_n_lineEdit.setValidator(onlyInt)
        self.inner_tuple_n_lineEdit.setText(str(self.size_of_inner_set_tuple))
        self.inner_tuple_n_lineEdit.textChanged.connect(self.onInnerNChanged)

        self.inner_tuple_n_box = QHBoxLayout()
        self.inner_tuple_n_box.addWidget(self.inner_tuple_n_label)
        self.inner_tuple_n_box.addWidget(self.inner_tuple_n_lineEdit)

        self.inner_tupleType_label = QLabel("Tuple types:")
        self.inner_tupleType_label.setMargin(8)

        self.inner_tupleType_button = QPushButton("Edit")
        self.inner_tupleType_button.setDefault(False)
        self.inner_tupleType_button.setAutoDefault(False)
        self.inner_tupleType_button.clicked.connect(self.onInnerTypesButtonClicked)

        self.inner_tupleTypeBox = QHBoxLayout()
        self.inner_tupleTypeBox.addWidget(self.inner_tupleType_label)
        self.inner_tupleTypeBox.addWidget(self.inner_tupleType_button)

        self.tuple_n_label = QLabel("n:")
        self.tuple_n_label.setMargin(4)

        sp = self.tuple_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.tuple_n_label.setSizePolicy(sp)

        self.tuple_n_lineEdit = QLineEdit()
        self.tuple_n_lineEdit.setValidator(onlyInt)
        self.tuple_n_lineEdit.setText(str(self.size_of_inner_tuple))
        self.tuple_n_lineEdit.textChanged.connect(self.onNChanged)

        self.tuple_n_box = QHBoxLayout()
        self.tuple_n_box.addWidget(self.tuple_n_label)
        self.tuple_n_box.addWidget(self.tuple_n_lineEdit)

        self.tupleType_label = QLabel("Tuple types:")
        self.tupleType_label.setMargin(4)

        self.tupleType_button = QPushButton("Edit")
        self.tupleType_button.setDefault(False)
        self.tupleType_button.setAutoDefault(False)
        self.tupleType_button.clicked.connect(self.onTypesButtonClicked)

        self.tupleTypeBox = QHBoxLayout()
        self.tupleTypeBox.addWidget(self.tupleType_label)
        self.tupleTypeBox.addWidget(self.tupleType_button)

        allSets = self.accessDicts.getDictionaryWithoutTransformation("sets")
        allSets.pop(self.keyName)
        filteredForPowerset = []
        filteredForCrossproduct = []
        filteredForOthers = list(allSets)
        for elem in allSets:
            setType = str
            for innerElem in allSets[elem]:
                setType = type(innerElem)
                break
            if setType in [str, float, FPTMapping]:
                filteredForPowerset.append(elem)
                filteredForCrossproduct.append(elem)
            if setType in [tuple]:
                innerTupleTypes = []
                for innerElem in allSets[elem]:
                    for innerInnerElem in innerElem:
                        innerTupleTypes += [type(innerInnerElem)]
                    break
                allowed = True
                for tupleType in innerTupleTypes:
                    allowed = allowed and (tupleType in [str, float])
                if allowed:
                    filteredForPowerset.append(elem)
                    filteredForCrossproduct.append(elem)
            if setType in [frozenset]:
                innerSetType = str
                for innerElem in allSets[elem]:
                    done = False
                    for innerInnerElem in innerElem:
                        innerSetType = type(innerInnerElem)
                        done = True
                        break

                    if done:
                        break
                if innerSetType in [str, float]:
                    filteredForCrossproduct.append(elem)

        self.powerSet_label = QLabel("Choose set:")
        self.powerSet_label.setMargin(4)

        self.powerSet_comboBox = QComboBox()
        self.powerSet_comboBox.setFixedHeight(23)
        self.powerSet_comboBox.addItems(filteredForPowerset)
        self.powerSet_comboBox.currentIndexChanged.connect(self.loadPowerSet)

        self.powerSetBox = QHBoxLayout()
        self.powerSetBox.addWidget(self.powerSet_label)
        self.powerSetBox.addWidget(self.powerSet_comboBox)

        self.union1_label = QLabel("Choose first set:")
        self.union2_label = QLabel("Choose second set:")

        self.union1_comboBox = QComboBox()
        self.union2_comboBox = QComboBox()
        self.union1_comboBox.setFixedHeight(23)
        self.union2_comboBox.setFixedHeight(23)

        self.union1_comboBox.addItems(filteredForOthers)
        self.union2_comboBox.addItems(filteredForOthers)
        self.union1_comboBox.currentIndexChanged.connect(self.loadUnion)
        self.union2_comboBox.currentIndexChanged.connect(self.loadUnion)

        self.union1Box = QHBoxLayout()
        self.union2Box = QHBoxLayout()

        self.union1Box.addWidget(self.union1_label)
        self.union1Box.addWidget(self.union1_comboBox)
        self.union2Box.addWidget(self.union2_label)
        self.union2Box.addWidget(self.union2_comboBox)

        self.intersection1_label = QLabel("Choose first set:")
        self.intersection2_label = QLabel("Choose second set:")

        self.intersection1_comboBox = QComboBox()
        self.intersection2_comboBox = QComboBox()
        self.intersection1_comboBox.setFixedHeight(23)
        self.intersection2_comboBox.setFixedHeight(23)

        self.intersection1_comboBox.addItems(filteredForOthers)
        self.intersection2_comboBox.addItems(filteredForOthers)
        self.intersection1_comboBox.currentIndexChanged.connect(self.loadIntersection)
        self.intersection2_comboBox.currentIndexChanged.connect(self.loadIntersection)

        self.intersection1Box = QHBoxLayout()
        self.intersection2Box = QHBoxLayout()

        self.intersection1Box.addWidget(self.intersection1_label)
        self.intersection1Box.addWidget(self.intersection1_comboBox)
        self.intersection2Box.addWidget(self.intersection2_label)
        self.intersection2Box.addWidget(self.intersection2_comboBox)

        self.complement1_label = QLabel("Choose first set:")
        self.complement2_label = QLabel("Choose second set:")

        self.complement1_comboBox = QComboBox()
        self.complement2_comboBox = QComboBox()
        self.complement1_comboBox.setFixedHeight(23)
        self.complement2_comboBox.setFixedHeight(23)

        self.complement1_comboBox.addItems(filteredForOthers)
        self.complement2_comboBox.addItems(filteredForOthers)
        self.complement1_comboBox.currentIndexChanged.connect(self.loadComplement)
        self.complement2_comboBox.currentIndexChanged.connect(self.loadComplement)

        self.complement1Box = QHBoxLayout()
        self.complement2Box = QHBoxLayout()

        self.complement1Box.addWidget(self.complement1_label)
        self.complement1Box.addWidget(self.complement1_comboBox)
        self.complement2Box.addWidget(self.complement2_label)
        self.complement2Box.addWidget(self.complement2_comboBox)

        self.crossProduct_n_label = QLabel("n:")
        self.crossProduct_n_label.setMargin(4)

        sp = self.crossProduct_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.crossProduct_n_label.setSizePolicy(sp)

        self.crossProduct_n_lineEdit = QLineEdit()
        self.crossProduct_n_lineEdit.setValidator(onlyInt)
        self.crossProduct_n_lineEdit.setText(str(2))
        self.crossProduct_n_lineEdit.textChanged.connect(self.onCrossNChanged)

        self.crossProduct_n_box = QHBoxLayout()
        self.crossProduct_n_box.addWidget(self.crossProduct_n_label)
        self.crossProduct_n_box.addWidget(self.crossProduct_n_lineEdit)

        self.maxCrossProductSets = 9
        self.crossProduct_labels = []
        self.crossProduct_comboBoxes = []
        self.crossProduct_boxes = []

        for i in range(self.maxCrossProductSets):
            crossProduct_lbl = QLabel("Set " + str(i+1) + ":")
            crossProduct_lbl.setMargin(4)
            self.crossProduct_labels.append(crossProduct_lbl)

            crossProduct_cb = QComboBox()
            crossProduct_cb.setFixedHeight(23)
            crossProduct_cb.addItems(filteredForCrossproduct)
            crossProduct_cb.currentIndexChanged.connect(self.loadCrossSet)
            self.crossProduct_comboBoxes.append(crossProduct_cb)

            crossProduct_hb = QHBoxLayout()
            crossProduct_hb.addWidget(crossProduct_lbl)
            crossProduct_hb.addWidget(crossProduct_cb)
            self.crossProduct_boxes.append(crossProduct_hb)

        # self.crossProduct1_label = QLabel("Choose first set:")
        # self.crossProduct1_label.setMargin(4)
        # self.crossProduct2_label = QLabel("Choose second set:")
        # self.crossProduct2_label.setMargin(4)
        #
        # self.crossProduct1_comboBox = QComboBox()
        # self.crossProduct2_comboBox = QComboBox()
        # self.crossProduct1_comboBox.setFixedHeight(23)
        # self.crossProduct2_comboBox.setFixedHeight(23)
        #
        # self.crossProduct1_comboBox.addItems(filteredForCrossproduct)
        # self.crossProduct2_comboBox.addItems(filteredForCrossproduct)
        # self.crossProduct1_comboBox.currentIndexChanged.connect(self.loadCrossSet)
        # self.crossProduct2_comboBox.currentIndexChanged.connect(self.loadCrossSet)
        #
        # self.crossProduct1Box = QHBoxLayout()
        # self.crossProduct2Box = QHBoxLayout()
        #
        # self.crossProduct1Box.addWidget(self.crossProduct1_label)
        # self.crossProduct1Box.addWidget(self.crossProduct1_comboBox)
        # self.crossProduct2Box.addWidget(self.crossProduct2_label)
        # self.crossProduct2Box.addWidget(self.crossProduct2_comboBox)

        self.nElements_name_label = QLabel("Choose element name:")
        self.nElements_name_label.setMargin(4)
        self.nElements_n_label = QLabel("Choose n:")
        self.nElements_n_label.setMargin(4)

        sp = self.nElements_name_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.nElements_name_label.setSizePolicy(sp)

        sp = self.nElements_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.nElements_n_label.setSizePolicy(sp)

        self.nElements_name_lineEdit = QLineEdit()
        self.nElements_n_lineEdit = QLineEdit()
        onlyInt = QIntValidator(1, 99999)
        self.nElements_n_lineEdit.setValidator(onlyInt)

        self.nElements_name_lineEdit.textChanged.connect(self.loadNElements)
        self.nElements_n_lineEdit.textChanged.connect(self.loadNElements)

        self.nElements_name_box = QHBoxLayout()
        self.nElements_n_box = QHBoxLayout()

        self.nElements_name_box.addWidget(self.nElements_name_label)
        self.nElements_name_box.addWidget(self.nElements_name_lineEdit)
        self.nElements_n_box.addWidget(self.nElements_n_label)
        self.nElements_n_box.addWidget(self.nElements_n_lineEdit)

        self.add_button = QPushButton("+")
        self.add_button.setFixedHeight(23)
        self.add_button.setFixedWidth(23)
        self.add_button.setDefault(False)
        self.add_button.setAutoDefault(False)
        self.add_button.clicked.connect(self.addItem)

        self.delete_button = QPushButton("-")
        self.delete_button.setFixedHeight(23)
        self.delete_button.setFixedWidth(23)
        self.delete_button.setDefault(False)
        self.delete_button.setAutoDefault(False)
        self.delete_button.clicked.connect(self.deleteSelectedItems)

        self.newMappingName = QComboBox()
        self.newMappingName.setFixedHeight(23)

        sp = self.newMappingName.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.newMappingName.setSizePolicy(sp)

        if self.type_of_set == "mapping":
            self.loadMappings()

        self.addBox = QHBoxLayout()
        self.addBox.addWidget(self.newMappingName)
        self.addBox.addWidget(self.add_button)
        self.addBox.addWidget(self.delete_button)
        self.addBox.setAlignment(Qt.AlignRight)

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

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.name_label)
        self.vbox.addWidget(self.name_textEdit)
        self.vbox.addWidget(self.type_label)
        self.vbox.addWidget(self.type_comboBox)
        self.vbox.addLayout(self.setTypeBox)
        self.vbox.addLayout(self.inner_tuple_n_box)
        self.vbox.addLayout(self.inner_tupleTypeBox)
        self.vbox.addLayout(self.tuple_n_box)
        self.vbox.addLayout(self.tupleTypeBox)
        self.vbox.addLayout(self.union1Box)
        self.vbox.addLayout(self.union2Box)
        self.vbox.addLayout(self.intersection1Box)
        self.vbox.addLayout(self.intersection2Box)
        self.vbox.addLayout(self.complement1Box)
        self.vbox.addLayout(self.complement2Box)
        self.vbox.addLayout(self.powerSetBox)
        self.vbox.addLayout(self.crossProduct_n_box)
        for i in range(self.maxCrossProductSets):
            self.vbox.addLayout(self.crossProduct_boxes[i])
        self.vbox.addLayout(self.nElements_name_box)
        self.vbox.addLayout(self.nElements_n_box)
        self.vbox.addWidget(self.content_label)
        self.vbox.addWidget(self.subcontent_listWidget)
        self.vbox.addLayout(self.addBox)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.setType_label.setVisible(self.type_of_set == "set")
        self.setType_comboBox.setVisible(self.type_of_set == "set")
        self.inner_tuple_n_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tuple_n_lineEdit.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_button.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.tuple_n_label.setVisible(self.type_of_set == "n-tuple")
        self.tuple_n_lineEdit.setVisible(self.type_of_set == "n-tuple")
        self.tupleType_label.setVisible(self.type_of_set == "n-tuple")
        self.tupleType_button.setVisible(self.type_of_set == "n-tuple")
        if self.type_of_set == "set" or self.type_of_set == "n-tuple":
            self.subcontent_listWidget.itemDoubleClicked.connect(self.launchPopup)
        self.newMappingName.setVisible(self.type_of_set == "mapping")
        self.union1_label.setVisible(self.type_of_set == "union")
        self.union1_comboBox.setVisible(self.type_of_set == "union")
        self.union2_label.setVisible(self.type_of_set == "union")
        self.union2_comboBox.setVisible(self.type_of_set == "union")
        self.intersection1_label.setVisible(self.type_of_set == "intersection")
        self.intersection1_comboBox.setVisible(self.type_of_set == "intersection")
        self.intersection2_label.setVisible(self.type_of_set == "intersection")
        self.intersection2_comboBox.setVisible(self.type_of_set == "intersection")
        self.complement1_label.setVisible(self.type_of_set == "complement")
        self.complement1_comboBox.setVisible(self.type_of_set == "complement")
        self.complement2_label.setVisible(self.type_of_set == "complement")
        self.complement2_comboBox.setVisible(self.type_of_set == "complement")
        self.powerSet_label.setVisible(self.type_of_set == "power set")
        self.powerSet_comboBox.setVisible(self.type_of_set == "power set")
        self.crossProduct_n_label.setVisible(self.type_of_set == "cross product")
        self.crossProduct_n_lineEdit.setVisible(self.type_of_set == "cross product")
        for i in range(2):
            self.crossProduct_labels[i].setVisible(self.type_of_set == "cross product")
            self.crossProduct_comboBoxes[i].setVisible(self.type_of_set == "cross product")
        for i in range(2, self.maxCrossProductSets):
            self.crossProduct_labels[i].setVisible(False)
            self.crossProduct_comboBoxes[i].setVisible(False)
        self.nElements_name_label.setVisible(self.type_of_set == "n elements")
        self.nElements_name_lineEdit.setVisible(self.type_of_set == "n elements")
        self.nElements_n_label.setVisible(self.type_of_set == "n elements")
        self.nElements_n_lineEdit.setVisible(self.type_of_set == "n elements")

    def connectSetOfDictionary(self):
        self.subcontent_listWidget.clear()
        if self.type_of_set == "string" or self.type_of_set == "number":
            for elem in sorted(self.contentOfDict):
                item = QDMListWidgetItem(elem, self.type_of_set)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.subcontent_listWidget.addItem(item)
        elif self.type_of_set == "mapping" or self.type_of_set == "n-tuple":
            for elem in sorted(self.contentOfDict):
                item = QDMListWidgetItem(elem, self.type_of_set)
                self.subcontent_listWidget.addItem(item)
        # elif self.type_of_set == "2-tuple":
        #     if self.types_of_inner_tuple == "string" or self.types_of_inner_tuple == "number" or self.types_of_inner_tuple == "2-tuple":
        #         try:
        #             for elem in sorted(self.contentOfDict):
        #                 item = QDMListWidgetItem(elem, self.type_of_set)
        #                 self.subcontent_listWidget.addItem(item)
        #         except TypeError:
        #             for elem in self.contentOfDict:
        #                 item = QDMListWidgetItem(elem, self.type_of_set)
        #                 self.subcontent_listWidget.addItem(item)
        #             print("INFO: Could not sort various types")
        #     elif self.types_of_inner_tuple == "mapping":
        #         for elem in sorted(self.contentOfDict, key=lambda tup: tuple([tup[0].name, tup[1].name])):
        #             item = QDMListWidgetItem(elem, self.type_of_set)
        #             self.subcontent_listWidget.addItem(item)
        #     elif self.types_of_inner_tuple == "set":
        #         for elem in sorted(self.contentOfDict, key=lambda tup: tuple([sorted(tup[0]), sorted(tup[1])])):
        #             item = QDMListWidgetItem(elem, self.type_of_set)
        #             self.subcontent_listWidget.addItem(item)
        elif self.type_of_set == "set":
            for elem in sorted(self.contentOfDict, key=lambda fst: len(fst)):
                item = QDMListWidgetItem(elem, self.type_of_set)
                self.subcontent_listWidget.addItem(item)
        # elif self.type_of_set == "set":
        #     if self.type_of_inner_set == "string" or self.type_of_inner_set == "number" or self.type_of_inner_set == "2-tuple":
        #         sortedList = sorted(self.contentOfDict, key=lambda fst: sorted([str(elem) for elem in fst]))
        #         for elem in sorted(sortedList, key=lambda fst: sorted([str(elem) for elem in fst])):
        #             item = QDMListWidgetItem(elem, self.type_of_set)
        #             self.subcontent_listWidget.addItem(item)
        #     elif self.type_of_inner_set == "mapping":
        #         sortedList = sorted(self.contentOfDict, key=lambda fst: sorted([elem.name for elem in fst]))
        #         for elem in sorted(sortedList, key=lambda fst: len(fst)):
        #             item = QDMListWidgetItem(elem, self.type_of_set)
        #             self.subcontent_listWidget.addItem(item)

    def onInnerTypeChanged(self):
        if self.setType_comboBox.currentText() == "n-tuple":
            if self.type_of_inner_set[0] != "n-tuple":
                self.type_of_inner_set = tuple(["n-tuple", ["string"]*self.size_of_inner_set_tuple])
        else:
            self.type_of_inner_set = self.setType_comboBox.currentText()

        self.inner_tuple_n_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tuple_n_lineEdit.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_button.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.contentOfDict = set()
        self.connectSetOfDictionary()

    # def onInnerTupleTypeChanged(self):
    #     self.types_of_inner_tuple = self.tupleType_comboBox.currentText()
    #     self.contentOfDict = set()
    #     self.connectSetOfDictionary()

    def onNChanged(self):
        if self.tuple_n_lineEdit.text() == "0" or self.tuple_n_lineEdit.text() == "1":
            self.tuple_n_lineEdit.setText("2")
        try:
            self.size_of_inner_tuple = int(self.tuple_n_lineEdit.text())
        except Exception:
            self.size_of_inner_tuple = 2
            self.tuple_n_lineEdit.setText("2")
        self.types_of_inner_tuple = ["string"] * self.size_of_inner_tuple
        self.contentOfDict = frozenset()
        self.connectSetOfDictionary()

    def onCrossNChanged(self):
        self.contentOfDict = frozenset()
        self.connectSetOfDictionary()
        if self.crossProduct_n_lineEdit.text() == "0" or self.crossProduct_n_lineEdit.text() == "1":
            self.crossProduct_n_lineEdit.setText("2")
        try:
            new_size = int(self.crossProduct_n_lineEdit.text())
        except Exception:
            new_size = 2
            self.crossProduct_n_lineEdit.setText("2")
        for i in range(new_size):
            self.crossProduct_labels[i].setVisible(True)
            self.crossProduct_comboBoxes[i].setVisible(True)
        for i in range(new_size, self.maxCrossProductSets):
            self.crossProduct_labels[i].setVisible(False)
            self.crossProduct_comboBoxes[i].setVisible(False)

    def onInnerNChanged(self):
        if self.inner_tuple_n_lineEdit.text() == "0" or self.inner_tuple_n_lineEdit.text() == "1":
            self.inner_tuple_n_lineEdit.setText("2")
        try:
            self.size_of_inner_set_tuple = int(self.inner_tuple_n_lineEdit.text())
        except Exception:
            self.size_of_inner_set_tuple = 2
            self.inner_tuple_n_lineEdit.setText("2")
        self.type_of_inner_set = tuple(["n-tuple", ["string"]*self.size_of_inner_set_tuple])
        self.contentOfDict = frozenset()
        self.connectSetOfDictionary()

    def onTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.types_of_inner_tuple))
        if pop.exec():
            if self.types_of_inner_tuple != pop.types_of_tuple:
                self.types_of_inner_tuple = pop.types_of_tuple
                self.contentOfDict = frozenset()
                self.connectSetOfDictionary()

    def onInnerTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.type_of_inner_set[1]), inner=True)
        if pop.exec():
            if self.type_of_inner_set[1] != pop.types_of_tuple:
                self.type_of_inner_set = tuple(["n-tuple", pop.types_of_tuple])
                self.contentOfDict = frozenset()
                self.connectSetOfDictionary()

    def onTypeChanged(self):
        self.type_of_set = self.type_comboBox.currentText()
        self.contentOfDict = frozenset()
        self.connectSetOfDictionary()

        self.setType_label.setVisible(self.type_of_set == "set")
        self.setType_comboBox.setVisible(self.type_of_set == "set")
        self.inner_tuple_n_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tuple_n_lineEdit.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_label.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.inner_tupleType_button.setVisible(self.type_of_set == "set" and self.type_of_inner_set[0] == "n-tuple")
        self.tuple_n_label.setVisible(self.type_of_set == "n-tuple")
        self.tuple_n_lineEdit.setVisible(self.type_of_set == "n-tuple")
        self.tupleType_label.setVisible(self.type_of_set == "n-tuple")
        self.tupleType_button.setVisible(self.type_of_set == "n-tuple")
        try:
            self.subcontent_listWidget.itemDoubleClicked.disconnect(self.launchPopup)
        except:
            pass
        if self.type_of_set == "set" or self.type_of_set == "n-tuple":
            self.subcontent_listWidget.itemDoubleClicked.connect(self.launchPopup)

        self.newMappingName.setVisible(self.type_of_set == "mapping")
        if self.type_of_set == "mapping":
            self.loadMappings()

        self.union1_label.setVisible(self.type_of_set == "union")
        self.union1_comboBox.setVisible(self.type_of_set == "union")
        self.union2_label.setVisible(self.type_of_set == "union")
        self.union2_comboBox.setVisible(self.type_of_set == "union")
        if self.type_of_set == "union":
            self.loadUnion()

        self.intersection1_label.setVisible(self.type_of_set == "intersection")
        self.intersection1_comboBox.setVisible(self.type_of_set == "intersection")
        self.intersection2_label.setVisible(self.type_of_set == "intersection")
        self.intersection2_comboBox.setVisible(self.type_of_set == "intersection")
        if self.type_of_set == "intersection":
            self.loadIntersection()

        self.complement1_label.setVisible(self.type_of_set == "complement")
        self.complement1_comboBox.setVisible(self.type_of_set == "complement")
        self.complement2_label.setVisible(self.type_of_set == "complement")
        self.complement2_comboBox.setVisible(self.type_of_set == "complement")
        if self.type_of_set == "complement":
            self.loadComplement()

        self.powerSet_label.setVisible(self.type_of_set == "power set")
        self.powerSet_comboBox.setVisible(self.type_of_set == "power set")
        if self.type_of_set == "power set":
            self.loadPowerSet()

        self.crossProduct_n_label.setVisible(self.type_of_set == "cross product")
        self.crossProduct_n_lineEdit.setVisible(self.type_of_set == "cross product")
        for i in range(int(self.crossProduct_n_lineEdit.text())):
            self.crossProduct_labels[i].setVisible(self.type_of_set == "cross product")
            self.crossProduct_comboBoxes[i].setVisible(self.type_of_set == "cross product")
        for i in range(int(self.crossProduct_n_lineEdit.text()), self.maxCrossProductSets):
            self.crossProduct_labels[i].setVisible(False)
            self.crossProduct_comboBoxes[i].setVisible(False)
        if self.type_of_set == "cross product":
            self.loadCrossSet()

        self.nElements_name_label.setVisible(self.type_of_set == "n elements")
        self.nElements_name_lineEdit.setVisible(self.type_of_set == "n elements")
        self.nElements_n_label.setVisible(self.type_of_set == "n elements")
        self.nElements_n_lineEdit.setVisible(self.type_of_set == "n elements")
        if self.type_of_set == "n elements":
            self.loadNElements()

        self.add_button.setVisible(not (self.type_of_set == "union" or self.type_of_set == "intersection" or self.type_of_set == "complement" or self.type_of_set == "symmetric difference" or self.type_of_set == "power set" or self.type_of_set == "cross product" or self.type_of_set == "n elements"))
        self.delete_button.setVisible(not (self.type_of_set == "union" or self.type_of_set == "intersection" or self.type_of_set == "complement" or self.type_of_set == "symmetric difference" or self.type_of_set == "power set" or self.type_of_set == "cross product" or self.type_of_set == "n elements"))

    def launchPopup(self, item):
        if self.type_of_set == "set":
            pop = QDMContentListWidgetInnerSetPopup(item.item, self.type_of_inner_set)
            if pop.exec():
                item.item = pop.set
                item.overwriteText()
        elif self.type_of_set == "n-tuple":
            pop = QDMContentListWidgetNTuplePopup(item.item, self.types_of_inner_tuple)
            if pop.exec():
                item.item = pop.tup
                item.overwriteText()
        # elif self.type_of_set == "2-tuple":
        #     pop = QDMContentListWidgetTuplePopup(item.item, self.types_of_inner_tuple, editing=True)
        #     if pop.exec():
        #         item.item = pop.tuple
        #         item.overwriteText()

    def addItem(self):
        if self.type_of_set == "string":
            newItem = QDMListWidgetItem("enter name", self.type_of_set)
            newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
            self.subcontent_listWidget.addItem(newItem)
            self.subcontent_listWidget.editItem(newItem)
            self.subcontent_listWidget.scrollToBottom()
        elif self.type_of_set == "number":
            newItem = QDMListWidgetItem("enter number", self.type_of_set)
            newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
            self.subcontent_listWidget.addItem(newItem)
            self.subcontent_listWidget.editItem(newItem)
            self.subcontent_listWidget.scrollToBottom()
        elif self.type_of_set == "n-tuple":
            default_tuple = []
            for i in range(len(self.types_of_inner_tuple)):
                if type(self.types_of_inner_tuple[i]) == tuple:
                    if self.types_of_inner_tuple[i][0] == "n-tuple":
                        default_tuple.append(["" if elem == "string" else 0 for elem in self.types_of_inner_tuple[i][1]])
                    elif self.types_of_inner_tuple[i][0] == "set":
                        default_tuple.append(frozenset())
                else:
                    if self.types_of_inner_tuple[i] == "string":
                        default_tuple.append("")
                    elif self.types_of_inner_tuple[i] == "number":
                        default_tuple.append(0)
                    elif self.types_of_inner_tuple[i] == "mapping":
                        default_tuple.append(None)
            pop = QDMContentListWidgetNTuplePopup(tuple(default_tuple), self.types_of_inner_tuple)
            if pop.exec():
                newItem = QDMListWidgetItem(pop.tup, self.type_of_set)
                self.subcontent_listWidget.addItem(newItem)
                self.subcontent_listWidget.scrollToBottom()
        elif self.type_of_set == "set":
            pop = QDMContentListWidgetInnerSetPopup(frozenset(), self.type_of_inner_set)
            if pop.exec():
                newItem = QDMListWidgetItem(pop.set, self.type_of_set)
                self.subcontent_listWidget.addItem(newItem)
                self.subcontent_listWidget.scrollToBottom()
        elif self.type_of_set == "mapping":
            if self.newMappingName.count() > 0:
                newItem = QDMListWidgetItem(FPTMapping(self.newMappingName.currentText()), self.type_of_set)
                self.subcontent_listWidget.addItem(newItem)
                self.loadMappings()
            self.subcontent_listWidget.scrollToBottom()

    def deleteSelectedItems(self):
        for item in self.subcontent_listWidget.selectedItems():
            self.subcontent_listWidget.takeItem(self.subcontent_listWidget.row(item))
        if self.type_of_set == "mapping":
            self.loadMappings()

    def loadMappings(self):
        allMappings = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        for i in range(0, self.subcontent_listWidget.count()):
            allMappings.pop(self.subcontent_listWidget.item(i).item.name)
        self.newMappingName.clear()
        self.newMappingName.addItems(allMappings)

    def loadUnion(self):
        try:
            self.subcontent_listWidget.clear()
            listOfFirstSet = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.union1_comboBox.currentText()])
            listOfSecondSet = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.union2_comboBox.currentText()])

            firstSetType = "string"
            firstInnerTupleType = ["string", "string"]
            firstInnerSetType = "string"
            if len(listOfFirstSet) > 0:
                if type(listOfFirstSet[0]) == str:
                    firstSetType = "string"
                elif type(listOfFirstSet[0]) == int or type(listOfFirstSet[0]) == float:
                    firstSetType = "number"
                elif type(listOfFirstSet[0]) == tuple:
                    firstSetType = "n-tuple"
                    firstInnerTupleType = []
                    for i in range(len(listOfFirstSet[0])):
                        if type(listOfFirstSet[0][i]) == str:
                            firstInnerTupleType.append("string")
                        elif type(listOfFirstSet[0][i]) == int or type(listOfFirstSet[0][i]) == float:
                            firstInnerTupleType.append("number")
                        elif type(listOfFirstSet[0][i]) == frozenset or type(listOfFirstSet[0][i]) == set:
                            innerType = str
                            if len(listOfFirstSet[0][i]) > 0:
                                innerType = type(list(listOfFirstSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            firstInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            firstInnerTupleType.append([tuple(["n-tuple", ["string" if type(innerTupleElem) == str else "number" for innerTupleElem in listOfFirstSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            firstInnerTupleType.append("mapping")
                elif type(listOfFirstSet[0]) == frozenset or type(listOfFirstSet[0]) == set:
                    firstSetType = "set"
                    for elem in listOfFirstSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    firstInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    firstInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    firstInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    firstInnerSetType = tuple(["n-tuple", ["string" if type(innerTupleElem) == str else "number" for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    firstInnerSetType = "mapping"
                                break
                            break
                elif type(listOfFirstSet[0]) == FPTMapping:
                    firstSetType = "mapping"

            secondSetType = "string"
            secondInnerTupleType = ["string", "string"]
            secondInnerSetType = "string"
            if len(listOfSecondSet) > 0:
                if type(listOfSecondSet[0]) == str:
                    secondSetType = "string"
                elif type(listOfSecondSet[0]) == int or type(listOfSecondSet[0]) == float:
                    secondSetType = "number"
                elif type(listOfSecondSet[0]) == tuple:
                    secondSetType = "n-tuple"
                    secondInnerTupleType = []
                    for i in range(len(listOfSecondSet[0])):
                        if type(listOfSecondSet[0][i]) == str:
                            secondInnerTupleType.append("string")
                        elif type(listOfSecondSet[0][i]) == int or type(listOfSecondSet[0][i]) == float:
                            secondInnerTupleType.append("number")
                        elif type(listOfSecondSet[0][i]) == frozenset or type(listOfSecondSet[0][i]) == set:
                            innerType = str
                            if len(listOfSecondSet[0][i]) > 0:
                                innerType = type(list(listOfSecondSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            secondInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            secondInnerTupleType.append([tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in listOfSecondSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            secondInnerTupleType.append("mapping")
                elif type(listOfSecondSet[0]) == frozenset or type(listOfSecondSet[0]) == set:
                    secondSetType = "set"
                    for elem in listOfSecondSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    secondInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    secondInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    secondInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    secondInnerSetType = tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    secondInnerSetType = "mapping"
                                break
                            break
                elif type(listOfSecondSet[0]) == FPTMapping:
                    secondSetType = "mapping"

            if firstSetType == secondSetType and firstInnerTupleType == secondInnerTupleType and firstInnerSetType == secondInnerSetType:
                # if firstSetType == "mapping":
                #     union = listOfFirstSet
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [elem.name]
                #     for elem in listOfSecondSet:
                #         if elem.name not in firstSetNames:
                #             union.append(elem)
                #     union = frozenset(union)
                # elif firstInnerTupleType == "mapping":
                #     union = listOfFirstSet
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [(elem[0].name, elem[1].name)]
                #     for elem in listOfSecondSet:
                #         if (elem[0].name, elem[1].name) not in firstSetNames:
                #             union.append(elem)
                #     union = frozenset(union)
                # elif firstInnerSetType == "mapping":
                #     union = listOfFirstSet
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [set([innerElem.name for innerElem in elem])]
                #     for elem in listOfSecondSet:
                #         if set([innerElem.name for innerElem in elem]) not in firstSetNames:
                #             union.append(elem)
                #     union = frozenset(union)
                # else:
                #     listOfFirstSet = frozenset(listOfFirstSet)
                #     listOfSecondSet = frozenset(listOfSecondSet)
                #     union = listOfFirstSet.union(listOfSecondSet)
                listOfFirstSet = frozenset(listOfFirstSet)
                listOfSecondSet = frozenset(listOfSecondSet)
                union = listOfFirstSet.union(listOfSecondSet)

                # if firstSetType == "2-tuple":
                #     for elem in union:
                #         item = QDMListWidgetItem(elem, firstSetType, tupleType=firstInnerTupleType)
                #         self.subcontent_listWidget.addItem(item)
                # elif firstSetType == "set":
                #     for elem in union:
                #         item = QDMListWidgetItem(elem, firstSetType, setType=firstInnerSetType)
                #         self.subcontent_listWidget.addItem(item)
                # else:
                #     for elem in union:
                #         item = QDMListWidgetItem(elem, firstSetType)
                #         self.subcontent_listWidget.addItem(item)
                for elem in union:
                    item = QDMListWidgetItem(elem, firstSetType)
                    self.subcontent_listWidget.addItem(item)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nChosen sets do not have the same type")
                msg.exec()

        except Exception as e:
            dumpException(e)

    def loadIntersection(self):
        try:
            self.subcontent_listWidget.clear()
            listOfFirstSet = list(
                self.accessDicts.getDictionaryWithoutTransformation("sets")[self.intersection1_comboBox.currentText()])
            listOfSecondSet = list(
                self.accessDicts.getDictionaryWithoutTransformation("sets")[self.intersection2_comboBox.currentText()])

            firstSetType = "string"
            firstInnerTupleType = ["string", "string"]
            firstInnerSetType = "string"
            if len(listOfFirstSet) > 0:
                if type(listOfFirstSet[0]) == str:
                    firstSetType = "string"
                elif type(listOfFirstSet[0]) == int or type(listOfFirstSet[0]) == float:
                    firstSetType = "number"
                elif type(listOfFirstSet[0]) == tuple:
                    firstSetType = "n-tuple"
                    firstInnerTupleType = []
                    for i in range(len(listOfFirstSet[0])):
                        if type(listOfFirstSet[0][i]) == str:
                            firstInnerTupleType.append("string")
                        elif type(listOfFirstSet[0][i]) == int or type(listOfFirstSet[0][i]) == float:
                            firstInnerTupleType.append("number")
                        elif type(listOfFirstSet[0][i]) == frozenset or type(listOfFirstSet[0][i]) == set:
                            innerType = str
                            if len(listOfFirstSet[0][i]) > 0:
                                innerType = type(list(listOfFirstSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            firstInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            firstInnerTupleType.append([tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in listOfFirstSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            firstInnerTupleType.append("mapping")
                elif type(listOfFirstSet[0]) == frozenset or type(listOfFirstSet[0]) == set:
                    firstSetType = "set"
                    for elem in listOfFirstSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    firstInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    firstInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    firstInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    firstInnerSetType = tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    firstInnerSetType = "mapping"
                                break
                            break
                elif type(listOfFirstSet[0]) == FPTMapping:
                    firstSetType = "mapping"

            secondSetType = "string"
            secondInnerTupleType = ["string", "string"]
            secondInnerSetType = "string"
            if len(listOfSecondSet) > 0:
                if type(listOfSecondSet[0]) == str:
                    secondSetType = "string"
                elif type(listOfSecondSet[0]) == int or type(listOfSecondSet[0]) == float:
                    secondSetType = "number"
                elif type(listOfSecondSet[0]) == tuple:
                    secondSetType = "n-tuple"
                    secondInnerTupleType = []
                    for i in range(len(listOfSecondSet[0])):
                        if type(listOfSecondSet[0][i]) == str:
                            secondInnerTupleType.append("string")
                        elif type(listOfSecondSet[0][i]) == int or type(listOfSecondSet[0][i]) == float:
                            secondInnerTupleType.append("number")
                        elif type(listOfSecondSet[0][i]) == frozenset or type(listOfSecondSet[0][i]) == set:
                            innerType = str
                            if len(listOfSecondSet[0][i]) > 0:
                                innerType = type(list(listOfSecondSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            secondInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            secondInnerTupleType.append([tuple(["n-tuple",
                                                                ["string" if type(innerTupleElem) == str else "number"
                                                                 for innerTupleElem in listOfSecondSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            secondInnerTupleType.append("mapping")
                elif type(listOfSecondSet[0]) == frozenset or type(listOfSecondSet[0]) == set:
                    secondSetType = "set"
                    for elem in listOfSecondSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    secondInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    secondInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    secondInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    secondInnerSetType = tuple(["n-tuple",
                                                                ["string" if type(innerTupleElem) == str else "number"
                                                                 for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    secondInnerSetType = "mapping"
                                break
                            break
                elif type(listOfSecondSet[0]) == FPTMapping:
                    secondSetType = "mapping"

            if firstSetType == secondSetType and firstInnerTupleType == secondInnerTupleType and firstInnerSetType == secondInnerSetType:
                # if firstSetType == "mapping":
                #     intersection = []
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [elem.name]
                #     for elem in listOfSecondSet:
                #         if elem.name in firstSetNames:
                #             intersection.append(elem)
                #     intersection = frozenset(intersection)
                # elif firstInnerTupleType == "mapping":
                #     intersection = []
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [(elem[0].name, elem[1].name)]
                #     for elem in listOfSecondSet:
                #         if (elem[0].name, elem[1].name) in firstSetNames:
                #             intersection.append(elem)
                #     intersection = frozenset(intersection)
                # elif firstInnerSetType == "mapping":
                #     intersection = []
                #     firstSetNames = []
                #     for elem in listOfFirstSet:
                #         firstSetNames += [set([innerElem.name for innerElem in elem])]
                #     for elem in listOfSecondSet:
                #         if set([innerElem.name for innerElem in elem]) in firstSetNames:
                #             intersection.append(elem)
                #     intersection = frozenset(intersection)
                # else:
                #     listOfFirstSet = frozenset(listOfFirstSet)
                #     listOfSecondSet = frozenset(listOfSecondSet)
                #     intersection = listOfFirstSet.intersection(listOfSecondSet)
                listOfFirstSet = frozenset(listOfFirstSet)
                listOfSecondSet = frozenset(listOfSecondSet)
                intersection = listOfFirstSet.intersection(listOfSecondSet)

                # if firstSetType == "2-tuple":
                #     for elem in intersection:
                #         item = QDMListWidgetItem(elem, firstSetType, tupleType=firstInnerTupleType)
                #         self.subcontent_listWidget.addItem(item)
                # elif firstSetType == "set":
                #     for elem in intersection:
                #         item = QDMListWidgetItem(elem, firstSetType, setType=firstInnerSetType)
                #         self.subcontent_listWidget.addItem(item)
                # else:
                #     for elem in intersection:
                #         item = QDMListWidgetItem(elem, firstSetType)
                #         self.subcontent_listWidget.addItem(item)
                for elem in intersection:
                    item = QDMListWidgetItem(elem, firstSetType)
                    self.subcontent_listWidget.addItem(item)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nChosen sets do not have the same type")
                msg.exec()

        except Exception as e:
            dumpException(e)

    def loadComplement(self):
        try:
            self.subcontent_listWidget.clear()
            listOfFirstSet = list(
                self.accessDicts.getDictionaryWithoutTransformation("sets")[self.complement1_comboBox.currentText()])
            listOfSecondSet = list(
                self.accessDicts.getDictionaryWithoutTransformation("sets")[self.complement2_comboBox.currentText()])

            firstSetType = "string"
            firstInnerTupleType = ["string", "string"]
            firstInnerSetType = "string"
            if len(listOfFirstSet) > 0:
                if type(listOfFirstSet[0]) == str:
                    firstSetType = "string"
                elif type(listOfFirstSet[0]) == int or type(listOfFirstSet[0]) == float:
                    firstSetType = "number"
                elif type(listOfFirstSet[0]) == tuple:
                    firstSetType = "n-tuple"
                    firstInnerTupleType = []
                    for i in range(len(listOfFirstSet[0])):
                        if type(listOfFirstSet[0][i]) == str:
                            firstInnerTupleType.append("string")
                        elif type(listOfFirstSet[0][i]) == int or type(listOfFirstSet[0][i]) == float:
                            firstInnerTupleType.append("number")
                        elif type(listOfFirstSet[0][i]) == frozenset or type(listOfFirstSet[0][i]) == set:
                            innerType = str
                            if len(listOfFirstSet[0][i]) > 0:
                                innerType = type(list(listOfFirstSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            firstInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            firstInnerTupleType.append([tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in listOfFirstSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            firstInnerTupleType.append("mapping")
                elif type(listOfFirstSet[0]) == frozenset or type(listOfFirstSet[0]) == set:
                    firstSetType = "set"
                    for elem in listOfFirstSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    firstInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    firstInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    firstInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    firstInnerSetType = tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    firstInnerSetType = "mapping"
                                break
                            break
                elif type(listOfFirstSet[0]) == FPTMapping:
                    firstSetType = "mapping"

            secondSetType = "string"
            secondInnerTupleType = ["string", "string"]
            secondInnerSetType = "string"
            if len(listOfSecondSet) > 0:
                if type(listOfSecondSet[0]) == str:
                    secondSetType = "string"
                elif type(listOfSecondSet[0]) == int or type(listOfSecondSet[0]) == float:
                    secondSetType = "number"
                elif type(listOfSecondSet[0]) == tuple:
                    secondSetType = "n-tuple"
                    secondInnerTupleType = []
                    for i in range(len(listOfSecondSet[0])):
                        if type(listOfSecondSet[0][i]) == str:
                            secondInnerTupleType.append("string")
                        elif type(listOfSecondSet[0][i]) == int or type(listOfSecondSet[0][i]) == float:
                            secondInnerTupleType.append("number")
                        elif type(listOfSecondSet[0][i]) == frozenset or type(listOfSecondSet[0][i]) == set:
                            innerType = str
                            if len(listOfSecondSet[0][i]) > 0:
                                innerType = type(list(listOfSecondSet[0][i])[0])
                            innerType = "string" if innerType == str else "number"
                            secondInnerTupleType.append(tuple(["set", innerType]))
                        elif type(listOfFirstSet[0][i]) == tuple:
                            secondInnerTupleType.append([tuple(["n-tuple",
                                                                ["string" if type(innerTupleElem) == str else "number"
                                                                 for innerTupleElem in listOfSecondSet[0][i]]])])
                        elif type(listOfFirstSet[0][i]) == FPTMapping:
                            secondInnerTupleType.append("mapping")
                elif type(listOfSecondSet[0]) == frozenset or type(listOfSecondSet[0]) == set:
                    secondSetType = "set"
                    for elem in listOfSecondSet:
                        if len(elem) > 0:
                            for innerElem in elem:
                                if type(innerElem) == str:
                                    secondInnerSetType = "string"
                                elif type(innerElem) == int or type(innerElem) == float:
                                    secondInnerSetType = "number"
                                elif type(innerElem) == frozenset or type(innerElem) == set:
                                    secondInnerSetType = "set"
                                elif type(innerElem) == tuple:
                                    secondInnerSetType = tuple(["n-tuple",
                                                                ["string" if type(innerTupleElem) == str else "number"
                                                                 for innerTupleElem in innerElem]])
                                elif type(innerElem) == FPTMapping:
                                    secondInnerSetType = "mapping"
                                break
                            break
                elif type(listOfSecondSet[0]) == FPTMapping:
                    secondSetType = "mapping"

            if firstSetType == secondSetType and firstInnerTupleType == secondInnerTupleType and firstInnerSetType == secondInnerSetType:
                listOfFirstSet = frozenset(listOfFirstSet)
                listOfSecondSet = frozenset(listOfSecondSet)
                complement = listOfFirstSet.difference(listOfSecondSet)

                for elem in complement:
                    item = QDMListWidgetItem(elem, firstSetType)
                    self.subcontent_listWidget.addItem(item)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nChosen sets do not have the same type")
                msg.exec()

        except Exception as e:
            dumpException(e)

    def loadPowerSet(self):
        try:
            self.subcontent_listWidget.clear()
            listOfSet = list(
                self.accessDicts.getDictionaryWithoutTransformation("sets")[self.powerSet_comboBox.currentText()])
            temp = chain.from_iterable(combinations(listOfSet, r) for r in range(len(listOfSet) + 1))
            powSet = frozenset(frozenset(i) for i in temp)
            for elem in powSet:
                item = QDMListWidgetItem(elem, self.type_of_set)
                self.subcontent_listWidget.addItem(item)
        except Exception as e:
            print(e)

    def loadCrossSet(self):
        try:
            self.subcontent_listWidget.clear()
            crossProduct_size = int(self.crossProduct_n_lineEdit.text())
            listOfSets = []
            for i in range(crossProduct_size):
                listOfSets.append(list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.crossProduct_comboBoxes[i].currentText()]))

            # setTypes = []
            # innerTupleTypes = []
            # innerSetTypes = []
            # for s in listOfSets:
            #     setType = "string"
            #     innerTupleType = ["string", "string"]
            #     innerSetType = "string"
            #     if len(s) > 0:
            #         if type(s[0]) == str:
            #             setType = "string"
            #         elif type(s[0]) == int or type(s[0]) == float:
            #             setType = "number"
            #         elif type(s[0]) == tuple:
            #             setType = "n-tuple"
            #             innerTupleType = []
            #             for i in range(len(s[0])):
            #                 if type(s[0][i]) == str:
            #                     innerTupleType.append("string")
            #                 elif type(s[0][i]) == int or type(s[0][i]) == float:
            #                     innerTupleType.append("number")
            #                 elif type(s[0][i]) == frozenset or type(s[0][i]) == set:
            #                     innerType = str
            #                     if len(s[0][i]) > 0:
            #                         innerType = type(list(s[0][i])[0])
            #                     innerType = "string" if innerType == str else "number"
            #                     innerTupleType.append(tuple(["set", innerType]))
            #                 elif type(s[0][i]) == tuple:
            #                     innerTupleType.append([tuple(["n-tuple",
            #                                                        ["string" if type(
            #                                                            innerTupleElem) == str else "number"
            #                                                         for innerTupleElem in s[0][i]]])])
            #                 elif type(s[0][i]) == FPTMapping:
            #                     innerTupleType.append("mapping")
            #         elif type(s[0]) == frozenset or type(s[0]) == set:
            #             setType = "set"
            #             for elem in s:
            #                 if len(elem) > 0:
            #                     for innerElem in elem:
            #                         if type(innerElem) == str:
            #                             innerSetType = "string"
            #                         elif type(innerElem) == int or type(innerElem) == float:
            #                             innerSetType = "number"
            #                         elif type(innerElem) == frozenset or type(innerElem) == set:
            #                             innerSetType = "set"
            #                         elif type(innerElem) == tuple:
            #                             innerSetType = tuple(["n-tuple",
            #                                                        ["string" if type(
            #                                                            innerTupleElem) == str else "number"
            #                                                         for innerTupleElem in innerElem]])
            #                         elif type(innerElem) == FPTMapping:
            #                             innerSetType = "mapping"
            #                         break
            #                     break
            #         elif type(s[0]) == FPTMapping:
            #             setType = "mapping"
            #
            #     setTypes.append(setType)
            #     innerTupleTypes.append(innerTupleType)
            #     innerSetTypes.append(innerSetType)

            if crossProduct_size == 3:
                crossProduct = frozenset((a, b, c) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2])
            elif crossProduct_size == 4:
                crossProduct = frozenset((a, b, c, d) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3])
            elif crossProduct_size == 5:
                crossProduct = frozenset((a, b, c, d, e) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3] for e in listOfSets[4])
            elif crossProduct_size == 6:
                crossProduct = frozenset((a, b, c, d, e, f) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3] for e in listOfSets[4] for f in listOfSets[5])
            elif crossProduct_size == 7:
                crossProduct = frozenset((a, b, c, d, e, f, g) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3] for e in listOfSets[4] for f in listOfSets[5] for g in listOfSets[6])
            elif crossProduct_size == 8:
                crossProduct = frozenset((a, b, c, d, e, f, g, h) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3] for e in listOfSets[4] for f in listOfSets[5] for g in listOfSets[6] for h in listOfSets[7])
            elif crossProduct_size == 9:
                crossProduct = frozenset((a, b, c, d, e, f, g, h, i) for a in listOfSets[0] for b in listOfSets[1] for c in listOfSets[2] for d in listOfSets[3] for e in listOfSets[4] for f in listOfSets[5] for g in listOfSets[6] for h in listOfSets[7] for i in listOfSets[8])
            else:
                crossProduct = frozenset((a, b) for a in listOfSets[0] for b in listOfSets[1])

            for elem in crossProduct:
                item = QDMListWidgetItem(elem, "n-tuple")
                self.subcontent_listWidget.addItem(item)

            # if firstSetType == secondSetType:
            #     if firstInnerTupleType == secondInnerTupleType and firstInnerSetType == secondInnerSetType:
            #         crossProduct = frozenset((x, y) for x in listOfFirstSet for y in listOfSecondSet)
            #         for elem in crossProduct:
            #             item = QDMListWidgetItem(elem, "2-tuple")
            #             self.subcontent_listWidget.addItem(item)
            #     elif firstInnerTupleType == "string" and secondInnerTupleType == "number" and firstInnerSetType == secondInnerSetType:
            #         crossProduct = frozenset((x, y) for x in listOfFirstSet for y in listOfSecondSet)
            #         for elem in crossProduct:
            #             item = QDMListWidgetItem(elem, "2-tuple")
            #             self.subcontent_listWidget.addItem(item)
            #     elif firstInnerTupleType == "number" and secondInnerTupleType == "string" and firstInnerSetType == secondInnerSetType:
            #         crossProduct = frozenset((x, y) for x in listOfFirstSet for y in listOfSecondSet)
            #         for elem in crossProduct:
            #             item = QDMListWidgetItem(elem, "2-tuple")
            #             self.subcontent_listWidget.addItem(item)
            #     elif firstInnerTupleType == secondInnerTupleType and firstInnerSetType == "string" and secondInnerSetType == "number":
            #         crossProduct = frozenset((x, y) for x in listOfFirstSet for y in listOfSecondSet)
            #         for elem in crossProduct:
            #             item = QDMListWidgetItem(elem, "2-tuple")
            #             self.subcontent_listWidget.addItem(item)
            #     elif firstInnerTupleType == secondInnerTupleType and firstInnerSetType == "number" and secondInnerSetType == "string":
            #         crossProduct = frozenset((x, y) for x in listOfFirstSet for y in listOfSecondSet)
            #         for elem in crossProduct:
            #             item = QDMListWidgetItem(elem, "2-tuple")
            #             self.subcontent_listWidget.addItem(item)
            #     else:
            #         msg = QMessageBox()
            #         msg.setWindowTitle("Information")
            #         msg.setIcon(QMessageBox.Information)
            #         msg.setText("Information:\nChosen sets do not have the same type")
            #         msg.exec()
            # else:
            #     msg = QMessageBox()
            #     msg.setWindowTitle("Information")
            #     msg.setIcon(QMessageBox.Information)
            #     msg.setText("Information:\nChosen sets do not have the same type")
            #     msg.exec()

        except Exception as e:
            print(e)

    def loadNElements(self):
        try:
            self.subcontent_listWidget.clear()

            name = self.nElements_name_lineEdit.text()
            n = self.nElements_n_lineEdit.text()

            if n == "" or name == "":
                return
            else:
                newList = []
                for i in range(int(n)):
                    newList += [name + str(i)]

                for elem in newList:
                    item = QDMListWidgetItem(elem, "string")
                    self.subcontent_listWidget.addItem(item)
        except Exception as e:
            print(e)

    def onNameChanged(self):
        self.keyName = self.name_textEdit.text()

    def getMappingNameTuples(self):
        res = []
        for elem in self.contentOfDict:
            res.append((elem[0].name, elem[1].name))
        return res

    def onSave(self):
        if self.type_of_set == "string" or self.type_of_set == "n elements":
            self.contentOfDict = set()
            doubleValues = False
            for i in range(0, self.subcontent_listWidget.count()):
                if self.subcontent_listWidget.item(i).text() in self.contentOfDict:
                    doubleValues = True
                self.contentOfDict.add(self.subcontent_listWidget.item(i).text())
            if doubleValues:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nDuplicates have been removed from the list")
                msg.exec()
            self.accept()

        elif self.type_of_set == "number":
            self.contentOfDict = set()
            doubleValues = False
            try:
                for i in range(0, self.subcontent_listWidget.count()):
                    if float(self.subcontent_listWidget.item(i).text()) in self.contentOfDict:
                        doubleValues = True
                    self.contentOfDict.add(float(self.subcontent_listWidget.item(i).text()))
                if doubleValues:
                    msg = QMessageBox()
                    msg.setWindowTitle("Information")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information:\nDuplicates have been removed from the list")
                    msg.exec()
                self.accept()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThere are inputs of a wrong type")
                msg.exec()

        elif self.type_of_set == "set" or self.type_of_set == "power set":
            try:
                self.contentOfDict = set()
                doubleValues = False
                try:
                    for i in range(0, self.subcontent_listWidget.count()):
                        if self.subcontent_listWidget.item(i).item in self.contentOfDict:
                            doubleValues = True
                        self.contentOfDict.add(self.subcontent_listWidget.item(i).item)
                    if doubleValues:
                        msg = QMessageBox()
                        msg.setWindowTitle("Information")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Information:\nDuplicates have been removed from the list")
                        msg.exec()
                    self.accept()
                except ValueError:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Warning:\nThere are inputs of a wrong type")
                    msg.exec()
            except Exception as e:
                print(e)

        elif self.type_of_set == "n-tuple" or self.type_of_set == "cross product":
            self.contentOfDict = set()
            doubleValues = False
            try:
                for i in range(0, self.subcontent_listWidget.count()):
                    if self.subcontent_listWidget.item(i).item in self.contentOfDict:
                        doubleValues = True
                    self.contentOfDict.add(self.subcontent_listWidget.item(i).item)
                if doubleValues:
                    msg = QMessageBox()
                    msg.setWindowTitle("Information")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information:\nDuplicates have been removed from the list")
                    msg.exec()
                self.accept()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThere are inputs of a wrong type")
                msg.exec()

        elif self.type_of_set == "union" or self.type_of_set == "intersection" or self.type_of_set == "complement":
            self.contentOfDict = set()
            doubleValues = False
            try:
                for i in range(0, self.subcontent_listWidget.count()):
                    if self.subcontent_listWidget.item(i).item in self.contentOfDict:
                        doubleValues = True
                    self.contentOfDict.add(self.subcontent_listWidget.item(i).item)
                if doubleValues:
                    msg = QMessageBox()
                    msg.setWindowTitle("Information")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information:\nDuplicates have been removed from the list")
                    msg.exec()

                self.accept()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThere are inputs of a wrong type")
                msg.exec()

        # elif self.type_of_set == "cross product":
        #     self.contentOfDict = set()
        #     doubleValues = False
        #     try:
        #         for i in range(0, self.subcontent_listWidget.count()):
        #             if self.subcontent_listWidget.item(i).item in self.contentOfDict:
        #                 doubleValues = True
        #             self.contentOfDict.add(self.subcontent_listWidget.item(i).item)
        #         if doubleValues:
        #             msg = QMessageBox()
        #             msg.setWindowTitle("Information")
        #             msg.setIcon(QMessageBox.Information)
        #             msg.setText("Information:\nDuplicates have been removed from the list")
        #             msg.exec()
        #
        #         for elem in self.contentOfDict:
        #             if type(elem[0]) != type(elem[1]):
        #                 msg = QMessageBox()
        #                 msg.setWindowTitle("Warning")
        #                 msg.setIcon(QMessageBox.Warning)
        #                 msg.setText("Warning:\nThe two sets must be of the same type")
        #                 msg.exec()
        #                 return
        #
        #         self.accept()
        #     except ValueError:
        #         msg = QMessageBox()
        #         msg.setWindowTitle("Warning")
        #         msg.setIcon(QMessageBox.Warning)
        #         msg.setText("Warning:\nThere are inputs of a wrong type")
        #         msg.exec()

        elif self.type_of_set == "mapping":
            self.contentOfDict = set()
            for i in range(0, self.subcontent_listWidget.count()):
                self.contentOfDict.add(FPTMapping(self.subcontent_listWidget.item(i).text()))
            self.accept()

        self.contentOfDict = frozenset(self.contentOfDict)

    def onCancel(self):
        self.reject()
