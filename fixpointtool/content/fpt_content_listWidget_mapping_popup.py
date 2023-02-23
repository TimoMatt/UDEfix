import copy
import os
from configparser import ConfigParser

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidget_inner_tuple_type_popup import QDMContentListWidgetTupleTypePopup
from fixpointtool.content.fpt_mapping import FPTMapping
from fixpointtool.content.fpt_content_mappingEdit import QDMMappingEdit
from nodeeditor.utils import dumpException

DEBUG = False


class QDMContentListWidgetMappingPopup(QDialog):
    LIST_OF_TYPES = ["string", "number", "mapping", "n-tuple", "set"]
    LIST_OF_SET_TYPES = ["string", "number", "mapping", "n-tuple"]
    # LIST_OF_TYPES = ["string", "number", "mapping", "2-tuple", "set"]
    # LIST_OF_SET_TYPES = ["string", "number", "mapping", "2-tuple"]
    # LIST_OF_TUPLE_TYPES = ["string", "number", "mapping", "2-tuple", "set"]
    LIST_OF_MV_AlGEBRAS = ["algebra 1", "algebra 2"]

    def __init__(self, mapping, parent=None):
        super().__init__(parent)

        self.accessDicts = AccessDictionaries()

        self.func = mapping
        self.func_name = self.func.name
        self.list_of_tuples = self.func.listOfTuples
        self.list_of_elements = self.func.listOfElements
        self.list_of_values = self.func.listOfValues

        self.mapping_type = self.func.mappingType

        self.input_set_type = "string"
        self.input_tuple_types = ["string", "string"]
        self.input_tuple_size = 2
        self.input_set_tuple_size = 2
        if self.func.inputSetName is None and self.func.inputMV is None:
            self.input_set_name = "custom set"

            if self.func.inputType == str:
                self.input_type = "string"
            elif self.func.inputType == float or self.func.inputType == int:
                self.input_type = "number"
            elif self.func.inputType == FPTMapping:
                self.input_type = "mapping"
            elif self.func.inputType == tuple:
                self.input_type = "n-tuple"
                for elem in self.func.listOfElements:
                    self.input_tuple_types = []
                    self.input_tuple_size = len(elem)
                    for tupleElem in elem:
                        if type(tupleElem) == str:
                            self.input_tuple_types += ["string"]
                        elif type(tupleElem) == int or type(tupleElem) == float:
                            self.input_tuple_types += ["number"]
                        elif type(tupleElem) == frozenset or type(tupleElem) == set:
                            innerType = str
                            if len(tupleElem) > 0:
                                innerType = type(list(tupleElem)[0])
                            innerType = "string" if innerType == str else "number"
                            self.input_tuple_types += [tuple(["set", innerType])]
                        elif type(tupleElem) == tuple:
                            self.input_tuple_types += [tuple(["n-tuple",
                                                                 ["string" if type(innerTupleElem) == str else "number"
                                                                  for innerTupleElem in tupleElem]])]
                        elif type(tupleElem) == FPTMapping:
                            self.input_tuple_types += ["mapping"]
                    break
            elif self.func.inputType == set or self.func.inputType == frozenset:
                self.input_type = "set"
                for elem in self.func.listOfElements:
                    isOkay = False
                    for innerElem in elem:
                        if type(innerElem) == str:
                            self.input_set_type = "string"
                            isOkay = True
                        elif type(innerElem) == float or type(innerElem) == int:
                            self.input_set_type = "number"
                            isOkay = True
                        elif type(innerElem) == tuple:
                            self.input_set_tuple_size = len(innerElem)
                            self.input_set_type = tuple(["n-tuple",
                                                            ["string" if type(innerTupleElem) == str else "number" for
                                                             innerTupleElem in innerElem]])
                            isOkay = True
                        elif type(innerElem) == FPTMapping:
                            self.input_set_type = "mapping"
                            isOkay = True
                        else:
                            print("WARNING: Inner Set type not supported")
                    if isOkay:
                        break
            else:
                print("WARNING: Mapping input type", self.func.inputType, "is not supported")
        elif self.func.inputMV is None:
            self.input_set_name = self.func.inputSetName
            self.input_set = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.input_set_name])

            if len(self.input_set) == 0 or type(self.input_set[0]) == str:
                self.input_type = "string"
            elif type(self.input_set[0]) == float or type(self.input_set[0]) == int:
                self.input_type = "number"
            elif type(self.input_set[0]) == FPTMapping:
                self.input_type = "mapping"
            elif type(self.input_set[0]) == tuple:
                self.input_type = "n-tuple"
                for elem in self.input_set:
                    self.input_tuple_types = []
                    self.input_tuple_size = len(elem)
                    for tupleElem in elem:
                        if type(tupleElem) == str:
                            self.input_tuple_types += ["string"]
                        elif type(tupleElem) == int or type(tupleElem) == float:
                            self.input_tuple_types += ["number"]
                        elif type(tupleElem) == frozenset or type(tupleElem) == set:
                            innerType = str
                            if len(tupleElem) > 0:
                                innerType = type(list(tupleElem)[0])
                            innerType = "string" if innerType == str else "number"
                            self.input_tuple_types += [tuple(["set", innerType])]
                        elif type(tupleElem) == tuple:
                            self.input_tuple_types += [tuple(["n-tuple",
                                                              ["string" if type(innerTupleElem) == str else "number"
                                                               for innerTupleElem in tupleElem]])]
                        elif type(tupleElem) == FPTMapping:
                            self.input_tuple_types += ["mapping"]
                    break
            elif type(self.input_set[0]) == set or type(self.input_set[0]) == frozenset:
                self.input_type = "set"
                for elem in self.input_set:
                    isOkay = False
                    for innerElem in elem:
                        if type(innerElem) == str:
                            self.input_set_type = "string"
                            isOkay = True
                        elif type(innerElem) == float or type(innerElem) == int:
                            self.input_set_type = "number"
                            isOkay = True
                        elif type(innerElem) == tuple:
                            self.input_set_tuple_size = len(innerElem)
                            self.input_set_type = tuple(["n-tuple",
                                                         ["string" if type(innerTupleElem) == str else "number" for
                                                          innerTupleElem in innerElem]])
                            isOkay = True
                        elif type(innerElem) == FPTMapping:
                            self.input_set_type = "mapping"
                            isOkay = True
                        else:
                            print("WARNING: Inner Set type not supported")
                    if isOkay:
                        break
            else:
                print("WARNING: Mapping input type", type(self.input_set[0]), "is not supported")
        else:
            self.input_set_name = "MV-algebra"
            self.input_mv = self.func.inputMV
            self.input_mv_k = self.func.inputMVK

            self.input_type = "number"

        self.output_set_type = "string"
        self.output_tuple_types = ["string", "string"]
        self.output_tuple_size = 2
        self.output_set_tuple_size = 2
        if self.func.outputSetName is None and self.func.outputMV is None:
            self.output_set_name = "custom set"

            if self.func.outputType == str:
                self.output_type = "string"
            elif self.func.outputType == float or self.func.outputType == int:
                self.output_type = "number"
            elif self.func.outputType == FPTMapping:
                self.output_type = "mapping"
            elif self.func.outputType == tuple:
                self.output_type = "n-tuple"
                for elem in self.func.listOfValues:
                    self.output_tuple_types = []
                    self.output_tuple_size = len(elem)
                    for tupleElem in elem:
                        if type(tupleElem) == str:
                            self.output_tuple_types += ["string"]
                        elif type(tupleElem) == int or type(tupleElem) == float:
                            self.output_tuple_types += ["number"]
                        elif type(tupleElem) == frozenset or type(tupleElem) == set:
                            innerType = str
                            if len(tupleElem) > 0:
                                innerType = type(list(tupleElem)[0])
                            innerType = "string" if innerType == str else "number"
                            self.output_tuple_types += [tuple(["set", innerType])]
                        elif type(tupleElem) == tuple:
                            self.output_tuple_types += [tuple(["n-tuple",
                                                              ["string" if type(innerTupleElem) == str else "number"
                                                               for innerTupleElem in tupleElem]])]
                        elif type(tupleElem) == FPTMapping:
                            self.output_tuple_types += ["mapping"]
                    break
            elif self.func.outputType == set or self.func.outputType == frozenset:
                self.output_type = "set"
                for elem in self.func.listOfValues:
                    isOkay = False
                    for innerElem in elem:
                        if type(innerElem) == str:
                            self.output_set_type = "string"
                            isOkay = True
                        elif type(innerElem) == float or type(innerElem) == int:
                            self.output_set_type = "number"
                            isOkay = True
                        elif type(innerElem) == tuple:
                            self.output_set_tuple_size = len(innerElem)
                            self.output_set_type = tuple(["n-tuple",
                                                         ["string" if type(innerTupleElem) == str else "number" for
                                                          innerTupleElem in innerElem]])
                            isOkay = True
                        elif type(innerElem) == FPTMapping:
                            self.output_set_type = "mapping"
                            isOkay = True
                        else:
                            print("WARNING: Inner Set type not supported")
                    if isOkay:
                        break
            else:
                print("WARNING: Mapping output type", self.func.outputType, "is not supported")
        elif self.func.outputMV is None:
            self.output_set_name = self.func.outputSetName
            self.output_set = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.output_set_name])

            if len(self.output_set) == 0 or type(self.output_set[0]) == str:
                self.output_type = "string"
            elif type(self.output_set[0]) == float or type(self.output_set[0]) == int:
                self.output_type = "number"
            elif type(self.output_set[0]) == FPTMapping:
                self.output_type = "mapping"
            elif type(self.output_set[0]) == tuple:
                self.output_type = "n-tuple"
                for elem in self.output_set:
                    self.output_tuple_types = []
                    self.output_tuple_size = len(elem)
                    for tupleElem in elem:
                        if type(tupleElem) == str:
                            self.output_tuple_types += ["string"]
                        elif type(tupleElem) == int or type(tupleElem) == float:
                            self.output_tuple_types += ["number"]
                        elif type(tupleElem) == frozenset or type(tupleElem) == set:
                            innerType = str
                            if len(tupleElem) > 0:
                                innerType = type(list(tupleElem)[0])
                            innerType = "string" if innerType == str else "number"
                            self.output_tuple_types += [tuple(["set", innerType])]
                        elif type(tupleElem) == tuple:
                            self.output_tuple_types += [tuple(["n-tuple",
                                                               ["string" if type(innerTupleElem) == str else "number"
                                                                for innerTupleElem in tupleElem]])]
                        elif type(tupleElem) == FPTMapping:
                            self.output_tuple_types += ["mapping"]
                    break
            elif type(self.output_set[0]) == set or type(self.output_set[0]) == frozenset:
                self.output_type = "set"
                for elem in self.output_set:
                    isOkay = False
                    for innerElem in elem:
                        if type(innerElem) == str:
                            self.output_set_type = "string"
                            isOkay = True
                        elif type(innerElem) == float or type(innerElem) == int:
                            self.output_set_type = "number"
                            isOkay = True
                        elif type(innerElem) == tuple:
                            self.output_set_tuple_size = len(innerElem)
                            self.output_set_type = tuple(["n-tuple",
                                                          ["string" if type(innerTupleElem) == str else "number" for
                                                           innerTupleElem in innerElem]])
                            isOkay = True
                        elif type(innerElem) == FPTMapping:
                            self.output_set_type = "mapping"
                            isOkay = True
                        else:
                            print("WARNING: Inner Set type not supported")
                    if isOkay:
                        break
            else:
                print("WARNING: Mapping output type", type(self.output_set[0]), "is not supported")
        else:
            self.output_set_name = "MV-algebra"
            self.output_mv = self.func.outputMV
            self.output_mv_k = self.func.outputMVK

            self.output_type = "number"

        if DEBUG:
            print(self.input_type)
            print(self.input_tuple_types)
            print(self.input_set_type)
            print(self.output_type)
            print(self.output_tuple_types)
            print(self.output_set_type)

        self.setWindowTitle("Edit mapping")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 200)

        self.name_label = QLabel("Name:")
        self.types_label = QLabel("Types:")
        self.content_label = QLabel("Content:")

        self.mapping_type_label = QLabel("Mapping type")
        self.input_set_label = QLabel("Domain")
        self.input_type_label = QLabel("\u2794 Type")
        self.output_set_label = QLabel("Codomain")
        self.output_type_label = QLabel("\u2794 Type")
        self.mapping_type_comboBox = QComboBox()
        self.input_set_comboBox = QComboBox()
        self.input_type_comboBox = QComboBox()
        self.output_set_comboBox = QComboBox()
        self.output_type_comboBox = QComboBox()

        self.mapping_type_comboBox.setMaximumWidth(137)
        self.input_set_comboBox.setMaximumWidth(137)
        self.input_type_comboBox.setMaximumWidth(137)
        self.input_set_comboBox.setMaximumWidth(137)
        self.output_set_comboBox.setMaximumWidth(137)
        self.output_type_comboBox.setMaximumWidth(137)

        self.mapping_type_label.setMargin(4)
        self.input_set_label.setMargin(4)
        self.input_type_label.setMargin(4)
        self.output_set_label.setMargin(4)
        self.output_type_label.setMargin(4)
        self.mapping_type_comboBox.addItems(FPTMapping.LIST_OF_MAPPING_TYPES)
        self.mapping_type_comboBox.setCurrentText(self.mapping_type)
        self.mapping_type_comboBox.currentIndexChanged.connect(self.onMappingTypeChanged)

        # # if empty sets should be disabled
        # nonEmptySets = []
        # for key in self.accessDicts.getDictionaryWithoutTransformation("sets").keys():
        #     if len(self.accessDicts.getDictionaryWithoutTransformation("sets")[key]) > 0:
        #         nonEmptySets.append(key)

        self.input_set_comboBox.addItem("custom set")
        self.input_set_comboBox.addItem("MV-algebra")
        self.input_set_comboBox.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())  # with empty sets
        self.input_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_TYPES)
        if self.input_set_name == "custom set":
            self.input_type_comboBox.setCurrentText(self.input_type)
        self.input_set_comboBox.setCurrentText(self.input_set_name)
        self.input_set_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        self.input_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.output_set_comboBox.addItem("custom set")
        self.output_set_comboBox.addItem("MV-algebra")
        self.output_set_comboBox.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())  # with empty sets
        self.output_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_TYPES)
        if self.output_set_name == "custom set":
            self.output_type_comboBox.setCurrentText(self.output_type)
        self.output_set_comboBox.setCurrentText(self.output_set_name)
        self.output_set_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        self.output_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.input_mv_algebra_label = QLabel("\u2794 MV-algebra")
        self.output_mv_algebra_label = QLabel("\u2794 MV-algebra")
        self.input_mv_algebra_label.setMargin(4)
        self.output_mv_algebra_label.setMargin(4)

        self.input_mv_algebra_k_label = QLabel("\u2794 k")
        self.output_mv_algebra_k_label = QLabel("\u2794 k")
        self.input_mv_algebra_k_label.setMargin(4)
        self.output_mv_algebra_k_label.setMargin(4)

        sp = self.input_mv_algebra_k_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.input_mv_algebra_k_label.setSizePolicy(sp)
        sp = self.output_mv_algebra_k_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.output_mv_algebra_k_label.setSizePolicy(sp)

        self.input_mv_algebra_comboBox = QComboBox()
        self.output_mv_algebra_comboBox = QComboBox()
        self.input_mv_algebra_comboBox.setMaximumWidth(137)
        self.output_mv_algebra_comboBox.setMaximumWidth(137)
        self.input_mv_algebra_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_MV_AlGEBRAS)
        self.output_mv_algebra_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_MV_AlGEBRAS)

        self.input_mv_algebra_comboBox.setItemData(0, "( [0, 1], \u2A01, 0, \u0304·\u0304 )\n"
                                                "x \u2A01 y = min{x + y, 1}\n"
                                                "x\u0304 = 1 - x", Qt.ToolTipRole)
        self.input_mv_algebra_comboBox.setItemData(1, "( {0,...,k}, \u2A01, 0, \u0304·\u0304 )\n"
                                                "x \u2A01 y = min{x + y, k}\n"
                                                "x\u0304 = k - x", Qt.ToolTipRole)
        self.output_mv_algebra_comboBox.setItemData(0, "( [0, 1], \u2A01, 0, \u0304·\u0304 )\n"
                                                      "x \u2A01 y = min{x + y, 1}\n"
                                                      "x\u0304 = 1 - x", Qt.ToolTipRole)
        self.output_mv_algebra_comboBox.setItemData(1, "( {0,...,k}, \u2A01, 0, \u0304·\u0304 )\n"
                                                      "x \u2A01 y = min{x + y, k}\n"
                                                      "x\u0304 = k - x", Qt.ToolTipRole)

        self.input_mv_algebra_k = QLineEdit()
        self.output_mv_algebra_k = QLineEdit()

        self.input_mv_algebra_k.setMaximumWidth(137)
        self.output_mv_algebra_k.setMaximumWidth(137)

        onlyInt = QIntValidator(1, 99999)
        self.input_mv_algebra_k.setValidator(onlyInt)
        self.output_mv_algebra_k.setValidator(onlyInt)

        self.input_mv_algebra_k.setText("1")
        self.output_mv_algebra_k.setText("1")

        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

        if self.input_set_name == "MV-algebra":
            self.input_mv_algebra_comboBox.setCurrentText(self.input_mv)
            self.input_mv_algebra_k.setText(self.input_mv_k)
        else:
            self.input_mv_algebra_comboBox.setCurrentText(config['all']['mv-algebra'])
            self.input_mv_algebra_k.setText(config['all']['k'])

        if self.output_set_name == "MV-algebra":
            self.output_mv_algebra_comboBox.setCurrentText(self.output_mv)
            self.output_mv_algebra_k.setText(self.output_mv_k)
        else:
            self.output_mv_algebra_comboBox.setCurrentText(config['all']['mv-algebra'])
            self.output_mv_algebra_k.setText(config['all']['k'])

        self.input_mv_algebra_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        self.output_mv_algebra_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.input_mv_algebra_k.textChanged.connect(self.onTypeChanged)
        self.output_mv_algebra_k.textChanged.connect(self.onTypeChanged)

        self.input_mv_algebra_k.textChanged.connect(lambda text: self.fixKValue(self.input_mv_algebra_k, text))
        self.output_mv_algebra_k.textChanged.connect(lambda text: self.fixKValue(self.output_mv_algebra_k, text))

        self.mapping_type_hbox = QHBoxLayout()
        self.mapping_type_hbox.addWidget(self.mapping_type_label)
        self.mapping_type_hbox.addWidget(self.mapping_type_comboBox)

        self.input_mv_algebra_box = QHBoxLayout()
        self.input_mv_algebra_box.addWidget(self.input_mv_algebra_label)
        self.input_mv_algebra_box.addWidget(self.input_mv_algebra_comboBox)

        self.output_mv_algebra_box = QHBoxLayout()
        self.output_mv_algebra_box.addWidget(self.output_mv_algebra_label)
        self.output_mv_algebra_box.addWidget(self.output_mv_algebra_comboBox)

        self.input_mv_algebra_k_box = QHBoxLayout()
        self.input_mv_algebra_k_box.addWidget(self.input_mv_algebra_k_label)
        self.input_mv_algebra_k_box.addWidget(self.input_mv_algebra_k)

        self.output_mv_algebra_k_box = QHBoxLayout()
        self.output_mv_algebra_k_box.addWidget(self.output_mv_algebra_k_label)
        self.output_mv_algebra_k_box.addWidget(self.output_mv_algebra_k)

        self.input_set_hbox = QHBoxLayout()
        self.input_set_hbox.addWidget(self.input_set_label)
        self.input_set_hbox.addWidget(self.input_set_comboBox)

        self.input_type_hbox = QHBoxLayout()
        self.input_type_hbox.addWidget(self.input_type_label)
        self.input_type_hbox.addWidget(self.input_type_comboBox)

        self.output_set_hbox = QHBoxLayout()
        self.output_set_hbox.addWidget(self.output_set_label)
        self.output_set_hbox.addWidget(self.output_set_comboBox)

        self.output_type_hbox = QHBoxLayout()
        self.output_type_hbox.addWidget(self.output_type_label)
        self.output_type_hbox.addWidget(self.output_type_comboBox)

        self.input_set_type_label = QLabel("\u2794 Set type")
        self.input_set_type_label.setMargin(4)
        self.output_set_type_label = QLabel("\u2794 Set type")
        self.output_set_type_label.setMargin(4)

        self.input_set_type_comboBox = QComboBox()
        self.input_set_type_comboBox.setMaximumWidth(137)
        self.input_set_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_SET_TYPES)
        if self.input_set_name == "custom set":
            if type(self.input_set_type) == tuple:
                self.input_set_type_comboBox.setCurrentText(self.input_set_type[0])
            else:
                self.input_set_type_comboBox.setCurrentText(self.input_set_type)
        self.output_set_type_comboBox = QComboBox()
        self.output_set_type_comboBox.setMaximumWidth(137)
        self.output_set_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_SET_TYPES)
        if self.output_set_name == "custom set":
            if type(self.output_set_type) == tuple:
                self.output_set_type_comboBox.setCurrentText(self.output_set_type[0])
            else:
                self.output_set_type_comboBox.setCurrentText(self.output_set_type)
        self.input_set_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        self.output_set_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.input_set_type_hbox = QHBoxLayout()
        self.input_set_type_hbox.addWidget(self.input_set_type_label)
        self.input_set_type_hbox.addWidget(self.input_set_type_comboBox)
        self.output_set_type_hbox = QHBoxLayout()
        self.output_set_type_hbox.addWidget(self.output_set_type_label)
        self.output_set_type_hbox.addWidget(self.output_set_type_comboBox)

        self.input_set_tuple_n_label = QLabel("n")
        self.input_set_tuple_n_label.setMargin(8)
        self.output_set_tuple_n_label = QLabel("n")
        self.output_set_tuple_n_label.setMargin(8)

        sp = self.input_set_tuple_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.input_set_tuple_n_label.setSizePolicy(sp)
        self.output_set_tuple_n_label.setSizePolicy(sp)

        onlyInt = QIntValidator(2, 9)

        self.input_set_tuple_n_lineEdit = QLineEdit()
        self.input_set_tuple_n_lineEdit.setValidator(onlyInt)
        self.input_set_tuple_n_lineEdit.setText(str(self.input_set_tuple_size))
        self.input_set_tuple_n_lineEdit.textChanged.connect(self.onInputInnerNChanged)

        self.output_set_tuple_n_lineEdit = QLineEdit()
        self.output_set_tuple_n_lineEdit.setValidator(onlyInt)
        self.output_set_tuple_n_lineEdit.setText(str(self.output_set_tuple_size))
        self.output_set_tuple_n_lineEdit.textChanged.connect(self.onOutputInnerNChanged)

        self.input_set_tuple_n_box = QHBoxLayout()
        self.input_set_tuple_n_box.addWidget(self.input_set_tuple_n_label)
        self.input_set_tuple_n_box.addWidget(self.input_set_tuple_n_lineEdit)

        self.output_set_tuple_n_box = QHBoxLayout()
        self.output_set_tuple_n_box.addWidget(self.output_set_tuple_n_label)
        self.output_set_tuple_n_box.addWidget(self.output_set_tuple_n_lineEdit)

        self.input_set_tupleType_label = QLabel("Tuple types:")
        self.input_set_tupleType_label.setMargin(8)
        self.output_set_tupleType_label = QLabel("Tuple types:")
        self.output_set_tupleType_label.setMargin(8)

        self.input_set_tupleType_button = QPushButton("Edit")
        self.input_set_tupleType_button.setDefault(False)
        self.input_set_tupleType_button.setAutoDefault(False)
        self.input_set_tupleType_button.clicked.connect(self.onInputSetTupleTypesButtonClicked)

        self.output_set_tupleType_button = QPushButton("Edit")
        self.output_set_tupleType_button.setDefault(False)
        self.output_set_tupleType_button.setAutoDefault(False)
        self.output_set_tupleType_button.clicked.connect(self.onOutputSetTupleTypesButtonClicked)

        self.input_set_tupleType_box = QHBoxLayout()
        self.input_set_tupleType_box.addWidget(self.input_set_tupleType_label)
        self.input_set_tupleType_box.addWidget(self.input_set_tupleType_button)

        self.output_set_tupleType_box = QHBoxLayout()
        self.output_set_tupleType_box.addWidget(self.output_set_tupleType_label)
        self.output_set_tupleType_box.addWidget(self.output_set_tupleType_button)

        self.input_tuple_n_label = QLabel("n:")
        self.input_tuple_n_label.setMargin(4)
        self.output_tuple_n_label = QLabel("n:")
        self.output_tuple_n_label.setMargin(4)

        sp = self.input_tuple_n_label.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.input_tuple_n_label.setSizePolicy(sp)
        self.output_tuple_n_label.setSizePolicy(sp)

        self.input_tuple_n_lineEdit = QLineEdit()
        self.input_tuple_n_lineEdit.setValidator(onlyInt)
        self.input_tuple_n_lineEdit.setText(str(self.input_tuple_size))
        self.input_tuple_n_lineEdit.textChanged.connect(self.onInputNChanged)

        self.output_tuple_n_lineEdit = QLineEdit()
        self.output_tuple_n_lineEdit.setValidator(onlyInt)
        self.output_tuple_n_lineEdit.setText(str(self.output_tuple_size))
        self.output_tuple_n_lineEdit.textChanged.connect(self.onOutputNChanged)

        self.input_tuple_n_box = QHBoxLayout()
        self.input_tuple_n_box.addWidget(self.input_tuple_n_label)
        self.input_tuple_n_box.addWidget(self.input_tuple_n_lineEdit)

        self.output_tuple_n_box = QHBoxLayout()
        self.output_tuple_n_box.addWidget(self.output_tuple_n_label)
        self.output_tuple_n_box.addWidget(self.output_tuple_n_lineEdit)

        self.input_tupleType_label = QLabel("Tuple types:")
        self.input_tupleType_label.setMargin(4)
        self.output_tupleType_label = QLabel("Tuple types:")
        self.output_tupleType_label.setMargin(4)

        self.input_tupleType_button = QPushButton("Edit")
        self.input_tupleType_button.setDefault(False)
        self.input_tupleType_button.setAutoDefault(False)
        self.input_tupleType_button.clicked.connect(self.onInputTupleTypesButtonClicked)

        self.output_tupleType_button = QPushButton("Edit")
        self.output_tupleType_button.setDefault(False)
        self.output_tupleType_button.setAutoDefault(False)
        self.output_tupleType_button.clicked.connect(self.onOutputTupleTypesButtonClicked)

        self.input_tupleType_box = QHBoxLayout()
        self.input_tupleType_box.addWidget(self.input_tupleType_label)
        self.input_tupleType_box.addWidget(self.input_tupleType_button)

        self.output_tupleType_box = QHBoxLayout()
        self.output_tupleType_box.addWidget(self.output_tupleType_label)
        self.output_tupleType_box.addWidget(self.output_tupleType_button)

        # self.input_tuple_type_label = QLabel("\u2794 Tuple type")
        # self.input_tuple_type_label.setMargin(4)
        # self.output_tuple_type_label = QLabel("\u2794 Tuple type")
        # self.output_tuple_type_label.setMargin(4)
        #
        # self.input_tuple_type_comboBox = QComboBox()
        # self.input_tuple_type_comboBox.setMaximumWidth(137)
        # self.input_tuple_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_TUPLE_TYPES)
        # if self.input_set_name == "custom set":
        #     self.input_tuple_type_comboBox.setCurrentText(self.input_tuple_types)
        # self.output_tuple_type_comboBox = QComboBox()
        # self.output_tuple_type_comboBox.setMaximumWidth(137)
        # self.output_tuple_type_comboBox.addItems(QDMContentListWidgetMappingPopup.LIST_OF_TUPLE_TYPES)
        # if self.output_set_name == "custom set":
        #     self.output_tuple_type_comboBox.setCurrentText(self.output_tuple_types)
        # self.input_tuple_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        # self.output_tuple_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)
        #
        # self.input_tuple_type_hbox = QHBoxLayout()
        # self.input_tuple_type_hbox.addWidget(self.input_tuple_type_label)
        # self.input_tuple_type_hbox.addWidget(self.input_tuple_type_comboBox)
        # self.output_tuple_type_hbox = QHBoxLayout()
        # self.output_tuple_type_hbox.addWidget(self.output_tuple_type_label)
        # self.output_tuple_type_hbox.addWidget(self.output_tuple_type_comboBox)

        self.name_textEdit = QTextEdit(self.func_name)
        self.name_textEdit.setFixedHeight(23)
        self.name_textEdit.textChanged.connect(self.onNameChanged)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.setDefault(False)
        self.save_button.setAutoDefault(False)
        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)
        self.save_button.clicked.connect(self.onSave)
        self.cancel_button.clicked.connect(self.onCancel)

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                            input_mv=self.input_mv,
                                            input_mv_k=self.input_mv_k,
                                            output_mv=self.output_mv,
                                            output_mv_k=self.output_mv_k)

        self.mappingEdit.addMappings(self.list_of_elements, self.list_of_values)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(280, 200)
        self.scroll.setWidget(self.mappingEdit)
        self.scroll.verticalScrollBar().rangeChanged.connect(self.moveScrollBarToBottom)

        self.delete_button = QPushButton("-")
        self.delete_button.setFixedSize(23, 23)
        self.delete_button.setDefault(False)
        self.delete_button.setAutoDefault(False)
        self.delete_button.clicked.connect(self.onDeleteButtonClicked)

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(23, 23)
        self.add_button.setDefault(False)
        self.add_button.setAutoDefault(False)
        self.add_button.clicked.connect(self.onAddButtonClicked)

        self.add_all_button = QPushButton("++")
        self.add_all_button.setFixedSize(23, 23)
        self.add_all_button.setDefault(False)
        self.add_all_button.setAutoDefault(False)
        self.add_all_button.clicked.connect(self.onAddAllButtonClicked)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.cancel_button)

        self.addBox = QHBoxLayout()
        self.addBox.addWidget(self.delete_button)
        self.addBox.addWidget(self.add_button)
        self.addBox.addWidget(self.add_all_button)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.name_label)
        self.vbox.addWidget(self.name_textEdit)
        self.vbox.addWidget(self.types_label)
        self.vbox.addLayout(self.mapping_type_hbox)
        self.vbox.addLayout(self.input_set_hbox)
        self.vbox.addLayout(self.input_mv_algebra_box)
        self.vbox.addLayout(self.input_mv_algebra_k_box)
        self.vbox.addLayout(self.input_type_hbox)
        self.vbox.addLayout(self.input_set_type_hbox)
        self.vbox.addLayout(self.input_set_tuple_n_box)
        self.vbox.addLayout(self.input_set_tupleType_box)
        # self.vbox.addLayout(self.input_tuple_type_hbox)
        self.vbox.addLayout(self.input_tuple_n_box)
        self.vbox.addLayout(self.input_tupleType_box)
        self.vbox.addLayout(self.output_set_hbox)
        self.vbox.addLayout(self.output_mv_algebra_box)
        self.vbox.addLayout(self.output_mv_algebra_k_box)
        self.vbox.addLayout(self.output_type_hbox)
        self.vbox.addLayout(self.output_set_type_hbox)
        self.vbox.addLayout(self.output_set_tuple_n_box)
        self.vbox.addLayout(self.output_set_tupleType_box)
        # self.vbox.addLayout(self.output_tuple_type_hbox)
        self.vbox.addLayout(self.output_tuple_n_box)
        self.vbox.addLayout(self.output_tupleType_box)
        self.vbox.addWidget(self.content_label)
        self.vbox.addWidget(self.scroll)
        self.vbox.addLayout(self.addBox)
        self.vbox.setAlignment(self.addBox, Qt.AlignRight)
        self.vbox.addLayout(self.hbox)

        self.add_all_button.setVisible(self.input_set_name != "custom set" and self.input_set_name != "MV-algebra")
        self.input_type_label.setVisible(self.input_set_name == "custom set")
        self.input_type_comboBox.setVisible(self.input_set_name == "custom set")
        self.output_type_label.setVisible(self.output_set_name == "custom set")
        self.output_type_comboBox.setVisible(self.output_set_name == "custom set")
        self.input_set_type_label.setVisible(self.input_set_name == "custom set" and self.input_type == "set")
        self.input_set_type_comboBox.setVisible(self.input_set_name == "custom set" and self.input_type == "set")
        self.input_set_tuple_n_label.setVisible(
            self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[
                0] == "n-tuple")
        self.input_set_tuple_n_lineEdit.setVisible(
            self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[
                0] == "n-tuple")
        self.input_set_tupleType_label.setVisible(
            self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[
                0] == "n-tuple")
        self.input_set_tupleType_button.setVisible(
            self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[
                0] == "n-tuple")
        self.output_set_type_label.setVisible(self.output_set_name == "custom set" and self.output_type == "set")
        self.output_set_type_comboBox.setVisible(self.output_set_name == "custom set" and self.output_type == "set")
        self.output_set_tuple_n_label.setVisible(
            self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[
                0] == "n-tuple")
        self.output_set_tuple_n_lineEdit.setVisible(
            self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[
                0] == "n-tuple")
        self.output_set_tupleType_label.setVisible(
            self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[
                0] == "n-tuple")
        self.output_set_tupleType_button.setVisible(
            self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[
                0] == "n-tuple")
        self.input_tuple_n_label.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
        self.input_tuple_n_lineEdit.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
        self.input_tupleType_label.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
        self.input_tupleType_button.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
        self.output_tuple_n_label.setVisible(self.output_set_name == "custom set" and self.output_type == "n-tuple")
        self.output_tuple_n_lineEdit.setVisible(
            self.output_set_name == "custom set" and self.output_type == "n-tuple")
        self.output_tupleType_label.setVisible(
            self.output_set_name == "custom set" and self.output_type == "n-tuple")
        self.output_tupleType_button.setVisible(
            self.output_set_name == "custom set" and self.output_type == "n-tuple")
        self.input_mv_algebra_label.setVisible(self.input_set_name == "MV-algebra")
        self.input_mv_algebra_comboBox.setVisible(self.input_set_name == "MV-algebra")
        self.input_mv_algebra_k_label.setVisible(self.input_set_name == "MV-algebra")
        self.input_mv_algebra_k.setVisible(self.input_set_name == "MV-algebra")
        self.output_mv_algebra_label.setVisible(self.output_set_name == "MV-algebra")
        self.output_mv_algebra_comboBox.setVisible(self.output_set_name == "MV-algebra")
        self.output_mv_algebra_k_label.setVisible(self.output_set_name == "MV-algebra")
        self.output_mv_algebra_k.setVisible(self.output_set_name == "MV-algebra")

        self.setLayout(self.vbox)

    def onNameChanged(self):
        self.func_name = self.name_textEdit.toPlainText()

    def onInputNChanged(self):
        if self.input_tuple_n_lineEdit.text() == "0" or self.input_tuple_n_lineEdit.text() == "1":
            self.input_tuple_n_lineEdit.setText("2")
        try:
            self.input_tuple_size = int(self.input_tuple_n_lineEdit.text())
        except Exception:
            self.input_tuple_size = 2
            self.input_tuple_n_lineEdit.setText("2")
        self.input_tuple_types = ["string"] * self.input_tuple_size

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onOutputNChanged(self):
        if self.output_tuple_n_lineEdit.text() == "0" or self.output_tuple_n_lineEdit.text() == "1":
            self.output_tuple_n_lineEdit.setText("2")
        try:
            self.output_tuple_size = int(self.output_tuple_n_lineEdit.text())
        except Exception:
            self.output_tuple_size = 2
            self.output_tuple_n_lineEdit.setText("2")
        self.output_tuple_types = ["string"] * self.output_tuple_size

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onInputTupleTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.input_tuple_types))
        if pop.exec():
            if self.input_tuple_types != pop.types_of_tuple:
                self.input_tuple_types = pop.types_of_tuple

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onOutputTupleTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.output_tuple_types))
        if pop.exec():
            if self.output_tuple_types != pop.types_of_tuple:
                self.output_tuple_types = pop.types_of_tuple

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onInputInnerNChanged(self):
        if self.input_set_tuple_n_lineEdit.text() == "0" or self.input_set_tuple_n_lineEdit.text() == "1":
            self.input_set_tuple_n_lineEdit.setText("2")
        try:
            self.input_set_tuple_size = int(self.input_set_tuple_n_lineEdit.text())
        except Exception:
            self.input_set_tuple_size = 2
            self.input_set_tuple_n_lineEdit.setText("2")
        self.input_set_type = tuple(["n-tuple", ["string"]*self.input_set_tuple_size])

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onOutputInnerNChanged(self):
        if self.output_set_tuple_n_lineEdit.text() == "0" or self.output_set_tuple_n_lineEdit.text() == "1":
            self.output_set_tuple_n_lineEdit.setText("2")
        try:
            self.output_set_tuple_size = int(self.output_set_tuple_n_lineEdit.text())
        except Exception:
            self.output_set_tuple_size = 2
            self.output_set_tuple_n_lineEdit.setText("2")
        self.output_set_type = tuple(["n-tuple", ["string"] * self.output_set_tuple_size])

        if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
            if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_set_name != "custom set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_set_type=self.output_set_type)
            elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "set" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "n-tuple" and self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_set_type=self.output_set_type)
            elif self.input_type == "set" and self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name)
            elif self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_tuple_type=self.output_tuple_types)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_set_type=self.output_set_type)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
        elif self.input_set_name != "MV-algebra":
            if self.input_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  input_set_type=self.input_set_type,
                                                  input_set=self.input_set_name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_set_type=self.input_set_type,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            elif self.input_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_tuple_type=self.input_tuple_types,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)
        elif self.output_set_name != "MV-algebra":
            if self.output_set_name != "custom set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types,
                                                  output_set_type=self.output_set_type,
                                                  output_set=self.output_set_name)
            elif self.output_type == "set":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_set_type=self.output_set_type)
            elif self.output_type == "n-tuple":
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_tuple_type=self.output_tuple_types)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k)
        else:
            self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                              input_mv=self.input_mv,
                                              input_mv_k=self.input_mv_k,
                                              output_mv=self.output_mv,
                                              output_mv_k=self.output_mv_k)

        self.scroll.setWidget(self.mappingEdit)

    def onInputSetTupleTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.input_set_type[1]), inner=True)
        if pop.exec():
            if self.input_set_type[1] != pop.types_of_tuple:
                self.input_set_type = tuple(["n-tuple", pop.types_of_tuple])

                if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
                    if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_set_name != "custom set" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_set_type=self.output_set_type)
                    elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "set" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_set_type=self.input_set_type,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "set" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_set_type=self.output_set_type)
                    elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "n-tuple" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_set_type=self.output_set_type)
                    elif self.input_type == "set" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name)
                    elif self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types)
                    elif self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type)
                    elif self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_set_type=self.output_set_type)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
                elif self.input_set_name != "MV-algebra":
                    if self.input_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    elif self.input_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    elif self.input_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                elif self.output_set_name != "MV-algebra":
                    if self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_set_type=self.output_set_type)
                    elif self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_tuple_type=self.output_tuple_types)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k)
                else:
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)

                self.scroll.setWidget(self.mappingEdit)

    def onOutputSetTupleTypesButtonClicked(self):
        pop = QDMContentListWidgetTupleTypePopup(copy.deepcopy(self.output_set_type[1]), inner=True)
        if pop.exec():
            if self.output_set_type[1] != pop.types_of_tuple:
                self.output_set_type = tuple(["n-tuple", pop.types_of_tuple])

                if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
                    if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_set_name != "custom set" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_set_type=self.output_set_type)
                    elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "set" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_set_type=self.input_set_type,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "set" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_set_type=self.output_set_type)
                    elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "n-tuple" and self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_set_type=self.output_set_type)
                    elif self.input_type == "set" and self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name)
                    elif self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.input_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types)
                    elif self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_tuple_type=self.output_tuple_types)
                    elif self.input_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type)
                    elif self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_set_type=self.output_set_type)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
                elif self.input_set_name != "MV-algebra":
                    if self.input_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          input_set_type=self.input_set_type,
                                                          input_set=self.input_set_name,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    elif self.input_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_set_type=self.input_set_type,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    elif self.input_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_tuple_type=self.input_tuple_types,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          output_mv=self.output_mv,
                                                          output_mv_k=self.output_mv_k)
                elif self.output_set_name != "MV-algebra":
                    if self.output_set_name != "custom set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_tuple_type=self.output_tuple_types,
                                                          output_set_type=self.output_set_type,
                                                          output_set=self.output_set_name)
                    elif self.output_type == "set":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_set_type=self.output_set_type)
                    elif self.output_type == "n-tuple":
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k,
                                                          output_tuple_type=self.output_tuple_types)
                    else:
                        self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                          input_mv=self.input_mv,
                                                          input_mv_k=self.input_mv_k)
                else:
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)

                self.scroll.setWidget(self.mappingEdit)

    def onTypeChanged(self):
        try:
            self.input_set_name = self.input_set_comboBox.currentText()
            self.output_set_name = self.output_set_comboBox.currentText()

            if self.input_set_name == "custom set":
                self.input_type = self.input_type_comboBox.currentText()
                self.input_set_type = self.input_set_type_comboBox.currentText()
                if self.input_set_type == "n-tuple":
                    self.input_set_type = tuple(["n-tuple", ["string"]*self.input_set_tuple_size])
                # self.input_tuple_types = self.input_tuple_type_comboBox.currentText()
            elif self.input_set_name == "MV-algebra":
                self.input_mv = self.input_mv_algebra_comboBox.currentText()
                self.input_mv_k = self.input_mv_algebra_k.text()

                self.input_type = "number"
            else:
                self.input_set = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.input_set_name])
                type_of_set = str
                for elem in self.input_set:
                    type_of_set = type(elem)
                    break

                self.input_type = "string"
                self.input_set_type = "string"
                self.input_tuple_types = ["string", "string"]
                self.input_tuple_size = 2
                self.input_set_tuple_size = 2
                if type_of_set == str:
                    self.input_type = "string"
                elif type_of_set == float or type_of_set == int:
                    self.input_type = "number"
                elif type_of_set == FPTMapping:
                    self.input_type = "mapping"
                elif type_of_set == tuple:
                    self.input_type = "n-tuple"
                    for elem in self.input_set:
                        self.input_tuple_types = []
                        self.input_tuple_size = len(elem)
                        for tupleElem in elem:
                            if type(tupleElem) == str:
                                self.input_tuple_types += ["string"]
                            elif type(tupleElem) == int or type(tupleElem) == float:
                                self.input_tuple_types += ["number"]
                            elif type(tupleElem) == frozenset or type(tupleElem) == set:
                                innerType = str
                                if len(tupleElem) > 0:
                                    innerType = type(list(tupleElem)[0])
                                innerType = "string" if innerType == str else "number"
                                self.input_tuple_types += [tuple(["set", innerType])]
                            elif type(tupleElem) == tuple:
                                self.input_tuple_types += [tuple(["n-tuple",
                                                                  ["string" if type(innerTupleElem) == str else "number"
                                                                   for innerTupleElem in tupleElem]])]
                            elif type(tupleElem) == FPTMapping:
                                self.input_tuple_types += ["mapping"]
                        break
                elif type_of_set == set or type_of_set == frozenset:
                    self.input_type = "set"
                    for elem in self.input_set:
                        isOkay = False
                        for innerElem in elem:
                            if type(innerElem) == str:
                                self.input_set_type = "string"
                                isOkay = True
                            elif type(innerElem) == float or type(innerElem) == int:
                                self.input_set_type = "number"
                                isOkay = True
                            elif type(innerElem) == tuple:
                                self.input_set_tuple_size = len(innerElem)
                                self.input_set_type = tuple(["n-tuple",
                                                             ["string" if type(innerTupleElem) == str else "number" for
                                                              innerTupleElem in innerElem]])
                                isOkay = True
                            elif type(innerElem) == FPTMapping:
                                self.input_set_type = "mapping"
                                isOkay = True
                            else:
                                print("WARNING: Inner Set type not supported")
                        if isOkay:
                            break
                else:
                    print("WARNING: Mapping input type", type_of_set, "is not supported")

            if self.output_set_name == "custom set":
                self.output_type = self.output_type_comboBox.currentText()
                self.output_set_type = self.output_set_type_comboBox.currentText()
                if self.output_set_type == "n-tuple":
                    self.output_set_type = tuple(["n-tuple", ["string"]*self.output_set_tuple_size])
                # self.output_tuple_types = self.output_tuple_type_comboBox.currentText()
            elif self.output_set_name == "MV-algebra":
                self.output_mv = self.output_mv_algebra_comboBox.currentText()
                self.output_mv_k = self.output_mv_algebra_k.text()

                self.output_type = "number"
            else:
                self.output_set = list(self.accessDicts.getDictionaryWithoutTransformation("sets")[self.output_set_name])
                type_of_set = str
                for elem in self.output_set:
                    type_of_set = type(elem)
                    break

                self.output_type = "string"
                self.output_set_type = "string"
                self.output_tuple_types = ["string", "string"]
                self.output_tuple_size = 2
                self.output_set_tuple_size = 2
                if type_of_set == str:
                    self.output_type = "string"
                elif type_of_set == float or type_of_set == int:
                    self.output_type = "number"
                elif type_of_set == FPTMapping:
                    self.output_type = "mapping"
                elif type_of_set == tuple:
                    self.output_type = "n-tuple"
                    for elem in self.output_set:
                        self.output_tuple_types = []
                        self.output_tuple_size = len(elem)
                        for tupleElem in elem:
                            if type(tupleElem) == str:
                                self.output_tuple_types += ["string"]
                            elif type(tupleElem) == int or type(tupleElem) == float:
                                self.output_tuple_types += ["number"]
                            elif type(tupleElem) == frozenset or type(tupleElem) == set:
                                innerType = str
                                if len(tupleElem) > 0:
                                    innerType = type(list(tupleElem)[0])
                                innerType = "string" if innerType == str else "number"
                                self.output_tuple_types += [tuple(["set", innerType])]
                            elif type(tupleElem) == tuple:
                                self.output_tuple_types += [tuple(["n-tuple",
                                                                   ["string" if type(
                                                                       innerTupleElem) == str else "number"
                                                                    for innerTupleElem in tupleElem]])]
                            elif type(tupleElem) == FPTMapping:
                                self.output_tuple_types += ["mapping"]
                        break
                elif type_of_set == set or type_of_set == frozenset:
                    self.output_type = "set"
                    for elem in self.output_set:
                        isOkay = False
                        for innerElem in elem:
                            if type(innerElem) == str:
                                self.output_set_type = "string"
                                isOkay = True
                            elif type(innerElem) == float or type(innerElem) == int:
                                self.output_set_type = "number"
                                isOkay = True
                            elif type(innerElem) == tuple:
                                self.output_set_tuple_size = len(innerElem)
                                self.output_set_type = tuple(["n-tuple",
                                                              ["string" if type(innerTupleElem) == str else "number" for
                                                               innerTupleElem in innerElem]])
                                isOkay = True
                            elif type(innerElem) == FPTMapping:
                                self.output_set_type = "mapping"
                                isOkay = True
                            else:
                                print("WARNING: Inner Set type not supported")
                        if isOkay:
                            break
                else:
                    print("WARNING: Mapping output type", type_of_set, "is not supported")

            if self.input_set_name != "MV-algebra" and self.output_set_name != "MV-algebra":
                if self.input_set_name != "custom set" and self.output_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      input_set_type=self.input_set_type,
                                                      input_set=self.input_set_name,
                                                      output_tuple_type=self.output_tuple_types,
                                                      output_set_type=self.output_set_type,
                                                      output_set=self.output_set_name)
                elif self.input_set_name != "custom set" and self.output_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      input_set_type=self.input_set_type,
                                                      input_set=self.input_set_name,
                                                      output_set_type=self.output_set_type)
                elif self.input_set_name != "custom set" and self.output_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      input_set_type=self.input_set_type,
                                                      input_set=self.input_set_name,
                                                      output_tuple_type=self.output_tuple_types)
                elif self.input_type == "set" and self.output_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_set_type=self.input_set_type,
                                                      output_tuple_type=self.output_tuple_types,
                                                      output_set_type=self.output_set_type,
                                                      output_set=self.output_set_name)
                elif self.input_type == "n-tuple" and self.output_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      output_tuple_type=self.output_tuple_types,
                                                      output_set_type=self.output_set_type,
                                                      output_set=self.output_set_name)
                elif self.input_type == "set" and self.output_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_set_type=self.input_set_type,
                                                      output_set_type=self.output_set_type)
                elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      output_tuple_type=self.output_tuple_types)
                elif self.input_type == "n-tuple" and self.output_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      output_set_type=self.output_set_type)
                elif self.input_type == "set" and self.output_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_set_type=self.input_set_type,
                                                      output_tuple_type=self.output_tuple_types)
                elif self.input_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      input_set_type=self.input_set_type,
                                                      input_set=self.input_set_name)
                elif self.output_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      output_tuple_type=self.output_tuple_types,
                                                      output_set_type=self.output_set_type,
                                                      output_set=self.output_set_name)
                elif self.input_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_tuple_type=self.input_tuple_types)
                elif self.output_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      output_tuple_type=self.output_tuple_types)
                elif self.input_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_set_type=self.input_set_type)
                elif self.output_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      output_set_type=self.output_set_type)
                else:
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name)
            elif self.input_set_name != "MV-algebra":
                if self.input_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      input_set_type=self.input_set_type,
                                                      input_set=self.input_set_name,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)
                elif self.input_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_set_type=self.input_set_type,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)
                elif self.input_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_tuple_type=self.input_tuple_types,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)
                else:
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      output_mv=self.output_mv,
                                                      output_mv_k=self.output_mv_k)
            elif self.output_set_name != "MV-algebra":
                if self.output_set_name != "custom set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k,
                                                      output_tuple_type=self.output_tuple_types,
                                                      output_set_type=self.output_set_type,
                                                      output_set=self.output_set_name)
                elif self.output_type == "set":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k,
                                                      output_set_type=self.output_set_type)
                elif self.output_type == "n-tuple":
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k,
                                                      output_tuple_type=self.output_tuple_types)
                else:
                    self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func.name,
                                                      input_mv=self.input_mv,
                                                      input_mv_k=self.input_mv_k)
            else:
                self.mappingEdit = QDMMappingEdit(self.input_type, self.output_type, self.func_name,
                                                  input_mv=self.input_mv,
                                                  input_mv_k=self.input_mv_k,
                                                  output_mv=self.output_mv,
                                                  output_mv_k=self.output_mv_k)

            self.scroll.setWidget(self.mappingEdit)

            self.add_all_button.setVisible(self.input_set_name != "custom set" and self.input_set_name != "MV-algebra")
            self.input_type_label.setVisible(self.input_set_name == "custom set")
            self.input_type_comboBox.setVisible(self.input_set_name == "custom set")
            self.output_type_label.setVisible(self.output_set_name == "custom set")
            self.output_type_comboBox.setVisible(self.output_set_name == "custom set")
            self.input_set_type_label.setVisible(self.input_set_name == "custom set" and self.input_type == "set")
            self.input_set_type_comboBox.setVisible(self.input_set_name == "custom set" and self.input_type == "set")
            self.input_set_tuple_n_label.setVisible(self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[0] == "n-tuple")
            self.input_set_tuple_n_lineEdit.setVisible(self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[0] == "n-tuple")
            self.input_set_tupleType_label.setVisible(self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[0] == "n-tuple")
            self.input_set_tupleType_button.setVisible(self.input_set_name == "custom set" and self.input_type == "set" and self.input_set_type[0] == "n-tuple")
            self.output_set_type_label.setVisible(self.output_set_name == "custom set" and self.output_type == "set")
            self.output_set_type_comboBox.setVisible(self.output_set_name == "custom set" and self.output_type == "set")
            self.output_set_tuple_n_label.setVisible(self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[0] == "n-tuple")
            self.output_set_tuple_n_lineEdit.setVisible(self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[0] == "n-tuple")
            self.output_set_tupleType_label.setVisible(self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[0] == "n-tuple")
            self.output_set_tupleType_button.setVisible(self.output_set_name == "custom set" and self.output_type == "set" and self.output_set_type[0] == "n-tuple")
            self.input_tuple_n_label.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
            self.input_tuple_n_lineEdit.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
            self.input_tupleType_label.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
            self.input_tupleType_button.setVisible(self.input_set_name == "custom set" and self.input_type == "n-tuple")
            self.output_tuple_n_label.setVisible(self.output_set_name == "custom set" and self.output_type == "n-tuple")
            self.output_tuple_n_lineEdit.setVisible(self.output_set_name == "custom set" and self.output_type == "n-tuple")
            self.output_tupleType_label.setVisible(self.output_set_name == "custom set" and self.output_type == "n-tuple")
            self.output_tupleType_button.setVisible(self.output_set_name == "custom set" and self.output_type == "n-tuple")
            self.input_mv_algebra_label.setVisible(self.input_set_name == "MV-algebra")
            self.input_mv_algebra_comboBox.setVisible(self.input_set_name == "MV-algebra")
            self.input_mv_algebra_k_label.setVisible(self.input_set_name == "MV-algebra")
            self.input_mv_algebra_k.setVisible(self.input_set_name == "MV-algebra")
            self.output_mv_algebra_label.setVisible(self.output_set_name == "MV-algebra")
            self.output_mv_algebra_comboBox.setVisible(self.output_set_name == "MV-algebra")
            self.output_mv_algebra_k_label.setVisible(self.output_set_name == "MV-algebra")
            self.output_mv_algebra_k.setVisible(self.output_set_name == "MV-algebra")
        except Exception as e:
            dumpException(e)

    def fixKValue(self, input, text):
        if "." in text:
            input.setText(text.replace(".", ""))

    def onMappingTypeChanged(self):
        self.mapping_type = self.mapping_type_comboBox.currentText()

    def onDeleteButtonClicked(self):
        self.mappingEdit.deleteCheckedMappings()

    def onAddButtonClicked(self):
        self.mappingEdit.addMapping()

    def onAddAllButtonClicked(self):
        if self.input_type == "string" or self.input_type == "number":
            input_set_list = sorted(self.input_set)
        elif self.input_type == "mapping":
            input_set_list = sorted(self.input_set, key=lambda mapping: mapping.name)
        elif self.input_type == "n-tuple":
            input_set_list = sorted(self.input_set)
        # elif self.input_type == "2-tuple":
        #     if self.input_tuple_types == "string" or self.input_tuple_types == "number" or self.input_tuple_types == "2-tuple":
        #         input_set_list = sorted(self.input_set)
        #     elif self.input_tuple_types == "mapping":
        #         input_set_list = sorted(self.input_set, key=lambda tup: tuple([tup[0].name, tup[1].name]))
        #     elif self.input_tuple_types == "set":
        #         input_set_list = sorted(self.input_set, key=lambda tup: tuple([sorted(tup[0]), sorted(tup[1])]))
        elif self.input_type == "set":
            if self.input_set_type == "string" or self.input_set_type == "number" or self.input_set_type == "n-tuple":
                input_set_list = sorted(self.input_set, key=lambda fst: sorted(fst))
                input_set_list = sorted(input_set_list, key=lambda fst: len(fst))
            elif self.input_set_type == "mapping":
                input_set_list = sorted(self.input_set, key=lambda fst: sorted([elem.name for elem in fst]))
                input_set_list = sorted(input_set_list, key=lambda fst: len(fst))
        else:
            input_set_list = self.input_set  # default case

        input_set_list_string = []
        for elem in input_set_list:
            if self.input_type == "set":
                input_set_list_string.append(str(set(elem)))
            elif self.input_type == "n-tuple" and self.input_tuple_types == "set":
                input_set_list_string.append(str(tuple([set(innerElem) for innerElem in elem])))
                # input_set_list_string.append(str(tuple([set(elem[0]), set(elem[1])])))
            else:
                input_set_list_string.append(str(elem))

        mappings = self.mappingEdit.getMappings()
        x_values = []
        for mapping in mappings:
            x_values.append(mapping[0])

        if x_values:
            missing_x_values = list(frozenset(input_set_list_string) - frozenset(x_values))
        else:
            missing_x_values = input_set_list_string

        for elem in missing_x_values:
            self.mappingEdit.addMapping(input_set_list[input_set_list_string.index(elem)])

    def moveScrollBarToBottom(self, min, max):
        self.scroll.verticalScrollBar().setValue(max)

    def getMappingNameElements(self):
        res = []
        for elem in self.list_of_elements:
            res.append((elem[0].name, elem[1].name))
        return res

    def onSave(self):
        try:
            if self.func_name != self.func.name and self.func_name in FPTMapping.dictOfFPTMappings.keys():
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThis mapping name is already used")
                msg.exec()
            elif self.func_name == "":
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nMapping name is empty")
                msg.exec()
            else:
                self.list_of_tuples = []
                self.list_of_elements = []
                self.list_of_values = []

                mappings = self.mappingEdit.getMappings()

                emptyMappings = False
                doubleElements = False
                wrongInput = False

                if self.input_set_name != "custom set" and self.input_set_name != "MV-algebra" and self.output_set_name != "custom set" and self.output_set_name != "MV-algebra":
                    input_set_list = self.input_set
                    input_set_list_string = []
                    for elem in input_set_list:
                        if self.input_type == "set":
                            input_set_list_string.append(str(set(elem)))
                        elif self.input_type == "n-tuple" and self.input_tuple_types == "set":
                            input_set_list_string.append(str(tuple([set(innerElem) for innerElem in elem])))
                            # input_set_list_string.append(str(tuple([set(elem[0]), set(elem[1])])))
                        else:
                            input_set_list_string.append(str(elem))

                    output_set_list = self.output_set
                    output_set_list_string = []
                    for elem in output_set_list:
                        if self.output_type == "set":
                            output_set_list_string.append(str(set(elem)))
                        elif self.output_type == "n-tuple" and self.output_tuple_types == "set":
                            output_set_list_string.append(str(tuple([set(innerElem) for innerElem in elem])))
                            # output_set_list_string.append(str(tuple([set(elem[0]), set(elem[1])])))
                        else:
                            output_set_list_string.append(str(elem))

                    mapping_indices = []
                    for mapping in mappings:
                        if mapping[0] != "" and mapping[1] != "":
                            mapping_indices.append(tuple([input_set_list_string.index(mapping[0]), output_set_list_string.index(mapping[1])]))
                        else:
                            emptyMappings = True

                    for mapping in mapping_indices:
                        if input_set_list[mapping[0]] not in self.list_of_elements:
                            self.list_of_tuples.append([input_set_list[mapping[0]], output_set_list[mapping[1]]])
                            self.list_of_elements.append(input_set_list[mapping[0]])
                            self.list_of_values.append(output_set_list[mapping[1]])
                        else:
                            doubleElements = True
                            break

                elif self.input_set_name != "custom set" and self.input_set_name != "MV-algebra":
                    input_set_list = self.input_set
                    input_set_list_string = []
                    for elem in input_set_list:
                        if self.input_type == "set":
                            input_set_list_string.append(str(set(elem)))
                        elif self.input_type == "n-tuple" and self.input_tuple_types == "set":
                            input_set_list_string.append(str(tuple([set(innerElem) for innerElem in elem])))
                            # input_set_list_string.append(str(tuple([set(elem[0]), set(elem[1])])))
                        else:
                            input_set_list_string.append(str(elem))

                    mapping_indices = []
                    for mapping in mappings:
                        if mapping[0] != "":
                            mapping_indices.append(tuple([input_set_list_string.index(mapping[0]), mapping[1]]))
                        else:
                            emptyMappings = True

                    try:
                        if self.output_type == "string":
                            for mapping in mapping_indices:
                                if mapping[1] != "":
                                    if input_set_list[mapping[0]] not in self.list_of_elements:
                                        self.list_of_tuples.append([input_set_list[mapping[0]], str(mapping[1])])
                                        self.list_of_elements.append(input_set_list[mapping[0]])
                                        self.list_of_values.append(str(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.output_type == "number":
                            for mapping in mapping_indices:
                                if mapping[1] != "":
                                    if input_set_list[mapping[0]] not in self.list_of_elements:
                                        self.list_of_tuples.append([input_set_list[mapping[0]], float(mapping[1])])
                                        self.list_of_elements.append(input_set_list[mapping[0]])
                                        self.list_of_values.append(float(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.output_type == "mapping":
                            for mapping in mapping_indices:
                                if mapping[1] != "":
                                    if input_set_list[mapping[0]] not in self.list_of_elements:
                                        self.list_of_tuples.append([input_set_list[mapping[0]], FPTMapping(mapping[1])])
                                        self.list_of_elements.append(input_set_list[mapping[0]])
                                        self.list_of_values.append(FPTMapping(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.output_type == "n-tuple":
                            for mapping in mapping_indices:
                                # if mapping[1] != ("", "") and mapping[1] != (("", ""), ("", "")) and mapping[1] != (None, None):
                                if mapping[1] != tuple(self.output_tuple_size*[""]) and mapping[1] != tuple(self.output_tuple_size*[None]):
                                    if input_set_list[mapping[0]] not in self.list_of_elements:
                                        self.list_of_tuples.append([input_set_list[mapping[0]], mapping[1]])
                                        self.list_of_elements.append(input_set_list[mapping[0]])
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.output_type == "set":
                            for mapping in mapping_indices:
                                if input_set_list[mapping[0]] not in self.list_of_elements:
                                    self.list_of_tuples.append([input_set_list[mapping[0]], mapping[1]])
                                    self.list_of_elements.append(input_set_list[mapping[0]])
                                    self.list_of_values.append(mapping[1])
                                else:
                                    doubleElements = True
                                    break
                    except ValueError:
                        wrongInput = True

                elif self.output_set_name != "custom set" and self.output_set_name != "MV-algebra":
                    output_set_list = self.output_set
                    output_set_list_string = []
                    for elem in output_set_list:
                        if self.output_type == "set":
                            output_set_list_string.append(str(set(elem)))
                        elif self.output_type == "n-tuple" and self.output_tuple_types == "set":
                            output_set_list_string.append(str(tuple([set(innerElem) for innerElem in elem])))
                            # output_set_list_string.append(str(tuple([set(elem[0]), set(elem[1])])))
                        else:
                            output_set_list_string.append(str(elem))

                    mapping_indices = []
                    for mapping in mappings:
                        if mapping[1] != "":
                            mapping_indices.append(tuple([mapping[0], output_set_list_string.index(mapping[1])]))
                        else:
                            emptyMappings = True

                    try:
                        if self.input_type == "string":
                            for mapping in mapping_indices:
                                if mapping[0] != "":
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), output_set_list[mapping[1]]])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(output_set_list[mapping[1]])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.input_type == "number":
                            for mapping in mapping_indices:
                                if mapping[0] != "":
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), output_set_list[mapping[1]]])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(output_set_list[mapping[1]])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        if self.input_type == "mapping":
                            for mapping in mapping_indices:
                                element_names = []
                                for element in self.list_of_elements:
                                    element_names.append(element.name)

                                func1 = FPTMapping(mapping[0])
                                if func1.name not in element_names:
                                    self.list_of_tuples.append([func1, output_set_list[mapping[1]]])
                                    self.list_of_elements.append(func1)
                                    self.list_of_values.append(output_set_list[mapping[1]])
                                else:
                                    doubleElements = True
                                    break
                        if self.input_type == "n-tuple":
                            for mapping in mapping_indices:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[0] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]):
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], output_set_list[mapping[1]]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(output_set_list[mapping[1]])
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], output_set_list[mapping[1]]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(output_set_list[mapping[1]])
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        if self.input_type == "set":
                            for mapping in mapping_indices:
                                if mapping[0] != frozenset():
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], output_set_list[mapping[1]]])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(output_set_list[mapping[1]])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                    except ValueError:
                        wrongInput = True

                else:
                    try:
                        if self.input_type == "string" and self.output_type == "string":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != "":
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), str(mapping[1])])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(str(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "string" and self.output_type == "number":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != "":
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), float(mapping[1])])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(float(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "number" and self.output_type == "string":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != "":
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), str(mapping[1])])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(str(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "number" and self.output_type == "number":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != "":
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), float(mapping[1])])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(float(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "string" and self.output_type == "mapping":
                            for mapping in mappings:
                                if mapping[0] != "":
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), FPTMapping(mapping[1])])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(FPTMapping(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "mapping" and self.output_type == "string":
                            for mapping in mappings:
                                if mapping[1] != "":
                                    element_names = []
                                    for element in self.list_of_elements:
                                        element_names.append(element.name)

                                    func = FPTMapping(mapping[0])
                                    if func.name not in element_names:
                                        self.list_of_tuples.append([func, str(mapping[1])])
                                        self.list_of_elements.append(func)
                                        self.list_of_values.append(str(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "number" and self.output_type == "mapping":
                            for mapping in mappings:
                                if mapping[0] != "":
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), FPTMapping(mapping[1])])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(FPTMapping(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "mapping" and self.output_type == "number":
                            for mapping in mappings:
                                if mapping[1] != "":
                                    element_names = []
                                    for element in self.list_of_elements:
                                        element_names.append(element.name)

                                    func = FPTMapping(mapping[0])
                                    if func.name not in element_names:
                                        self.list_of_tuples.append([func, float(mapping[1])])
                                        self.list_of_elements.append(func)
                                        self.list_of_values.append(float(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "mapping" and self.output_type == "mapping":
                            for mapping in mappings:
                                element_names = []
                                for element in self.list_of_elements:
                                    element_names.append(element.name)

                                func1 = FPTMapping(mapping[0])
                                func2 = FPTMapping(mapping[1])
                                if func1.name not in element_names:
                                    self.list_of_tuples.append([func1, func2])
                                    self.list_of_elements.append(func1)
                                    self.list_of_values.append(func2)
                                else:
                                    doubleElements = True
                                    break
                        elif self.input_type == "n-tuple" and self.output_type == "n-tuple":
                            for mapping in mappings:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[0] != (None, None) and mapping[1] != ("", "") and mapping[1] != (("", ""), ("", "")) and mapping[1] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]) and mapping[1] != tuple(self.output_tuple_size * [""]) and mapping[1] != tuple(self.output_tuple_size * [None]):
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], mapping[1]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(mapping[1])
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], mapping[1]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(mapping[1])
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "n-tuple" and self.output_type == "string":
                            for mapping in mappings:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[1] != "" and mapping[0] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]) and mapping[1] != "":
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], str(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(str(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], str(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(str(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "n-tuple" and self.output_type == "number":
                            for mapping in mappings:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[1] != "" and mapping[0] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]) and mapping[1] != "":
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], float(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(float(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], float(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(float(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "n-tuple" and self.output_type == "mapping":
                            for mapping in mappings:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[0] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]):
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], FPTMapping(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(FPTMapping(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], FPTMapping(mapping[1])])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(FPTMapping(mapping[1]))
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "n-tuple" and self.output_type == "set":
                            for mapping in mappings:
                                # if mapping[0] != ("", "") and mapping[0] != (("", ""), ("", "")) and mapping[0] != (frozenset(), frozenset()) and mapping[0] != (None, None):
                                if mapping[0] != tuple(self.input_tuple_size * [""]) and mapping[0] != tuple(self.input_tuple_size * [None]):
                                    if type(mapping[0][0]) == FPTMapping:
                                        list_of_mapping_name_elements = self.getMappingNameElements()
                                        if (mapping[0][0].name, mapping[0][1].name) not in list_of_mapping_name_elements:
                                            self.list_of_tuples.append([mapping[0], mapping[1]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(mapping[1])
                                        else:
                                            doubleElements = True
                                            break
                                    else:
                                        if mapping[0] not in self.list_of_elements:
                                            self.list_of_tuples.append([mapping[0], mapping[1]])
                                            self.list_of_elements.append(mapping[0])
                                            self.list_of_values.append(mapping[1])
                                        else:
                                            doubleElements = True
                                            break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "string" and self.output_type == "n-tuple":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != tuple(self.output_tuple_size * [""]) and mapping[1] != tuple(self.output_tuple_size * [None]):
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), mapping[1]])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "number" and self.output_type == "n-tuple":
                            for mapping in mappings:
                                if mapping[0] != "" and mapping[1] != tuple(self.output_tuple_size * [""]) and mapping[1] != tuple(self.output_tuple_size * [None]):
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), mapping[1]])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "mapping" and self.output_type == "n-tuple":
                            for mapping in mappings:
                                if mapping[1] != tuple(self.output_tuple_size * [""]) and mapping[1] != tuple(self.output_tuple_size * [None]):
                                    element_names = []
                                    for element in self.list_of_elements:
                                        element_names.append(element.name)

                                    func = FPTMapping(mapping[0])
                                    if func.name not in element_names:
                                        self.list_of_tuples.append([func, mapping[1]])
                                        self.list_of_elements.append(func)
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "set" and self.output_type == "n-tuple":
                            for mapping in mappings:
                                if mapping[0] != frozenset() and mapping[1] != tuple(self.output_tuple_size * [""]) and mapping[1] != tuple(self.output_tuple_size * [None]):
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], mapping[1]])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "set" and self.output_type == "string":
                            for mapping in mappings:
                                if mapping[0] != frozenset() and mapping[1] != "":
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], str(mapping[1])])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(str(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "set" and self.output_type == "number":
                            for mapping in mappings:
                                if mapping[0] != frozenset() and mapping[1] != "":
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], float(mapping[1])])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(float(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "set" and self.output_type == "mapping":
                            for mapping in mappings:
                                if mapping[0] != frozenset() and mapping[1] != "":
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], FPTMapping(mapping[1])])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(FPTMapping(mapping[1]))
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "set" and self.output_type == "set":
                            for mapping in mappings:
                                if mapping[0] != frozenset():
                                    if mapping[0] not in self.list_of_elements:
                                        self.list_of_tuples.append([mapping[0], mapping[1]])
                                        self.list_of_elements.append(mapping[0])
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "string" and self.output_type == "set":
                            for mapping in mappings:
                                if mapping[0] != "":
                                    if str(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([str(mapping[0]), mapping[1]])
                                        self.list_of_elements.append(str(mapping[0]))
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "number" and self.output_type == "set":
                            for mapping in mappings:
                                if mapping[0] != "":
                                    if float(mapping[0]) not in self.list_of_elements:
                                        self.list_of_tuples.append([float(mapping[0]), mapping[1]])
                                        self.list_of_elements.append(float(mapping[0]))
                                        self.list_of_values.append(mapping[1])
                                    else:
                                        doubleElements = True
                                        break
                                else:
                                    emptyMappings = True
                        elif self.input_type == "mapping" and self.output_type == "set":
                            for mapping in mappings:
                                element_names = []
                                for element in self.list_of_elements:
                                    element_names.append(element.name)

                                func = FPTMapping(mapping[0])
                                if func.name not in element_names:
                                    self.list_of_tuples.append([func, mapping[1]])
                                    self.list_of_elements.append(func)
                                    self.list_of_values.append(mapping[1])
                                else:
                                    doubleElements = True
                                    break
                    except ValueError:
                        wrongInput = True

                if DEBUG: print(self.list_of_tuples)
                if DEBUG: print(self.list_of_elements)
                if DEBUG: print(self.list_of_values)
                if DEBUG: print(emptyMappings)
                if DEBUG: print(doubleElements)
                if DEBUG: print(wrongInput)

                if wrongInput:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Warning:\nThere are inputs or outputs of a wrong type")
                    msg.exec()
                elif doubleElements:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Warning:\nThere are elements which map to multiple values")
                    msg.exec()
                elif emptyMappings:
                    msg = QMessageBox()
                    msg.setWindowTitle("Information")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information:\nEmpty mappings have been removed")
                    msg.exec()
                    self.accept()
                else:
                    self.accept()
        except Exception as e:
            dumpException(e)

    def onCancel(self):
        self.reject()
