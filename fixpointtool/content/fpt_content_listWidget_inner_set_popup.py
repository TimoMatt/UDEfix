from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidgetItem import QDMListWidgetItem
from fixpointtool.content.fpt_mapping import FPTMapping


class QDMContentListWidgetInnerSetPopup(QDialog):
    LIST_OF_TUPLE_TYPES = ["string", "number"]

    def __init__(self, set, type_of_set, excluded_mapping=None, parent=None):
        super().__init__(parent)

        self.excluded_mapping = excluded_mapping

        self.set = set
        self.type_of_set = type_of_set

        self.types_of_inner_tuple = ["string", "string"]
        if self.type_of_set[0] == "n-tuple":
            self.types_of_inner_tuple = self.type_of_set[1]

        self.setWindowTitle("Edit set")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(300, 300)

        self.accessDicts = AccessDictionaries()

        self.content_label = QLabel("Content:")

        self.set_listWidget = QListWidget()
        self.set_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectSet()

        if self.type_of_set == "n-tuple":
            self.set_listWidget.itemDoubleClicked.connect(self.launchPopup)

        # self.tupleType_label = QLabel("Tuple type:")
        # self.tupleType_label.setMargin(4)
        #
        # self.tupleType_comboBox = QComboBox()
        # self.tupleType_comboBox.addItems(QDMContentListWidgetInnerSetPopup.LIST_OF_TUPLE_TYPES)
        # self.tupleType_comboBox.setCurrentText(self.types_of_inner_tuple)
        # self.tupleType_comboBox.currentIndexChanged.connect(self.onTupleTypeChanged)
        #
        # self.tupleTypeBox = QHBoxLayout()
        # self.tupleTypeBox.addWidget(self.tupleType_label)
        # self.tupleTypeBox.addWidget(self.tupleType_comboBox)

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

        sp = self.newMappingName.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.newMappingName.setSizePolicy(sp)

        self.newMappingName.setFixedHeight(23)
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
        self.vbox.addWidget(self.content_label)
        # self.vbox.addLayout(self.tupleTypeBox)
        self.vbox.addWidget(self.set_listWidget)
        self.vbox.addLayout(self.addBox)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        # self.tupleType_comboBox.setVisible(self.type_of_set == "2-tuple")
        # self.tupleType_label.setVisible(self.type_of_set == "2-tuple")
        self.newMappingName.setVisible(self.type_of_set == "mapping")

    def connectSet(self):
        self.set_listWidget.clear()
        if self.type_of_set == "string" or self.type_of_set == "number":
            for elem in sorted(self.set):
                item = QDMListWidgetItem(elem, self.type_of_set)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.set_listWidget.addItem(item)
        elif self.type_of_set[0] == "n-tuple":
            for elem in sorted(self.set):
                item = QDMListWidgetItem(elem, "n-tuple")
                self.set_listWidget.addItem(item)
        elif self.type_of_set == "mapping":
            for elem in sorted(self.set, key=lambda mapping: mapping.name):
                item = QDMListWidgetItem(elem, self.type_of_set)
                self.set_listWidget.addItem(item)

    # def onTupleTypeChanged(self):
    #     self.types_of_inner_tuple = self.tupleType_comboBox.currentText()
    #     self.set = set()
    #     self.connectSet()

    def launchPopup(self, item):
        from fixpointtool.content.fpt_content_listWidget_inner_n_tuple_popup import QDMContentListWidgetNTuplePopup
        pop = QDMContentListWidgetNTuplePopup(item.item, self.types_of_inner_tuple)
        if pop.exec():
            item.item = pop.tuple
            item.overwriteText()

    def addItem(self):
        if self.type_of_set == "string":
            newItem = QDMListWidgetItem("enter name", self.type_of_set)
            newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
            self.set_listWidget.addItem(newItem)
            self.set_listWidget.editItem(newItem)
            self.set_listWidget.scrollToBottom()
        elif self.type_of_set == "number":
            newItem = QDMListWidgetItem("enter number", self.type_of_set)
            newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
            self.set_listWidget.addItem(newItem)
            self.set_listWidget.editItem(newItem)
            self.set_listWidget.scrollToBottom()
        # elif self.type_of_set == "2-tuple":
        #     from fixpointtool.content.fpt_content_listWidget_inner_tuple_popup import QDMContentListWidgetTuplePopup
        #     pop = QDMContentListWidgetTuplePopup(tuple(["", ""]), self.types_of_inner_tuple)
        #     if pop.exec():
        #         try:
        #             newItem = QDMListWidgetItem(pop.tuple, self.type_of_set)
        #             self.set_listWidget.addItem(newItem)
        #             self.set_listWidget.scrollToBottom()
        #         except Exception as e:
        #             print(e)
        elif self.type_of_set == "mapping":
            if self.newMappingName.count() > 0:
                newItem = QDMListWidgetItem(FPTMapping(self.newMappingName.currentText()), self.type_of_set)
                self.set_listWidget.addItem(newItem)
                self.loadMappings()
            self.set_listWidget.scrollToBottom()
        elif self.type_of_set[0] == "n-tuple":
            default_tuple = []
            for i in range(len(self.types_of_inner_tuple)):
                if self.types_of_inner_tuple[i] == "string":
                    default_tuple.append("")
                elif self.types_of_inner_tuple[i] == "number":
                    default_tuple.append(0)
            from fixpointtool.content.fpt_content_listWidget_inner_n_tuple_popup import QDMContentListWidgetNTuplePopup
            pop = QDMContentListWidgetNTuplePopup(tuple(default_tuple), self.types_of_inner_tuple)
            if pop.exec():
                newItem = QDMListWidgetItem(pop.tup, "n-tuple")
                self.set_listWidget.addItem(newItem)
                self.set_listWidget.scrollToBottom()

    def deleteSelectedItems(self):
        for item in self.set_listWidget.selectedItems():
            self.set_listWidget.takeItem(self.set_listWidget.row(item))
        if self.type_of_set == "mapping":
            self.loadMappings()

    def loadMappings(self):
        allMappings = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        if self.excluded_mapping is not None:
            allMappings.pop(self.excluded_mapping)
        for i in range(0, self.set_listWidget.count()):
            allMappings.pop(self.set_listWidget.item(i).item.name)
        self.newMappingName.clear()
        self.newMappingName.addItems(allMappings)

    def onSave(self):
        if self.type_of_set == "string":
            self.set = set()
            doubleValues = False
            for i in range(0, self.set_listWidget.count()):
                if self.set_listWidget.item(i).text() in self.set:
                    doubleValues = True
                self.set.add(self.set_listWidget.item(i).text())
            if doubleValues:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nDuplicates have been removed from the list")
                msg.exec()
            self.set = frozenset(self.set)
            self.accept()

        elif self.type_of_set == "number":
            self.set = set()
            doubleValues = False
            try:
                for i in range(0, self.set_listWidget.count()):
                    if float(self.set_listWidget.item(i).text()) in self.set:
                        doubleValues = True
                    self.set.add(float(self.set_listWidget.item(i).text()))
                if doubleValues:
                    msg = QMessageBox()
                    msg.setWindowTitle("Information")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information:\nDuplicates have been removed from the list")
                    msg.exec()
                self.set = frozenset(self.set)
                self.accept()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning:\nThere are inputs of a wrong type")
                msg.exec()

        elif self.type_of_set[0] == "n-tuple":
            self.set = set()
            doubleValues = False
            for i in range(0, self.set_listWidget.count()):
                if self.set_listWidget.item(i).item in self.set:
                    doubleValues = True
                self.set.add(self.set_listWidget.item(i).item)
            if doubleValues:
                msg = QMessageBox()
                msg.setWindowTitle("Information")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information:\nDuplicates have been removed from the list")
                msg.exec()
            self.set = frozenset(self.set)
            self.accept()

        # elif self.type_of_set == "2-tuple":
        #     self.set = set()
        #     doubleValues = False
        #     for i in range(0, self.set_listWidget.count()):
        #         if self.set_listWidget.item(i).item in self.set:
        #             doubleValues = True
        #         self.set.add(self.set_listWidget.item(i).item)
        #     if doubleValues:
        #         msg = QMessageBox()
        #         msg.setWindowTitle("Information")
        #         msg.setIcon(QMessageBox.Information)
        #         msg.setText("Information:\nDuplicates have been removed from the list")
        #         msg.exec()
        #     self.set = frozenset(self.set)
        #     self.accept()

        elif self.type_of_set == "mapping":
            self.set = set()
            for i in range(0, self.set_listWidget.count()):
                self.set.add(FPTMapping(self.set_listWidget.item(i).text()))
            self.set = frozenset(self.set)
            self.accept()

    def onCancel(self):
        self.reject()
