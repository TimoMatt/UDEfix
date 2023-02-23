from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from fixpointtool.content.fpt_content import AccessDictionaries, DICT_OF_DICTS
from fixpointtool.content.fpt_content_listWidget import QDMContentListWidget
from fixpointtool.content.fpt_content_listWidget_mapping_popup import QDMContentListWidgetMappingPopup
from fixpointtool.content.fpt_content_listWidget_sets_popup import QDMContentListWidgetSetPopup
from fixpointtool.content.fpt_content_listWidget_relation_popup import QDMContentListWidgetRelationPopup
from fixpointtool.content.fpt_mapping import FPTMapping
from fixpointtool.content.fpt_relation import FPTRelation

DEBUG = False


class QDMContentWidget(QWidget):
    listOfQDMContentWidget = []

    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.window = window

        self.initUI()

        self.accessDicts = AccessDictionaries()

        QDMContentWidget.listOfQDMContentWidget.append(self)

    def initUI(self):
        self.vbox = QVBoxLayout()

        self.allMappingsListWidget = QDMContentListWidget("mappings", self.window)
        self.relationsListWidget = QDMContentListWidget("relations", self.window)
        self.setsListWidget = QDMContentListWidget("sets", self.window)

        self.allMappingsListWidget.connectWithDictionary()
        self.relationsListWidget.connectWithDictionary()
        self.setsListWidget.connectWithDictionary()

        self.mappingsLabel = QLabel("Mappings:")
        self.relationsLabel = QLabel("Relations:")
        self.setsLabel = QLabel("Sets:")

        self.add_button0 = QPushButton("+")
        self.add_button0.setFixedHeight(23)
        self.add_button0.setFixedWidth(23)
        self.add_button0.setDefault(False)
        self.add_button0.setAutoDefault(False)
        self.add_button0.clicked.connect(self.addItem0)

        self.delete_button0 = QPushButton("-")
        self.delete_button0.setFixedHeight(23)
        self.delete_button0.setFixedWidth(23)
        self.delete_button0.setDefault(False)
        self.delete_button0.setAutoDefault(False)
        self.delete_button0.clicked.connect(self.deleteSelectedItems0)

        self.newKeyName0 = QLineEdit()

        self.addBox0 = QHBoxLayout()
        self.newKeyName0.setFixedHeight(23)
        self.addBox0.addWidget(self.newKeyName0)
        self.addBox0.addWidget(self.add_button0)
        self.addBox0.addWidget(self.delete_button0)
        self.addBox0.setAlignment(Qt.AlignRight)

        self.add_button1 = QPushButton("+")
        self.add_button1.setFixedHeight(23)
        self.add_button1.setFixedWidth(23)
        self.add_button1.setDefault(False)
        self.add_button1.setAutoDefault(False)
        self.add_button1.clicked.connect(self.addItem1)

        self.delete_button1 = QPushButton("-")
        self.delete_button1.setFixedHeight(23)
        self.delete_button1.setFixedWidth(23)
        self.delete_button1.setDefault(False)
        self.delete_button1.setAutoDefault(False)
        self.delete_button1.clicked.connect(self.deleteSelectedItems1)

        self.newKeyName1 = QLineEdit()

        self.addBox1 = QHBoxLayout()
        self.newKeyName1.setFixedHeight(23)
        self.addBox1.addWidget(self.newKeyName1)
        self.addBox1.addWidget(self.add_button1)
        self.addBox1.addWidget(self.delete_button1)
        self.addBox1.setAlignment(Qt.AlignRight)

        self.add_button4 = QPushButton("+")
        self.add_button4.setFixedHeight(23)
        self.add_button4.setFixedWidth(23)
        self.add_button4.setDefault(False)
        self.add_button4.setAutoDefault(False)
        self.add_button4.clicked.connect(self.addItem4)

        self.delete_button4 = QPushButton("-")
        self.delete_button4.setFixedHeight(23)
        self.delete_button4.setFixedWidth(23)
        self.delete_button4.setDefault(False)
        self.delete_button4.setAutoDefault(False)
        self.delete_button4.clicked.connect(self.deleteSelectedItems4)

        self.newKeyName4 = QLineEdit()

        self.addBox4 = QHBoxLayout()
        self.newKeyName4.setFixedHeight(23)
        self.addBox4.addWidget(self.newKeyName4)
        self.addBox4.addWidget(self.add_button4)
        self.addBox4.addWidget(self.delete_button4)
        self.addBox4.setAlignment(Qt.AlignRight)

        self.vbox.addWidget(self.mappingsLabel)
        self.vbox.addWidget(self.allMappingsListWidget)
        self.vbox.addLayout(self.addBox0)
        self.vbox.addWidget(self.relationsLabel)
        self.vbox.addWidget(self.relationsListWidget)
        self.vbox.addLayout(self.addBox4)
        self.vbox.addWidget(self.setsLabel)
        self.vbox.addWidget(self.setsListWidget)
        self.vbox.addLayout(self.addBox1)

        self.setLayout(self.vbox)

    def addItem1(self):
        newSetName = self.newKeyName1.text()
        if newSetName not in self.accessDicts.getDictionaryWithoutTransformation("sets").keys():

            # get new name if no name has been entered
            if newSetName == "":
                newSetName = "new set"
                counter = 1
                while True:
                    if newSetName + str(counter) not in self.accessDicts.getDictionaryWithoutTransformation("sets").keys():
                        newSetName = newSetName + str(counter)
                        break
                    counter += 1

            newSet = frozenset()
            self.accessDicts.addElementToDictionary("sets", newSetName, newSet)
            pop = QDMContentListWidgetSetPopup(newSetName, "sets", str, self)
            if pop.exec():
                if newSetName != pop.keyName:
                    self.accessDicts.deleteElementFromDictionary("sets", newSetName)
                self.accessDicts.addElementToDictionary("sets", pop.keyName, pop.contentOfDict)

                for subwnd in self.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("sets", new_name=pop.keyName)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.window.content_changed = True
            else:
                self.accessDicts.deleteElementFromDictionary("sets", newSetName)
            self.setsListWidget.connectWithDictionary()
            self.newKeyName1.clear()

    def addItem0(self):
        newFuncName = self.newKeyName0.text()
        if newFuncName not in self.accessDicts.getDictionaryWithoutTransformation("mappings").keys():

            # get new name if no name has been entered
            if newFuncName == "":
                newFuncName = "new mapping"
                counter = 1
                while True:
                    if newFuncName + str(counter) not in self.accessDicts.getDictionaryWithoutTransformation("mappings").keys():
                        newFuncName = newFuncName + str(counter)
                        break
                    counter += 1

            newFunc = FPTMapping(newFuncName, [], "all", "-", "-")
            self.accessDicts.addElementToDictionary("mappings", newFuncName, newFunc)
            pop = QDMContentListWidgetMappingPopup(newFunc)
            if pop.exec():
                if DEBUG: print(pop.func_name)
                if DEBUG: print(pop.list_of_tuples)
                if pop.func_name == pop.func.name:
                    if pop.input_set_name == "custom set" and pop.output_set_name == "custom set":
                        newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type)
                    elif pop.input_set_name == "custom set":
                        if pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, output_mv=pop.output_mv, output_mv_k=pop.output_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, output_set_name=pop.output_set_name)
                    elif pop.output_set_name == "custom set":
                        if pop.input_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_mv=pop.input_mv, input_mv_k=pop.input_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_set_name=pop.input_set_name)
                    else:
                        if pop.input_set_name == "MV-algebra" and pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_mv=pop.input_mv, input_mv_k=pop.input_mv_k, output_mv=pop.output_mv, output_mv_k=pop.output_mv_k)
                        elif pop.input_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_mv=pop.input_mv, input_mv_k=pop.input_mv_k, output_set_name=pop.output_set_name)
                        elif pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_set_name=pop.input_set_name, output_mv=pop.output_mv, output_mv_k=pop.output_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type, input_set_name=pop.input_set_name, output_set_name=pop.output_set_name)
                    newFunc.recreateFunctionFromList()
                    self.accessDicts.addElementToDictionary("mappings", pop.func_name, newFunc)
                else:
                    if pop.input_set_name == "custom set" and pop.output_set_name == "custom set":
                        newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type)
                    elif pop.input_set_name == "custom set":
                        if pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 output_mv=pop.output_mv, output_mv_k=pop.output_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 output_set_name=pop.output_set_name)
                    elif pop.output_set_name == "custom set":
                        if pop.input_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_mv=pop.input_mv, input_mv_k=pop.input_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_set_name=pop.input_set_name)
                    else:
                        if pop.input_set_name == "MV-algebra" and pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_mv=pop.input_mv, input_mv_k=pop.input_mv_k,
                                                 output_mv=pop.output_mv, output_mv_k=pop.output_mv_k)
                        elif pop.input_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_mv=pop.input_mv, input_mv_k=pop.input_mv_k,
                                                 output_set_name=pop.output_set_name)
                        elif pop.output_set_name == "MV-algebra":
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_set_name=pop.input_set_name, output_mv=pop.output_mv,
                                                 output_mv_k=pop.output_mv_k)
                        else:
                            newFunc = FPTMapping(pop.func_name, pop.list_of_tuples, pop.mapping_type,
                                                 input_set_name=pop.input_set_name, output_set_name=pop.output_set_name)
                    self.accessDicts.addElementToDictionary("mappings", pop.func_name, newFunc)
                    self.accessDicts.deleteElementFromDictionary("mappings", pop.func.name)
                    self.accessDicts.updateMappings(pop.func.name, pop.func_name)

                for subwnd in self.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.window.content_changed = True

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", newFuncName)
                FPTMapping.dictOfFPTMappings.pop(newFuncName)
                FPTMapping.dictOfMappings.pop(newFuncName)
            self.allMappingsListWidget.connectWithDictionary()
            self.newKeyName0.clear()

    def deleteSelectedItems0(self):
        for item in self.allMappingsListWidget.selectedItems():
            if DEBUG: print("DELETED:", item.text())
            self.accessDicts.deleteElementFromDictionary("mappings", item.text())
            self.accessDicts.updateMappings(item.text())

            for subwnd in self.window.mdiArea.subWindowList():
                for node in subwnd.widget().scene.nodes:
                    node.onDictChanged("mappings", item.text())
                for node in subwnd.widget().scene.nodes:
                    node.eval()

            self.window.content_changed = True

        self.allMappingsListWidget.connectWithDictionary()

    def deleteSelectedItems1(self):
        for item in self.setsListWidget.selectedItems():
            if item.text() != "-":
                self.accessDicts.deleteElementFromDictionary("sets", item.text())
                self.accessDicts.updateRelationsAndMappingsFromSetChange(item.text(), deleted=True)

                for subwnd in self.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("sets", item.text())
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.window.content_changed = True

        self.allMappingsListWidget.connectWithDictionary()
        self.relationsListWidget.connectWithDictionary()
        self.setsListWidget.connectWithDictionary()

    def addItem4(self):
        try:
            newRelationName = self.newKeyName4.text()
            if newRelationName not in self.accessDicts.getDictionaryWithoutTransformation("relations").keys() and len(self.accessDicts.getDictionaryWithoutTransformation("sets")) > 0:

                # get new name if no name has been entered
                if newRelationName == "":
                    newRelationName = "new relation"
                    counter = 1
                    while True:
                        if newRelationName + str(counter) not in self.accessDicts.getDictionaryWithoutTransformation("relations").keys():
                            newRelationName = newRelationName + str(counter)
                            break
                        counter += 1

                newRelation = FPTRelation(newRelationName, set(), "-", "-")
                self.accessDicts.addElementToDictionary("relations", newRelationName, newRelation)
                pop = QDMContentListWidgetRelationPopup(newRelation)
                if pop.exec():
                    if newRelationName != pop.relation.name:
                        self.accessDicts.deleteElementFromDictionary("relations", newRelationName)
                    self.accessDicts.addElementToDictionary("relations", pop.relation.name, pop.relation)

                    for subwnd in self.window.mdiArea.subWindowList():
                        for node in subwnd.widget().scene.nodes:
                            node.onDictChanged("relations", new_name=pop.relation.name)
                        for node in subwnd.widget().scene.nodes:
                            node.eval()

                    self.window.content_changed = True

                else:
                    self.accessDicts.deleteElementFromDictionary("relations", newRelationName)
                self.relationsListWidget.connectWithDictionary()
                self.newKeyName4.clear()
        except Exception as e:
            print(e)

    def deleteSelectedItems4(self):
        for item in self.relationsListWidget.selectedItems():
            self.accessDicts.deleteElementFromDictionary("relations", item.text())

            for subwnd in self.window.mdiArea.subWindowList():
                for node in subwnd.widget().scene.nodes:
                    node.onDictChanged("relations", item.text())
                for node in subwnd.widget().scene.nodes:
                    node.eval()

            self.window.content_changed = True

        self.relationsListWidget.connectWithDictionary()

    @staticmethod
    def reconnectAllDictionaries():
        for obj in QDMContentWidget.listOfQDMContentWidget:
            obj.allMappingsListWidget.connectWithDictionary()
            obj.relationsListWidget.connectWithDictionary()
            obj.setsListWidget.connectWithDictionary()
