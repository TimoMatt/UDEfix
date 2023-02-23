from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import chain, combinations

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_relationEdit import QDMRelationEdit
from fixpointtool.content.fpt_relation import FPTRelation
from nodeeditor.utils import dumpException


class QDMContentListWidgetRelationPopup(QDialog):

    def __init__(self, relation, parent=None):
        super().__init__(parent)

        self.accessDicts = AccessDictionaries()
        self.relation = relation
        self.relation_type = self.relation.type

        self.sets_content = self.accessDicts.getDictionaryWithoutTransformation("sets")

        self.setWindowTitle("Edit relation")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(302, 503)
        self.setMinimumSize(302, 503)

        self.name_label = QLabel("Name:")
        self.type_label = QLabel("Type:")
        self.content_label = QLabel("Content:")

        self.relation_type_comboBox = QComboBox()
        self.relation_type_comboBox.addItems(FPTRelation.LIST_OF_RELATION_TYPES)
        self.relation_type_comboBox.setCurrentText(self.relation_type)
        self.relation_type_comboBox.currentIndexChanged.connect(self.onTypeChanged)

        self.input_set_label = QLabel("First set")
        self.output_set_label = QLabel("Second set")

        # self.subset_type_label = QLabel("Is-element-of type")
        # self.subset_set_label = QLabel("Set")
        self.first_subset_set_label = QLabel("First Set")
        self.second_subset_set_label = QLabel("Second Set")

        self.u_projection_type_label = QLabel("Projection type")
        # self.u_set_label = QLabel("Set")
        self.first_u_set_label = QLabel("First Set")
        self.second_u_set_label = QLabel("Second Set")

        self.input_set_comboBox = QComboBox()
        self.output_set_comboBox = QComboBox()

        # self.subset_type_comboBox = QComboBox()
        # self.subset_set_comboBox = QComboBox()
        self.first_subset_set_comboBox = QComboBox()
        self.second_subset_set_comboBox = QComboBox()

        self.u_projection_type_comboBox = QComboBox()
        # self.u_set_comboBox = QComboBox()
        self.first_u_set_comboBox = QComboBox()
        self.second_u_set_comboBox = QComboBox()

        self.input_set_comboBox.setMaximumWidth(137)
        self.output_set_comboBox.setMaximumWidth(137)

        # self.subset_type_comboBox.setMaximumWidth(137)
        # self.subset_set_comboBox.setMaximumWidth(137)
        self.first_subset_set_comboBox.setMaximumWidth(137)
        self.second_subset_set_comboBox.setMaximumWidth(137)

        self.u_projection_type_comboBox.setMaximumWidth(137)
        # self.u_set_comboBox.setMaximumWidth(137)
        self.first_u_set_comboBox.setMaximumWidth(137)
        self.second_u_set_comboBox.setMaximumWidth(137)

        self.input_set_label.setMargin(4)
        self.output_set_label.setMargin(4)

        # self.subset_type_label.setMargin(4)
        # self.subset_set_label.setMargin(4)
        self.first_subset_set_label.setMargin(4)
        self.second_subset_set_label.setMargin(4)

        self.u_projection_type_label.setMargin(4)
        # self.u_set_label.setMargin(4)
        self.first_u_set_label.setMargin(4)
        self.second_u_set_label.setMargin(4)

        self.input_set_comboBox.addItems(self.sets_content.keys())
        self.input_set_comboBox.setCurrentText(self.relation.input_set_name)
        self.input_set_comboBox.currentIndexChanged.connect(self.onSetsChanged)
        self.output_set_comboBox.addItems(self.sets_content.keys())
        self.output_set_comboBox.setCurrentText(self.relation.output_set_name)
        self.output_set_comboBox.currentIndexChanged.connect(self.onSetsChanged)

        # self.subset_type_comboBox.addItems(FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES.values())
        # self.subset_type_comboBox.setCurrentText(FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES[self.relation.is_element_of_type])
        # self.subset_type_comboBox.currentIndexChanged.connect(self.onIsElementOfTypeChanged)

        # subset_set_comboBox_keys = ["-"]
        # for key in self.sets_content.keys():
        #     tempSet = self.sets_content[key]
        #     if tempSet is not None:
        #         for elem in tempSet:
        #             if type(elem) == str or type(elem) == float or type(elem) == int or type(elem) == FPTMapping:
        #                 subset_set_comboBox_keys.append(key)
        #             elif type(elem) == tuple:
        #                 if type(elem[0]) == str or type(elem[0]) == float or type(elem[0]) == int:
        #                     subset_set_comboBox_keys.append(key)
        #             # elif type(elem) == set or type(elem) == frozenset:
        #             #     for innerElem in elem:
        #             #         if type(innerElem) == str or type(innerElem) == float or type(innerElem) == int:
        #             #             subset_set_comboBox_keys.append(key)
        #             #             break
        #             #         break
        #             break

        self.set_of_sets_comboBox_keys = ["-"]
        self.set_of_tuples_comboBox_keys = ["-"]
        self.set_of_tupleOfSets_comboBox_keys = ["-"]
        for key in self.sets_content.keys():
            tempSet = self.sets_content[key]
            if tempSet is not None:
                for elem in tempSet:
                    if type(elem) == set or type(elem) == frozenset:
                        self.set_of_sets_comboBox_keys.append(key)
                        break
                    elif type(elem) == tuple:
                        self.set_of_tuples_comboBox_keys.append(key)
                        if type(elem[0]) == set or type(elem[0]) == frozenset:
                            self.set_of_tupleOfSets_comboBox_keys.append(key)
                        break
                    break

        self.set_of_setsOfTuples_comboBox_keys = ["-"]
        for key in self.sets_content.keys():
            tempSet = self.sets_content[key]
            if tempSet is not None:
                for elem in tempSet:
                    done = False
                    if type(elem) == set or type(elem) == frozenset:
                        for innerElem in elem:
                            if type(innerElem) == tuple:
                                self.set_of_setsOfTuples_comboBox_keys.append(key)
                                done = True
                                break
                            done = True
                            break
                    if done: break


        # self.subset_set_comboBox.addItems(subset_set_comboBox_keys)
        self.first_subset_set_comboBox.addItems(self.sets_content.keys())
        self.second_subset_set_comboBox.addItems(self.set_of_sets_comboBox_keys)

        # self.subset_set_comboBox.setCurrentText(self.relation.input_set_name)
        self.first_subset_set_comboBox.setCurrentText(self.relation.input_set_name)
        self.second_subset_set_comboBox.setCurrentText(self.relation.output_set_name)

        # self.subset_set_comboBox.currentIndexChanged.connect(self.onSubsetSetChanged)
        self.first_subset_set_comboBox.currentIndexChanged.connect(self.onSubsetSetsChanged)
        self.second_subset_set_comboBox.currentIndexChanged.connect(self.onSubsetSetsChanged)

        if self.relation.projection_type == 0 or self.relation.projection_type == 1:
            self.first_u_set_comboBox.addItems(self.set_of_tuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.sets_content.keys())
        elif self.relation.projection_type == 2:
            self.first_u_set_comboBox.addItems(self.set_of_setsOfTuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.set_of_tupleOfSets_comboBox_keys)
        elif self.relation.projection_type == 3 or self.relation.projection_type == 4:
            self.first_u_set_comboBox.addItems(self.set_of_setsOfTuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.set_of_sets_comboBox_keys)
        else:
            print("WARNING: Not existing projection type")

        self.first_u_set_comboBox.setCurrentText(self.relation.input_set_name)
        self.second_u_set_comboBox.setCurrentText(self.relation.output_set_name)
        self.first_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)
        self.second_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)

        self.u_projection_type_comboBox.addItems(FPTRelation.DICT_OF_PROJECTION_TYPES.values())
        self.u_projection_type_comboBox.setCurrentText(FPTRelation.DICT_OF_PROJECTION_TYPES[self.relation.projection_type])
        self.u_projection_type_comboBox.currentIndexChanged.connect(self.onProjectionTypeChanged)

        # u_set_comboBox_keys = ["-"]
        # if self.relation.projection_type == 0 or self.relation.projection_type == 1:
        #     for key in self.sets_content.keys():
        #         tempSet = self.sets_content[key]
        #         if tempSet is not None:
        #             for elem in tempSet:
        #                 if type(elem) == tuple:
        #                     u_set_comboBox_keys.append(key)
        #                 break
        # elif self.relation.projection_type == 2:
        #     for key in self.sets_content.keys():
        #         tempSet = self.sets_content[key]
        #         if tempSet is not None:
        #             for elem in tempSet:
        #                 if type(elem) == tuple:
        #                     if type(elem[0]) == str or type(elem[0]) == int or type(elem[0]) == float or type(elem[0]) == FPTMapping:
        #                         u_set_comboBox_keys.append(key)
        #                 break
        # elif self.relation.projection_type == 3 or self.relation.projection_type == 4:
        #     for key in self.sets_content.keys():
        #         tempSet = self.sets_content[key]
        #         if tempSet is not None:
        #             for elem in tempSet:
        #                 if type(elem) == tuple:
        #                     if type(elem[0]) == str or type(elem[0]) == int or type(elem[0]) == float or type(elem[0]) == FPTMapping or type(elem[0]) == tuple:
        #                         u_set_comboBox_keys.append(key)
        #                 break
        # else:
        #     print("WARNING: projection type does not exist")

        # self.u_set_comboBox.addItems(u_set_comboBox_keys)
        # self.u_set_comboBox.setCurrentText(self.relation.input_set_name)
        # self.u_set_comboBox.currentIndexChanged.connect(self.onUSetChanged)

        self.input_set_hbox = QHBoxLayout()
        self.input_set_hbox.addWidget(self.input_set_label)
        self.input_set_hbox.addWidget(self.input_set_comboBox)

        self.output_set_hbox = QHBoxLayout()
        self.output_set_hbox.addWidget(self.output_set_label)
        self.output_set_hbox.addWidget(self.output_set_comboBox)

        # self.subset_type_hbox = QHBoxLayout()
        # self.subset_type_hbox.addWidget(self.subset_type_label)
        # self.subset_type_hbox.addWidget(self.subset_type_comboBox)

        # self.subset_set_hbox = QHBoxLayout()
        # self.subset_set_hbox.addWidget(self.subset_set_label)
        # self.subset_set_hbox.addWidget(self.subset_set_comboBox)

        self.first_subset_set_hbox = QHBoxLayout()
        self.first_subset_set_hbox.addWidget(self.first_subset_set_label)
        self.first_subset_set_hbox.addWidget(self.first_subset_set_comboBox)

        self.second_subset_set_hbox = QHBoxLayout()
        self.second_subset_set_hbox.addWidget(self.second_subset_set_label)
        self.second_subset_set_hbox.addWidget(self.second_subset_set_comboBox)

        self.u_projection_type_hbox = QHBoxLayout()
        self.u_projection_type_hbox.addWidget(self.u_projection_type_label)
        self.u_projection_type_hbox.addWidget(self.u_projection_type_comboBox)

        # self.u_set_hbox = QHBoxLayout()
        # self.u_set_hbox.addWidget(self.u_set_label)
        # self.u_set_hbox.addWidget(self.u_set_comboBox)

        self.first_u_set_hbox = QHBoxLayout()
        self.first_u_set_hbox.addWidget(self.first_u_set_label)
        self.first_u_set_hbox.addWidget(self.first_u_set_comboBox)

        self.second_u_set_hbox = QHBoxLayout()
        self.second_u_set_hbox.addWidget(self.second_u_set_label)
        self.second_u_set_hbox.addWidget(self.second_u_set_comboBox)

        self.name_textEdit = QTextEdit(self.relation.name)
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

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(280, 200)
        self.scroll.setStyleSheet("background-color: #5a5a5a")

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.cancel_button)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.name_label)
        self.vbox.addWidget(self.name_textEdit)
        self.vbox.addWidget(self.type_label)
        self.vbox.addWidget(self.relation_type_comboBox)
        self.vbox.addLayout(self.input_set_hbox)
        self.vbox.addLayout(self.output_set_hbox)
        # self.vbox.addLayout(self.subset_type_hbox)
        # self.vbox.addLayout(self.subset_set_hbox)
        self.vbox.addLayout(self.first_subset_set_hbox)
        self.vbox.addLayout(self.second_subset_set_hbox)
        self.vbox.addLayout(self.u_projection_type_hbox)
        # self.vbox.addLayout(self.u_set_hbox)
        self.vbox.addLayout(self.first_u_set_hbox)
        self.vbox.addLayout(self.second_u_set_hbox)
        self.vbox.addWidget(self.content_label)
        self.vbox.addWidget(self.scroll)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.input_set_label.setVisible(self.relation_type == "custom")
        self.input_set_comboBox.setVisible(self.relation_type == "custom")
        self.output_set_label.setVisible(self.relation_type == "custom")
        self.output_set_comboBox.setVisible(self.relation_type == "custom")
        # self.subset_type_label.setVisible(self.relation_type == "is-element-of")
        # self.subset_type_comboBox.setVisible(self.relation_type == "is-element-of")
        # self.subset_set_label.setVisible(self.relation_type == "is-element-of" and self.relation.is_element_of_type == 1)
        # self.subset_set_comboBox.setVisible(self.relation_type == "is-element-of" and self.relation.is_element_of_type == 1)
        self.first_subset_set_label.setVisible(self.relation_type == "is-element-of")
        self.first_subset_set_comboBox.setVisible(self.relation_type == "is-element-of")
        self.second_subset_set_label.setVisible(self.relation_type == "is-element-of")
        self.second_subset_set_comboBox.setVisible(self.relation_type == "is-element-of")
        self.u_projection_type_label.setVisible(self.relation_type == "projection")
        self.u_projection_type_comboBox.setVisible(self.relation_type == "projection")
        # self.u_set_label.setVisible(self.relation_type == "projection")
        # self.u_set_comboBox.setVisible(self.relation_type == "projection")
        self.first_u_set_label.setVisible(self.relation_type == "projection")
        self.first_u_set_comboBox.setVisible(self.relation_type == "projection")
        self.second_u_set_label.setVisible(self.relation_type == "projection")
        self.second_u_set_comboBox.setVisible(self.relation_type == "projection")

        self.input_set = set()
        self.output_set = set()

        if self.relation.input_set_name is not None and self.relation.output_set_name is not None:
            self.input_set = self.sets_content[self.relation.input_set_name]
            self.output_set = self.sets_content[self.relation.output_set_name]
        else:
            if self.input_set_comboBox.count() > 0:
                self.input_set = self.sets_content[self.input_set_comboBox.currentText()]
                self.output_set = self.sets_content[self.output_set_comboBox.currentText()]
                self.relation = FPTRelation(self.relation.name, self.relation.relation,
                                            self.input_set_comboBox.currentText(),
                                            self.output_set_comboBox.currentText())

        # elif self.relation_type == "is-element-of":
        #     if self.relation.input_set_name is not None:
        #         self.input_set = self.sets_content[self.relation.input_set_name]
        #         listOfSet = list(self.input_set)
        #         temp = chain.from_iterable(combinations(listOfSet, r) for r in range(len(listOfSet) + 1))
        #         self.output_set = set(frozenset(i) for i in temp)
        # elif self.relation_type == "projection":
        #     if self.relation.input_set_name is not None:
        #
        #         if self.relation.projection_type == 0:
        #             self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
        #
        #             self.output_set = set()
        #             for tup in self.input_set:
        #                 self.output_set |= {tup[0]}
        #
        #         elif self.relation.projection_type == 1:
        #             self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
        #
        #             self.output_set = set()
        #             for tup in self.input_set:
        #                 self.output_set |= {tup[1]}
        #
        #         elif self.relation.projection_type == 2:
        #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
        #             self.input_set = pow_set
        #
        #             self.output_set = set()
        #             for tup_set in pow_set:
        #                 self.output_set |= {(frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set))}
        #
        #         elif self.relation.projection_type == 3:
        #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
        #             self.input_set = pow_set
        #
        #             self.output_set = set()
        #             for tup_set in pow_set:
        #                 self.output_set |= {frozenset(x for (x, y) in tup_set)}
        #
        #         elif self.relation.projection_type == 4:
        #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
        #             self.input_set = pow_set
        #
        #             self.output_set = set()
        #             for tup_set in pow_set:
        #                 self.output_set |= {frozenset(y for (x, y) in tup_set)}
        #
        #         else:
        #             print("WARNING: Projection type does not exist")
        #
        #     input = self.sets_content[self.u_set_comboBox.currentText()]
        #     powSet = self.power_set(input)
        #     crossSet = set((x, y) for x in input for y in input)
        #     self.input_set = self.power_set(crossSet)
        #     self.output_set = set((x, y) for x in powSet for y in powSet)

        self.showContentButton = QPushButton("Show Content")
        self.showContentButton.setDefault(False)
        self.showContentButton.setAutoDefault(False)
        self.showContentButton.setFixedSize(150, 25)
        self.showContentButton.clicked.connect(self.showContent)

        self.showContentVBox = QVBoxLayout()
        self.showContentVBox.addWidget(self.showContentButton, alignment=Qt.AlignHCenter)

        self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
        self.scroll.setWidget(self.relationEdit)
        self.scroll.setLayout(self.showContentVBox)

        self.relationEdit.setVisible(self.relation_type == "custom")
        self.showContentButton.setVisible(self.relation_type != "custom")

        if self.relation_type != "custom":
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def power_set(self, Y):
        s = list(Y)
        temp = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
        return set(frozenset(i) for i in temp)

    def u(self, C):
        return frozenset(x for (x, y) in C), frozenset(y for (x, y) in C)

    def onNameChanged(self):
        self.relation = FPTRelation(self.name_textEdit.toPlainText(), self.relation.relation,
                                    self.relation.input_set_name, self.relation.output_set_name,
                                    self.relation.type)

    def onTypeChanged(self):
        try:
            self.relation_type = self.relation_type_comboBox.currentText()

            self.input_set_label.setVisible(self.relation_type == "custom")
            self.input_set_comboBox.setVisible(self.relation_type == "custom")
            self.output_set_label.setVisible(self.relation_type == "custom")
            self.output_set_comboBox.setVisible(self.relation_type == "custom")
            # self.subset_set_label.setVisible(self.relation_type == "is-element-of")
            # self.subset_set_comboBox.setVisible(self.relation_type == "is-element-of")
            self.first_subset_set_label.setVisible(self.relation_type == "is-element-of")
            self.first_subset_set_comboBox.setVisible(self.relation_type == "is-element-of")
            self.second_subset_set_label.setVisible(self.relation_type == "is-element-of")
            self.second_subset_set_comboBox.setVisible(self.relation_type == "is-element-of")
            self.u_projection_type_label.setVisible(self.relation_type == "projection")
            self.u_projection_type_comboBox.setVisible(self.relation_type == "projection")
            # self.u_set_label.setVisible(self.relation_type == "projection")
            # self.u_set_comboBox.setVisible(self.relation_type == "projection")
            self.first_u_set_label.setVisible(self.relation_type == "projection")
            self.first_u_set_comboBox.setVisible(self.relation_type == "projection")
            self.second_u_set_label.setVisible(self.relation_type == "projection")
            self.second_u_set_comboBox.setVisible(self.relation_type == "projection")

            if self.relation_type != "custom":
                self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            self.input_set = set()
            self.output_set = set()
            if self.relation_type == "custom":
                if self.input_set_comboBox.count() > 0 and self.output_set_comboBox.count() > 0:
                    self.input_set_comboBox.currentIndexChanged.disconnect()
                    self.output_set_comboBox.currentIndexChanged.disconnect()

                    self.input_set_comboBox.setCurrentText("-")
                    self.output_set_comboBox.setCurrentText("-")
                    self.input_set = self.sets_content[self.input_set_comboBox.currentText()]
                    self.output_set = self.sets_content[self.output_set_comboBox.currentText()]
                    self.relation = FPTRelation(self.relation.name, frozenset(),
                                                self.input_set_comboBox.currentText(),
                                                self.output_set_comboBox.currentText())

                    self.input_set_comboBox.currentIndexChanged.connect(self.onSetsChanged)
                    self.output_set_comboBox.currentIndexChanged.connect(self.onSetsChanged)
                else:
                    print("WARNING: Set ComboBox is empty")
            elif self.relation_type == "is-element-of":
                if self.first_subset_set_comboBox.count() > 0 and self.second_subset_set_comboBox.count() > 0:
                    self.first_subset_set_comboBox.currentIndexChanged.disconnect()
                    self.second_subset_set_comboBox.currentIndexChanged.disconnect()

                    self.first_subset_set_comboBox.setCurrentText("-")
                    self.second_subset_set_comboBox.setCurrentText("-")
                    self.input_set = self.sets_content[self.first_subset_set_comboBox.currentText()]
                    self.output_set = self.sets_content[self.second_subset_set_comboBox.currentText()]

                    # listOfSet = list(self.input_set)
                    # temp = chain.from_iterable(combinations(listOfSet, r) for r in range(len(listOfSet) + 1))
                    # self.output_set = set(frozenset(i) for i in temp)

                    newRelation = []
                    for inputElem in self.input_set:
                        for outputElem in self.output_set:
                            if inputElem in outputElem:
                                newRelation += [(inputElem, outputElem)]

                    self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
                                                self.first_subset_set_comboBox.currentText(),
                                                self.second_subset_set_comboBox.currentText(),
                                                type="is-element-of")

                    self.first_subset_set_comboBox.currentIndexChanged.connect(self.onSubsetSetsChanged)
                    self.second_subset_set_comboBox.currentIndexChanged.connect(self.onSubsetSetsChanged)
                else:
                    print("WARNING: Set ComboBox is empty")
            elif self.relation_type == "projection":
                if self.first_u_set_comboBox.count() > 0 and self.second_u_set_comboBox.count() > 0:
                    self.first_u_set_comboBox.currentIndexChanged.disconnect()
                    self.second_u_set_comboBox.currentIndexChanged.disconnect()
                    self.u_projection_type_comboBox.currentIndexChanged.disconnect()

                    self.u_projection_type_comboBox.setCurrentText(FPTRelation.DICT_OF_PROJECTION_TYPES[0])
                    self.first_u_set_comboBox.setCurrentText("-")
                    self.second_u_set_comboBox.setCurrentText("-")

                    # u_set_comboBox_keys = ["-"]
                    # for key in self.sets_content.keys():
                    #     tempSet = self.sets_content[key]
                    #     if tempSet is not None:
                    #         for elem in tempSet:
                    #             if type(elem) == tuple:
                    #                 u_set_comboBox_keys.append(key)
                    #             break

                    # self.u_set_comboBox.currentIndexChanged.disconnect()
                    # self.u_set_comboBox.clear()
                    # self.u_set_comboBox.addItems(u_set_comboBox_keys)
                    # self.u_set_comboBox.currentIndexChanged.connect(self.onUSetChanged)

                    self.input_set = self.sets_content[self.first_u_set_comboBox.currentText()]
                    self.output_set = self.sets_content[self.second_u_set_comboBox.currentText()]

                    newRelation = []
                    for inputElem in self.input_set:
                        for outputElem in self.output_set:
                            if inputElem[0] == outputElem:
                                newRelation += [(inputElem, outputElem)]

                    self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
                                                self.first_u_set_comboBox.currentText(),
                                                self.second_u_set_comboBox.currentText(),
                                                type="projection", projection_type=0)

                    self.first_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)
                    self.second_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)
                    self.u_projection_type_comboBox.currentIndexChanged.connect(self.onProjectionTypeChanged)
                else:
                    print("WARNING: Set ComboBox is empty")

            self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
            self.scroll.setWidget(self.relationEdit)

            self.relationEdit.setVisible(self.relation_type == "custom")
            self.showContentButton.setVisible(self.relation_type != "custom")
        except Exception as e:
            print(e)

    def onSetsChanged(self):
        try:
            self.input_set = self.sets_content[self.input_set_comboBox.currentText()]
            self.output_set = self.sets_content[self.output_set_comboBox.currentText()]

            self.relation = FPTRelation(self.relation.name, frozenset(), self.input_set_comboBox.currentText(), self.output_set_comboBox.currentText())

            self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
            self.scroll.setWidget(self.relationEdit)

            self.relationEdit.setVisible(self.relation_type == "custom")
            self.showContentButton.setVisible(self.relation_type != "custom")
        except Exception as e:
            dumpException(e)

    # def onSubsetSetChanged(self):
    #     self.input_set = self.sets_content[self.subset_set_comboBox.currentText()]
    #     listOfSet = list(self.input_set)
    #     temp = chain.from_iterable(combinations(listOfSet, r) for r in range(len(listOfSet) + 1))
    #     self.output_set = set(frozenset(i) for i in temp)
    #
    #     newRelation = []
    #     for elem in self.input_set:
    #         for innerElem in self.output_set:
    #             if elem in innerElem:
    #                 newRelation += [(elem, innerElem)]
    #
    #     self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
    #                                 self.subset_set_comboBox.currentText(),
    #                                 type="is-element-of")
    #
    #     self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
    #     self.scroll.setWidget(self.relationEdit)

    def onSubsetSetsChanged(self):
        self.input_set = self.sets_content[self.first_subset_set_comboBox.currentText()]
        self.output_set = self.sets_content[self.second_subset_set_comboBox.currentText()]

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        newRelation = []
        for inputElem in self.input_set:
            for outputElem in self.output_set:
                if inputElem in outputElem:
                    newRelation += [(inputElem, outputElem)]

        self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
                                    self.first_subset_set_comboBox.currentText(),
                                    self.second_subset_set_comboBox.currentText(),
                                    type="is-element-of")

        self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
        self.scroll.setWidget(self.relationEdit)

        self.relationEdit.setVisible(self.relation_type == "custom")
        self.showContentButton.setVisible(self.relation_type != "custom")

    def onUSetsChanged(self):
        self.input_set = self.sets_content[self.first_u_set_comboBox.currentText()]
        self.output_set = self.sets_content[self.second_u_set_comboBox.currentText()]
        projection_type = list(FPTRelation.DICT_OF_PROJECTION_TYPES.values()).index(self.u_projection_type_comboBox.currentText())

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if projection_type == 0:
            newRelation = []
            for inputElem in self.input_set:
                for outputElem in self.output_set:
                    if inputElem[0] == outputElem:
                        newRelation += [(inputElem, outputElem)]

        elif projection_type == 1:
            newRelation = []
            for inputElem in self.input_set:
                for outputElem in self.output_set:
                    if inputElem[1] == outputElem:
                        newRelation += [(inputElem, outputElem)]

        elif projection_type == 2:
            newRelation = []
            for inputElem in self.input_set:
                x_values = []
                y_values = []
                for innerInputElem in inputElem:
                    x_values.append(innerInputElem[0])
                    y_values.append(innerInputElem[1])
                for outputElem in self.output_set:
                    if set(x_values) == outputElem[0] and set(y_values) == outputElem[1]:
                        newRelation += [(inputElem, outputElem)]

        elif projection_type == 3:
            newRelation = []
            for inputElem in self.input_set:
                x_values = []
                for innerInputElem in inputElem:
                    x_values.append(innerInputElem[0])
                for outputElem in self.output_set:
                    if set(x_values) == outputElem:
                        newRelation += [(inputElem, outputElem)]

        elif projection_type == 4:
            newRelation = []
            for inputElem in self.input_set:
                y_values = []
                for innerInputElem in inputElem:
                    y_values.append(innerInputElem[1])
                for outputElem in self.output_set:
                    if set(y_values) == outputElem:
                        newRelation += [(inputElem, outputElem)]

        else:
            newRelation = []
            print("WARNING: Projection type does not exist")

        self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
                                    self.first_u_set_comboBox.currentText(),
                                    self.second_u_set_comboBox.currentText(),
                                    type="projection", projection_type=projection_type)

        self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
        self.scroll.setWidget(self.relationEdit)

        self.relationEdit.setVisible(self.relation_type == "custom")
        self.showContentButton.setVisible(self.relation_type != "custom")

    # def onUSetsChanged(self):
    #     if self.u_projection_type_comboBox.currentText() == "(x, y) -> x":
    #         self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
    #         self.output_set = set()
    #
    #         newRelation = []
    #         for tup in self.input_set:
    #             self.output_set |= {tup[0]}
    #             newRelation += [(tup, tup[0])]
    #
    #     elif self.u_projection_type_comboBox.currentText() == "(x, y) -> y":
    #         self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
    #         self.output_set = set()
    #
    #         newRelation = []
    #         for tup in self.input_set:
    #             self.output_set |= {tup[1]}
    #             newRelation += [(tup, tup[1])]
    #
    #     elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> ({x\u2081,...}, {y\u2081,...})":
    #         pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #         self.input_set = pow_set
    #         self.output_set = set()
    #
    #         newRelation = []
    #         for tup_set in pow_set:
    #             self.output_set |= {(frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set))}
    #             newRelation += [(tup_set, (frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set)))]
    #
    #     elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {x\u2081,...}":
    #         pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #         self.input_set = pow_set
    #         self.output_set = set()
    #
    #         newRelation = []
    #         for tup_set in pow_set:
    #             self.output_set |= {frozenset(x for (x, y) in tup_set)}
    #             newRelation += [(tup_set, frozenset(x for (x, y) in tup_set))]
    #
    #     elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {y\u2081,...}":
    #         pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #         self.input_set = pow_set
    #         self.output_set = set()
    #
    #         newRelation = []
    #         for tup_set in pow_set:
    #             self.output_set |= {frozenset(y for (x, y) in tup_set)}
    #             newRelation += [(tup_set, frozenset(y for (x, y) in tup_set))]
    #
    #     else:
    #         print("WARNING: Projection type does not exist")
    #
    #     self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
    #                                 self.u_set_comboBox.currentText(),
    #                                 type="projection", projection_type=self.u_projection_type_comboBox.currentText())
    #
    #     self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
    #     self.scroll.setWidget(self.relationEdit)
    #
    #     # input = self.sets_content[self.u_set_comboBox.currentText()]
    #     # powSet = self.power_set(input)
    #     # crossSet = set((x, y) for x in input for y in input)
    #     # self.input_set = self.power_set(crossSet)
    #     # self.output_set = set((x, y) for x in powSet for y in powSet)
    #     #
    #     # newRelation = []
    #     # for inp in self.input_set:
    #     #     calculatedU = self.u(inp)
    #     #     for outp in self.output_set:
    #     #         if calculatedU == outp:
    #     #             newRelation += [(inp, outp)]
    #     #
    #     # self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
    #     #                             self.u_set_comboBox.currentText(),
    #     #                             type="projection")
    #     #
    #     # self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
    #     # self.scroll.setWidget(self.relationEdit)

    def onProjectionTypeChanged(self):
        self.first_u_set_comboBox.currentIndexChanged.disconnect()
        self.second_u_set_comboBox.currentIndexChanged.disconnect()
        projection_type = list(FPTRelation.DICT_OF_PROJECTION_TYPES.values()).index(self.u_projection_type_comboBox.currentText())

        self.first_u_set_comboBox.clear()
        self.second_u_set_comboBox.clear()

        if projection_type == 0 or projection_type == 1:
            self.first_u_set_comboBox.addItems(self.set_of_tuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.sets_content.keys())
        elif projection_type == 2:
            self.first_u_set_comboBox.addItems(self.set_of_setsOfTuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.set_of_tupleOfSets_comboBox_keys)
        elif projection_type == 3 or projection_type == 4:
            self.first_u_set_comboBox.addItems(self.set_of_setsOfTuples_comboBox_keys)
            self.second_u_set_comboBox.addItems(self.set_of_sets_comboBox_keys)
        else:
            print("WARNING: Not existing projection type")

        self.first_u_set_comboBox.setCurrentText("-")
        self.second_u_set_comboBox.setCurrentText("-")

        self.first_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)
        self.second_u_set_comboBox.currentIndexChanged.connect(self.onUSetsChanged)

        self.relation = FPTRelation(self.relation.name, frozenset(),
                                    self.first_u_set_comboBox.currentText(),
                                    self.second_u_set_comboBox.currentText(),
                                    type="projection", projection_type=projection_type)

        self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
        self.scroll.setWidget(self.relationEdit)

    # def onProjectionTypeChanged(self):
    #     u_set_comboBox_keys = ["-"]
    #     if self.u_projection_type_comboBox.currentText() == "(x, y) -> x" or self.u_projection_type_comboBox.currentText() == "(x, y) -> y":
    #         for key in self.sets_content.keys():
    #             tempSet = self.sets_content[key]
    #             if tempSet is not None:
    #                 for elem in tempSet:
    #                     if type(elem) == tuple:
    #                         u_set_comboBox_keys.append(key)
    #                     break
    #     elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> ({x\u2081,...}, {y\u2081,...})":
    #         for key in self.sets_content.keys():
    #             tempSet = self.sets_content[key]
    #             if tempSet is not None:
    #                 for elem in tempSet:
    #                     if type(elem) == tuple:
    #                         if type(elem[0]) == str or type(elem[0]) == int or type(elem[0]) == float or type(
    #                                 elem[0]) == FPTMapping:
    #                             u_set_comboBox_keys.append(key)
    #                     break
    #     elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {x\u2081,...}" or self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {y\u2081,...}":
    #         for key in self.sets_content.keys():
    #             tempSet = self.sets_content[key]
    #             if tempSet is not None:
    #                 for elem in tempSet:
    #                     if type(elem) == tuple:
    #                         if type(elem[0]) == str or type(elem[0]) == int or type(elem[0]) == float or type(
    #                                 elem[0]) == FPTMapping or type(elem[0]) == tuple:
    #                             u_set_comboBox_keys.append(key)
    #                     break
    #     else:
    #         print("WARNING: projection type does not exist")
    #
    #     self.u_set_comboBox.currentIndexChanged.disconnect()
    #     self.u_set_comboBox.clear()
    #     self.u_set_comboBox.addItems(u_set_comboBox_keys)
    #     self.u_set_comboBox.currentIndexChanged.connect(self.onUSetChanged)
    #
    #     self.u_set_comboBox.setCurrentText("-")
    #
    #     if self.u_set_comboBox.count() > 0:
    #         if self.u_projection_type_comboBox.currentText() == "(x, y) -> x":
    #             self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
    #             self.output_set = set()
    #
    #             newRelation = []
    #             for tup in self.input_set:
    #                 self.output_set |= {tup[0]}
    #                 newRelation += [(tup, tup[0])]
    #
    #         elif self.u_projection_type_comboBox.currentText() == "(x, y) -> y":
    #             self.input_set = self.sets_content[self.u_set_comboBox.currentText()]
    #             self.output_set = set()
    #
    #             newRelation = []
    #             for tup in self.input_set:
    #                 self.output_set |= {tup[1]}
    #                 newRelation += [(tup, tup[1])]
    #
    #         elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> ({x\u2081,...}, {y\u2081,...})":
    #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #             self.input_set = pow_set
    #             self.output_set = set()
    #
    #             newRelation = []
    #             for tup_set in pow_set:
    #                 self.output_set |= {(frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set))}
    #                 newRelation += [(tup_set, (frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set)))]
    #
    #         elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {x\u2081,...}":
    #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #             self.input_set = pow_set
    #             self.output_set = set()
    #
    #             newRelation = []
    #             for tup_set in pow_set:
    #                 self.output_set |= {frozenset(x for (x, y) in tup_set)}
    #                 newRelation += [(tup_set, frozenset(x for (x, y) in tup_set))]
    #
    #         elif self.u_projection_type_comboBox.currentText() == "{(x\u2081, y\u2081),...} -> {y\u2081,...}":
    #             pow_set = self.power_set(self.sets_content[self.u_set_comboBox.currentText()])
    #             self.input_set = pow_set
    #             self.output_set = set()
    #
    #             newRelation = []
    #             for tup_set in pow_set:
    #                 self.output_set |= {frozenset(y for (x, y) in tup_set)}
    #                 newRelation += [(tup_set, frozenset(y for (x, y) in tup_set))]
    #
    #         else:
    #             print("WARNING: Projection type does not exist")
    #
    #         self.relation = FPTRelation(self.relation.name, frozenset(newRelation),
    #                                     self.u_set_comboBox.currentText(),
    #                                     type="projection",
    #                                     projection_type=self.u_projection_type_comboBox.currentText())
    #
    #         self.relationEdit = QDMRelationEdit(self.input_set, self.output_set, self.relation)
    #         self.scroll.setWidget(self.relationEdit)

    def showContent(self):
        # Threads does not really work
        # newThread = Thread(target=self.relationEdit.createCheckboxes())
        # newThread.start()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.relationEdit.createCheckboxes()

        self.showContentButton.setVisible(False)
        self.relationEdit.setVisible(True)

        # Thread(target=self.showContentThread).start()

    # def showContentThread(self):
    #     try:
    #         self.relationEdit.createCheckboxes()
    #         self.scroll.setWidget(self.relationEdit)
    #         print("DONE")
    #     except RuntimeError:
    #         print("TEST")

    def onSave(self):
        if self.relation_type == "custom":
            self.relation = FPTRelation(self.relation.name,
                                        self.relationEdit.getRelation(),
                                        self.relation.input_set_name,
                                        self.relation.output_set_name)
        elif self.relation_type == "is-element-of":
            pass
        elif self.relation_type == "projection":
            pass
        else:
            print("WARNING: Problems with relation type")
        self.accept()

        # if self.relation_type == "custom":
        #     self.relation = FPTRelation(self.relation.name,
        #                                 self.relationEdit.getRelation(),
        #                                 self.relation.input_set_name,
        #                                 self.relation.output_set_name)
        # elif self.relation_type == "is-element-of":
        #     self.relation = FPTRelation(self.relation.name,
        #                                 self.relationEdit.getRelation(),
        #                                 self.relation.input_set_name,
        #                                 type="is-element-of")
        # elif self.relation_type == "projection":
        #     self.relation = FPTRelation(self.relation.name,
        #                                 self.relationEdit.getRelation(),
        #                                 self.relation.input_set_name,
        #                                 type="projection")
        # else:
        #     print("WARNING: Problems with relation type")
        # self.accept()

    def onCancel(self):
        self.reject()
