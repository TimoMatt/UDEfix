from PyQt5.QtWidgets import *

from fixpointtool.content.fpt_content_listWidget_mapping_popup import QDMContentListWidgetMappingPopup
from fixpointtool.content.fpt_content_listWidget_relation_popup import QDMContentListWidgetRelationPopup
from fixpointtool.content.fpt_mapping import FPTMapping
from nodeeditor.utils import dumpException
from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.content.fpt_content_listWidget_sets_popup import QDMContentListWidgetSetPopup

DEBUG = False


class QDMContentListWidget(QListWidget):
    def __init__(self, dict, window, parent=None):
        super().__init__(parent)

        self.accessDicts = AccessDictionaries()
        self.dictionaryName = dict

        self.window = window

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.itemDoubleClicked.connect(self.launchPopup)

    def launchPopup(self, item):
        try:
            if self.dictionaryName == "mappings":
                func = self.accessDicts.getDictionaryWithoutTransformation("mappings")[item.text()]
                pop = QDMContentListWidgetMappingPopup(func)
                if pop.exec():
                    if DEBUG: print(pop.func_name)
                    if DEBUG: print(pop.list_of_tuples)
                    if DEBUG: print(pop.mapping_type)
                    if pop.func_name == pop.func.name:
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
                                                     input_set_name=pop.input_set_name,
                                                     output_set_name=pop.output_set_name)
                        newFunc.recreateFunctionFromList()
                        self.accessDicts.addElementToDictionary("mappings", pop.func_name, newFunc)

                        for subwnd in self.window.mdiArea.subWindowList():
                            for node in subwnd.widget().scene.nodes:
                                node.onDictChanged("mappings")
                            for node in subwnd.widget().scene.nodes:
                                node.eval()

                        self.window.content_changed = True
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
                                                     input_set_name=pop.input_set_name,
                                                     output_set_name=pop.output_set_name)
                        self.accessDicts.addElementToDictionary("mappings", pop.func_name, newFunc)
                        self.accessDicts.deleteElementFromDictionary("mappings", pop.func.name)
                        self.accessDicts.updateMappings(pop.func.name, pop.func_name)

                        for subwnd in self.window.mdiArea.subWindowList():
                            for node in subwnd.widget().scene.nodes:
                                node.onDictChanged("mappings", pop.func.name, pop.func_name)
                            for node in subwnd.widget().scene.nodes:
                                node.eval()

                        self.window.content_changed = True

            if self.dictionaryName == "sets":
                if item.text() != "-":
                    type_of_set = None
                    for elem in self.accessDicts.getDictionaryWithoutTransformation(self.dictionaryName)[item.text()]:
                        type_of_set = type(elem)
                        break
                    pop = QDMContentListWidgetSetPopup(item.text(), self.dictionaryName, type_of_set, self)
                    if pop.exec():
                        if item.text() != pop.keyName:
                            self.accessDicts.deleteElementFromDictionary(self.dictionaryName, item.text())
                        self.accessDicts.addElementToDictionary(self.dictionaryName, pop.keyName, pop.contentOfDict)
                        if item.text() != pop.keyName:
                            self.accessDicts.updateRelationsAndMappingsFromSetChange(item.text(), pop.keyName)

                            for subwnd in self.window.mdiArea.subWindowList():
                                for node in subwnd.widget().scene.nodes:
                                    node.onDictChanged("sets", item.text(), pop.keyName)
                                for node in subwnd.widget().scene.nodes:
                                    node.eval()
                        else:
                            self.accessDicts.updateRelationsAndMappingsFromSetChange(pop.keyName)

                            for subwnd in self.window.mdiArea.subWindowList():
                                for node in subwnd.widget().scene.nodes:
                                    node.onDictChanged("sets")
                                for node in subwnd.widget().scene.nodes:
                                    node.eval()

                        self.window.content_changed = True

            if self.dictionaryName == "relations":
                rel = self.accessDicts.getDictionaryWithoutTransformation("relations")[item.text()]
                if len(self.accessDicts.getDictionaryWithoutTransformation("sets")) > 0:
                    pop = QDMContentListWidgetRelationPopup(rel)
                    if pop.exec():
                        if item.text() != pop.relation.name:
                            self.accessDicts.deleteElementFromDictionary(self.dictionaryName, item.text())
                        self.accessDicts.addElementToDictionary(self.dictionaryName, pop.relation.name, pop.relation)

                        if item.text() != pop.relation.name:
                            for subwnd in self.window.mdiArea.subWindowList():
                                for node in subwnd.widget().scene.nodes:
                                    node.onDictChanged("relations", item.text(), pop.relation.name)
                                for node in subwnd.widget().scene.nodes:
                                    node.eval()
                        else:
                            for subwnd in self.window.mdiArea.subWindowList():
                                for node in subwnd.widget().scene.nodes:
                                    node.onDictChanged("relations")
                                for node in subwnd.widget().scene.nodes:
                                    node.eval()

                        self.window.content_changed = True

            self.connectWithDictionary()
        except Exception as e:
            dumpException(e)

    def connectWithDictionary(self):
        self.clear()
        self.addItems(self.accessDicts.getDictionaryWithoutTransformation(self.dictionaryName))

