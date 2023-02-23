from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_mapping import FPTMapping


class QDMRelationEdit(QWidget):
    def __init__(self, input_set, output_set, relation):
        super().__init__()

        input_list = list(input_set)
        output_list = list(output_set)
        self.rel = relation

        firstSetType = "string"
        firstInnerTupleType = "string"
        firstInnerSetType = "string"
        if len(input_list) > 0:
            if type(input_list[0]) == str:
                firstSetType = "string"
            elif type(input_list[0]) == int or type(input_list[0]) == float:
                firstSetType = "number"
            elif type(input_list[0]) == tuple:
                firstSetType = "n-tuple"
                # for elem in input_list:
                #     if type(elem[0]) == str:
                #         firstInnerTupleType = "string"
                #     elif type(elem[0]) == int or type(elem[0]) == float:
                #         firstInnerTupleType = "number"
                #     elif type(elem[0]) == frozenset or type(elem[0]) == set:
                #         firstInnerTupleType = "set"
                #     elif type(elem[0]) == tuple:
                #         firstInnerTupleType = "2-tuple"
                #     elif type(elem[0]) == FPTMapping:
                #         firstInnerTupleType = "mapping"
                #     break
            elif type(input_list[0]) == frozenset or type(input_list[0]) == set:
                firstSetType = "set"
                for elem in input_list:
                    if len(elem) > 0:
                        for innerElem in elem:
                            if type(innerElem) == str:
                                firstInnerSetType = "string"
                            elif type(innerElem) == int or type(innerElem) == float:
                                firstInnerSetType = "number"
                            elif type(innerElem) == frozenset or type(innerElem) == set:
                                firstInnerSetType = "set"
                            elif type(innerElem) == tuple:
                                firstInnerSetType = "n-tuple"
                            elif type(innerElem) == FPTMapping:
                                firstInnerSetType = "mapping"
                            break
                        break
            elif type(input_list[0]) == FPTMapping:
                firstSetType = "mapping"

        try:
            if firstSetType == "string" or firstSetType == "number":
                self.input_list = sorted(input_list)
            elif firstSetType == "mapping":
                self.input_list = sorted(input_list, key=lambda mapping: mapping.name)
            # elif firstSetType == "2-tuple":
            #     if firstInnerTupleType == "string" or firstInnerTupleType == "number" or firstInnerTupleType == "2-tuple":
            #         self.input_list = sorted(input_list)
            #     elif firstInnerTupleType == "mapping":
            #         self.input_list = sorted(input_list, key=lambda tup: tuple([tup[0].name, tup[1].name]))
            #     elif firstInnerTupleType == "set":
            #         self.input_list = sorted(input_list, key=lambda tup: tuple([sorted(tup[0]), sorted(tup[1])]))
            elif firstSetType == "set":
                if firstInnerSetType == "string" or firstInnerSetType == "number" or firstInnerSetType == "n-tuple":
                    self.input_list = sorted(input_list, key=lambda fst: sorted(fst))
                    self.input_list = sorted(self.input_list, key=lambda fst: len(fst))
                elif firstInnerSetType == "mapping":
                    self.input_list = sorted(input_list, key=lambda fst: sorted([elem.name for elem in fst]))
                    self.input_list = sorted(self.input_list, key=lambda fst: len(fst))
            else:
                self.input_list = sorted(input_list)  # default case
        except TypeError:
            self.input_list = input_list
            print("INFO: Could not sort various types")

        secondSetType = "string"
        secondInnerTupleType = "string"
        secondInnerSetType = "string"
        if len(output_list) > 0:
            if type(output_list[0]) == str:
                secondSetType = "string"
            elif type(output_list[0]) == int or type(output_list[0]) == float:
                secondSetType = "number"
            elif type(output_list[0]) == tuple:
                secondSetType = "n-tuple"
                # for elem in output_list:
                #     if type(elem[0]) == str:
                #         secondInnerTupleType = "string"
                #     elif type(elem[0]) == int or type(elem[0]) == float:
                #         secondInnerTupleType = "number"
                #     elif type(elem[0]) == frozenset or type(elem[0]) == set:
                #         secondInnerTupleType = "set"
                #     elif type(elem[0]) == tuple:
                #         secondInnerTupleType = "2-tuple"
                #     elif type(elem[0]) == FPTMapping:
                #         secondInnerTupleType = "mapping"
                #     break
            elif type(output_list[0]) == frozenset or type(output_list[0]) == set:
                secondSetType = "set"
                for elem in output_list:
                    if len(elem) > 0:
                        for innerElem in elem:
                            if type(innerElem) == str:
                                secondInnerSetType = "string"
                            elif type(innerElem) == int or type(innerElem) == float:
                                secondInnerSetType = "number"
                            elif type(innerElem) == frozenset or type(innerElem) == set:
                                secondInnerSetType = "set"
                            elif type(innerElem) == tuple:
                                secondInnerSetType = "n-tuple"
                            elif type(innerElem) == FPTMapping:
                                secondInnerSetType = "mapping"
                            break
                        break
            elif type(output_list[0]) == FPTMapping:
                secondSetType = "mapping"

        try:
            if secondSetType == "string" or secondSetType == "number":
                self.output_list = sorted(output_list)
            elif secondSetType == "mapping":
                self.output_list = sorted(output_list, key=lambda mapping: mapping.name)
            # elif secondSetType == "2-tuple":
            #     if secondInnerTupleType == "string" or secondInnerTupleType == "number" or secondInnerTupleType == "2-tuple":
            #         self.output_list = sorted(output_list)
            #     elif secondInnerTupleType == "mapping":
            #         self.output_list = sorted(output_list, key=lambda tup: tuple([tup[0].name, tup[1].name]))
            #     elif secondInnerTupleType == "set":
            #         self.output_list = sorted(output_list, key=lambda tup: tuple([sorted(tup[0]), sorted(tup[1])]))
            elif secondSetType == "set":
                if secondInnerSetType == "string" or secondInnerSetType == "number" or secondInnerSetType == "n-tuple":
                    self.output_list = sorted(output_list, key=lambda fst: sorted(fst))
                    self.output_list = sorted(self.output_list, key=lambda fst: len(fst))
                elif secondInnerSetType == "mapping":
                    self.output_list = sorted(output_list, key=lambda fst: sorted([elem.name for elem in fst]))
                    self.output_list = sorted(self.output_list, key=lambda fst: len(fst))
            else:
                self.output_list = output_list  # default case
        except TypeError:
            self.output_list = output_list
            print("INFO: Could not sort various types")

        self.mappingNameRelation = []
        for elem in self.rel.relation:
            if type(elem[0]) == FPTMapping and type(elem[1]) == FPTMapping:
                self.mappingNameRelation.append(tuple([elem[0].name, elem[1].name]))
            elif type(elem[0]) == FPTMapping:
                self.mappingNameRelation.append(tuple([elem[0].name, elem[1]]))
            elif type(elem[1]) == FPTMapping:
                self.mappingNameRelation.append(tuple([elem[0], elem[1].name]))
            else:
                break
        self.mappingNameRelation = frozenset(self.mappingNameRelation)

        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()

        i = 1
        for elem in self.input_list:
            if type(elem) == set or type(elem) == frozenset:
                isSetOfFunctions = False
                for innerElem in elem:
                    isSetOfFunctions = type(innerElem) == FPTMapping
                    break

                if isSetOfFunctions:
                    newStr = "{"
                    for innerElem in sorted(elem, key=lambda mapping: mapping.name):
                        newStr += innerElem.name + ", "
                    if len(newStr) > 1:
                        newStr = newStr[:-2] + "}"
                    else:
                        newStr = "{}"
                else:
                    newStr = "{"
                    for innerElem in elem:
                        newStr += str(innerElem) + ", "
                    if len(elem) > 0:
                        newStr = newStr[:-2] + "}"
                    else:
                        newStr += "}"
            elif type(elem) == tuple:
                newStr = "("

                for tupElem in elem:
                    if type(tupElem) == set or type(tupElem) == frozenset:
                        innerStr = "{"
                        for innerElem in tupElem:
                            innerStr += str(innerElem) + ", "
                        if len(innerStr) > 1:
                            innerStr = innerStr[:-2] + "}"
                        else:
                            innerStr = "{}"
                    else:
                        innerStr = str(tupElem)

                    newStr += innerStr + ", "

                newStr = newStr[:-2] + ")"

                # if type(elem[0]) == set or type(elem[0]) == frozenset:
                #     newStr = "("
                #
                #     for innerElem in elem:
                #         newInnerStr = "{"
                #         for innerInnerElem in innerElem:
                #             newInnerStr += str(innerInnerElem) + ", "
                #         if len(newInnerStr) > 1:
                #             newInnerStr = newInnerStr[:-2] + "}"
                #         else:
                #             newInnerStr = "{}"
                #
                #         newStr += newInnerStr + ", "
                #
                #     if len(newStr) > 1:
                #         newStr = newStr[:-2] + ")"
                #     else:
                #         newStr = "()"
                #
                #     # newStr1 = "{"
                #     # for innerElem in elem[0]:
                #     #     newStr1 += str(innerElem) + ", "
                #     # if len(newStr1) > 1:
                #     #     newStr1 = newStr1[:-2] + "}"
                #     # else:
                #     #     newStr1 = "{}"
                #     #
                #     # newStr2 = "{"
                #     # for innerElem in elem[1]:
                #     #     newStr2 += str(innerElem) + ", "
                #     # if len(newStr2) > 1:
                #     #     newStr2 = newStr2[:-2] + "}"
                #     # else:
                #     #     newStr2 = "{}"
                #     #
                #     # newStr = "(" + newStr1 + ", " + newStr2 + ")"
                # else:
                #     newStr = str(elem)
            elif type(elem) == FPTMapping:
                newStr = elem.name
            else:
                newStr = str(elem)

            label = QLabel(newStr)
            label.setFont(QFont("Arial", 10))
            label.setStyleSheet("background-color: #5a5a5a")
            self.grid_layout.addWidget(label, i, 0)
            i += 1

        j = 1
        for elem in self.output_list:
            if type(elem) == set or type(elem) == frozenset:
                isSetOfFunctions = False
                for innerElem in elem:
                    isSetOfFunctions = type(innerElem) == FPTMapping
                    break

                if isSetOfFunctions:
                    newStr = "{"
                    for innerElem in sorted(elem, key=lambda mapping: mapping.name):
                        newStr += innerElem.name + ", "
                    if len(newStr) > 1:
                        newStr = newStr[:-2] + "}"
                    else:
                        newStr = "{}"
                else:
                    newStr = "{"
                    for innerElem in elem:
                        newStr += str(innerElem) + ", "
                    if len(elem) > 0:
                        newStr = newStr[:-2] + "}"
                    else:
                        newStr += "}"
            elif type(elem) == tuple:
                newStr = "("

                for tupElem in elem:
                    if type(tupElem) == set or type(tupElem) == frozenset:
                        innerStr = "{"
                        for innerElem in tupElem:
                            innerStr += str(innerElem) + ", "
                        if len(innerStr) > 1:
                            innerStr = innerStr[:-2] + "}"
                        else:
                            innerStr = "{}"
                    else:
                        innerStr = str(tupElem)

                    newStr += innerStr + ", "

                newStr = newStr[:-2] + ")"

                # if type(elem[0]) == set or type(elem[0]) == frozenset:
                #     newStr = "("
                #
                #     for innerElem in elem:
                #         newInnerStr = "{"
                #         for innerInnerElem in innerElem:
                #             newInnerStr += str(innerInnerElem) + ", "
                #         if len(newInnerStr) > 1:
                #             newInnerStr = newInnerStr[:-2] + "}"
                #         else:
                #             newInnerStr = "{}"
                #
                #         newStr += newInnerStr + ", "
                #
                #     if len(newStr) > 1:
                #         newStr = newStr[:-2] + ")"
                #     else:
                #         newStr = "()"
                #
                #     # newStr1 = "{"
                #     # for innerElem in elem[0]:
                #     #     newStr1 += str(innerElem) + ", "
                #     # if len(newStr1) > 1:
                #     #     newStr1 = newStr1[:-2] + "}"
                #     # else:
                #     #     newStr1 = "{}"
                #     #
                #     # newStr2 = "{"
                #     # for innerElem in elem[1]:
                #     #     newStr2 += str(innerElem) + ", "
                #     # if len(newStr2) > 1:
                #     #     newStr2 = newStr2[:-2] + "}"
                #     # else:
                #     #     newStr2 = "{}"
                #     #
                #     # newStr = "(" + newStr1 + ", " + newStr2 + ")"
                # else:
                #     newStr = str(elem)
            elif type(elem) == FPTMapping:
                newStr = elem.name
            else:
                newStr = str(elem)

            label = QLabel(newStr)
            label.setFont(QFont("Arial", 10))
            label.setStyleSheet("background-color: #5a5a5a")
            self.grid_layout.addWidget(label, 0, j, alignment=Qt.AlignCenter)
            j += 1

        if self.rel.type == "custom":
            self.createCheckboxes()

        # if True:  # old: self.rel.type == "custom"
        #     for i in range(1, len(self.input_list)+1):
        #         for j in range(1, len(self.output_list)+1):
        #             checkBox = QCheckBox()
        #             checkBox.setStyleSheet("background-color: #FFFFFF; spacing: 0px")
        #
        #             if type(self.input_list[i-1]) == FPTMapping and type(self.output_list[j - 1]) == FPTMapping:
        #                 checkBox.setChecked(tuple([self.input_list[i-1].name, self.output_list[j-1].name]) in self.mappingNameRelation)
        #             elif type(self.input_list[i-1]) == FPTMapping:
        #                 checkBox.setChecked(tuple([self.input_list[i-1].name, self.output_list[j-1]]) in self.mappingNameRelation)
        #             elif type(self.output_list[j-1]) == FPTMapping:
        #                 checkBox.setChecked(tuple([self.input_list[i-1], self.output_list[j-1].name]) in self.mappingNameRelation)
        #             else:
        #                 checkBox.setChecked(tuple([self.input_list[i-1], self.output_list[j-1]]) in self.rel.relation)
        #
        #             self.grid_layout.addWidget(checkBox, i, j, alignment=Qt.AlignCenter)

        self.setLayout(self.grid_layout)

    def createCheckboxes(self):
        for i in range(1, len(self.input_list) + 1):
            for j in range(1, len(self.output_list) + 1):
                checkBox = QCheckBox()
                checkBox.setStyleSheet("background-color: #FFFFFF; spacing: 0px")

                if type(self.input_list[i - 1]) == FPTMapping and type(self.output_list[j - 1]) == FPTMapping:
                    checkBox.setChecked(
                        tuple([self.input_list[i - 1].name, self.output_list[j - 1].name]) in self.mappingNameRelation)
                elif type(self.input_list[i - 1]) == FPTMapping:
                    checkBox.setChecked(
                        tuple([self.input_list[i - 1].name, self.output_list[j - 1]]) in self.mappingNameRelation)
                elif type(self.output_list[j - 1]) == FPTMapping:
                    checkBox.setChecked(
                        tuple([self.input_list[i - 1], self.output_list[j - 1].name]) in self.mappingNameRelation)
                else:
                    checkBox.setChecked(tuple([self.input_list[i - 1], self.output_list[j - 1]]) in self.rel.relation)

                self.grid_layout.addWidget(checkBox, i, j, alignment=Qt.AlignCenter)

    def getRelation(self):
        newRelation = []
        for i in range(1, len(self.input_list) + 1):
            for j in range(1, len(self.output_list) + 1):
                if self.grid_layout.itemAtPosition(i, j).widget().isChecked():
                    newRelation.append(tuple([self.input_list[i-1], self.output_list[j-1]]))

        return set(newRelation)