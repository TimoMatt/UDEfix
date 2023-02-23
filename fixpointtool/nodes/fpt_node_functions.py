from PyQt5 import QtGui

from fixpointtool.content.fpt_content_listWidget_mapping_popup import QDMContentListWidgetMappingPopup
from fixpointtool.content.fpt_content_listWidget_relation_popup import QDMContentListWidgetRelationPopup
from fixpointtool.content.fpt_content_widget import QDMContentWidget
from fixpointtool.content.fpt_mapping import FPTMapping
from fixpointtool.content.fpt_relation import FPTRelation
from fixpointtool.fpt_conf import *
from fixpointtool.fpt_node_base import *
from nodeeditor.utils import dumpException
from fixpointtool.content.fpt_content import AccessDictionaries
from fixpointtool.functions.fpt_functions import *


DEBUG = False


class FPTFunctionContent(QDMNodeContentWidget):
    def initUI(self):
        self.parameter_label = QLabel("Parameter:")
        self.input_label = QLabel("Input:")
        self.output_label = QLabel("Output:")

        self.parameter_box = QComboBox()
        self.input_box = QComboBox()
        self.output_box = QComboBox()

        self.parameter_box.setMaximumWidth(200)
        self.input_box.setMaximumWidth(200)
        self.output_box.setMaximumWidth(200)

        self.parameter_add = QPushButton("+")
        self.parameter_add.setMaximumWidth(30)

        self.parameter_box.setObjectName(self.node.content_label_objname)
        self.input_box.setObjectName(self.node.content_label_objname)
        self.output_box.setObjectName(self.node.content_label_objname)
        self.parameter_label.setObjectName(self.node.content_label_objname)
        self.input_label.setObjectName(self.node.content_label_objname)
        self.output_label.setObjectName(self.node.content_label_objname)
        self.parameter_add.setObjectName(self.node.content_label_objname + "button")

        self.parameter_hBox = QHBoxLayout()
        self.parameter_hBox.addWidget(self.parameter_box)
        self.parameter_hBox.addWidget(self.parameter_add)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.parameter_label)
        self.vbox.addLayout(self.parameter_hBox)
        self.vbox.addWidget(self.input_label)
        self.vbox.addWidget(self.input_box)
        self.vbox.addWidget(self.output_label)
        self.vbox.addWidget(self.output_box)
        self.setLayout(self.vbox)

    def serialize(self):
        res = super().serialize()
        res['parameter_box'] = self.parameter_box.currentText()
        res['input_box'] = self.input_box.currentText()
        res['output_box'] = self.output_box.currentText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            name1, name2, name3 = data['parameter_box'], data['input_box'], data['output_box']
            self.parameter_box.setCurrentText(name1)
            self.input_box.setCurrentText(name2)
            self.output_box.setCurrentText(name3)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class FPTFunctionAverageContent(QDMNodeContentWidget):
    def initUI(self):
        self.input_label = QLabel("Input:")
        self.output_label = QLabel("Output:")

        self.input_box = QComboBox()
        self.output_box = QComboBox()

        self.input_box.setMaximumWidth(200)
        self.output_box.setMaximumWidth(200)

        self.input_box.setObjectName(self.node.content_label_objname)
        self.output_box.setObjectName(self.node.content_label_objname)
        self.input_label.setObjectName(self.node.content_label_objname)
        self.output_label.setObjectName(self.node.content_label_objname)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.input_label)
        self.vbox.addWidget(self.input_box)
        self.vbox.addWidget(self.output_label)
        self.vbox.addWidget(self.output_box)
        self.setLayout(self.vbox)

    def serialize(self):
        res = super().serialize()
        res['input_box'] = self.input_box.currentText()
        res['output_box'] = self.output_box.currentText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            name1, name2 = data['input_box'], data['output_box']
            self.input_box.setCurrentText(name1)
            self.output_box.setCurrentText(name2)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class FPTFunctionHigherOrderFunctionContent(QDMNodeContentWidget):
    def initUI(self):
        self.information_label = QLabel("Function:")
        self.function_label = QLabel("f(a)")

        self.information_label.setObjectName(self.node.content_label_objname + "1")
        self.function_label.setObjectName(self.node.content_label_objname + "2")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.information_label)
        self.vbox.addWidget(self.function_label)
        self.setLayout(self.vbox)

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_CODE_CONSTANT)
class FPTNode_Constant(FPTNode):
    icon = "fixpointtool/icons/constant.png"
    op_code = OP_CODE_CONSTANT
    op_title = "Constant"
    content_label = "c"
    content_label_objname = "fpt_node_constant"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addConstantMapping)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "constant" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.parameter_box.addItems(listOfAvailableFunctions)
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

        # self.content.parameter_box.addItem("- add mapping -")
        # self.content.input_box.addItem("-     add set     -")
        # self.content.output_box.addItem("-     add set     -")

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "constant" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "constant" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "constant" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addConstantMapping(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "constant", input_set_name=output_set_name, output_mv=config['all']['mv-algebra'], output_mv_k=config['all']['k'])

            self.accessDicts.addElementToDictionary("mappings", new_mapping_name, new_mapping)
            pop = QDMContentListWidgetMappingPopup(new_mapping)
            if pop.exec():
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

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                if pop.mapping_type == "constant" or pop.mapping_type == "all":
                    self.content.parameter_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "c"
        dict_of_constants = self.accessDicts.getDictionary("mappings")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = c(dict_of_constants.get(self.content.parameter_box.currentText()),
                          dict_of_sets.get(self.content.input_box.currentText()),
                          dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = c_hash(dict_of_constants.get(self.content.parameter_box.currentText()),
                                    dict_of_sets.get(self.content.input_box.currentText()),
                                    dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = c_iota(dict_of_constants.get(self.content.parameter_box.currentText()),
                                    dict_of_sets.get(self.content.input_box.currentText()),
                                    dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("CONSTANT - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("CONSTANT - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("CONSTANT - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_ADDITION)
class FPTNode_Addition(FPTNode):
    icon = "fixpointtool/icons/addition.png"
    op_code = OP_CODE_ADDITION
    op_title = "Addition"
    content_label = "add"
    content_label_objname = "fpt_node_addition"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addAdditionMapping)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.parameter_box.addItems(listOfAvailableFunctions)
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addAdditionMapping(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "arithmetic", input_set_name=input_set_name,
                                     output_mv=config['all']['mv-algebra'], output_mv_k=config['all']['k'])

            self.accessDicts.addElementToDictionary("mappings", new_mapping_name, new_mapping)
            pop = QDMContentListWidgetMappingPopup(new_mapping)
            if pop.exec():
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

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                if pop.mapping_type == "arithmetic" or pop.mapping_type == "all":
                    self.content.parameter_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "add"
        dict_of_addition = self.accessDicts.getDictionary("mappings")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = add(dict_of_addition.get(self.content.parameter_box.currentText()),
                          dict_of_sets.get(self.content.input_box.currentText()),
                          dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = add_hash(dict_of_addition.get(self.content.parameter_box.currentText()),
                                    dict_of_sets.get(self.content.input_box.currentText()),
                                    dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = add_iota(dict_of_addition.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("ADDITION - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("ADDITION - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("ADDITION - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_SUBTRACTION)
class FPTNode_Subtraction(FPTNode):
    icon = "fixpointtool/icons/subtraction.png"
    op_code = OP_CODE_SUBTRACTION
    op_title = "Subtraction"
    content_label = "sub"
    content_label_objname = "fpt_node_subtraction"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addSubtractionMapping)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.parameter_box.addItems(listOfAvailableFunctions)
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addSubtractionMapping(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "arithmetic", input_set_name=input_set_name,
                                     output_mv=config['all']['mv-algebra'], output_mv_k=config['all']['k'])

            self.accessDicts.addElementToDictionary("mappings", new_mapping_name, new_mapping)
            pop = QDMContentListWidgetMappingPopup(new_mapping)
            if pop.exec():
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

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                if pop.mapping_type == "arithmetic"or pop.mapping_type == "all":
                    self.content.parameter_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "sub"
        dict_of_subtraction = self.accessDicts.getDictionary("mappings")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = sub(dict_of_subtraction.get(self.content.parameter_box.currentText()),
                          dict_of_sets.get(self.content.input_box.currentText()),
                          dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = sub_hash(dict_of_subtraction.get(self.content.parameter_box.currentText()),
                                    dict_of_sets.get(self.content.input_box.currentText()),
                                    dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = sub_iota(dict_of_subtraction.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("SUBTRACTION - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("SUBTRACTION - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("SUBTRACTION - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_SUBTRACTION_Z)
class FPTNode_Subtraction_z(FPTNode):
    icon = "fixpointtool/icons/subtraction_z.png"
    op_code = OP_CODE_SUBTRACTION_Z
    op_title = "Subtraction\u1DBB"
    content_label = "sub\u1DBB"
    content_label_objname = "fpt_node_subtraction_z"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addSubtractionMapping)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.parameter_box.addItems(listOfAvailableFunctions)
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "arithmetic" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addSubtractionMapping(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "arithmetic", input_set_name=input_set_name,
                                     output_mv=config['all']['mv-algebra'], output_mv_k=config['all']['k'])

            self.accessDicts.addElementToDictionary("mappings", new_mapping_name, new_mapping)
            pop = QDMContentListWidgetMappingPopup(new_mapping)
            if pop.exec():
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

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                if pop.mapping_type == "arithmetic" or pop.mapping_type == "all":
                    self.content.parameter_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "sub\u1DBB"
        dict_of_subtraction_z = self.accessDicts.getDictionary("mappings")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = sub_z(dict_of_subtraction_z.get(self.content.parameter_box.currentText()),
                          dict_of_sets.get(self.content.input_box.currentText()),
                          dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = sub_z_hash(dict_of_subtraction_z.get(self.content.parameter_box.currentText()),
                                    dict_of_sets.get(self.content.input_box.currentText()),
                                    dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = sub_z_iota(dict_of_subtraction_z.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("SUBTRACTION\u1DBB - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("SUBTRACTION\u1DBB - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("SUBTRACTION\u1DBB - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_REINDEXING)
class FPTNode_Reindexing(FPTNode):
    icon = "fixpointtool/icons/reindexing.png"
    op_code = OP_CODE_REINDEXING
    op_title = "Reindexing"
    content_label = "u"
    content_label_objname = "fpt_node_reindexing"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addReindexingMapping)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "reindexing" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.parameter_box.addItems(listOfAvailableFunctions)
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "reindexing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "reindexing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "reindexing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.parameter_box.addItems(listOfAvailableFunctions)

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addReindexingMapping(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":
            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "reindexing", output_set_name, input_set_name)
            self.accessDicts.addElementToDictionary("mappings", new_mapping_name, new_mapping)
            pop = QDMContentListWidgetMappingPopup(new_mapping)
            if pop.exec():
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

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("mappings", new_name=pop.func_name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                if pop.mapping_type == "reindexing" or pop.mapping_type == "all":
                    self.content.parameter_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "u"
        dict_of_reindexing_functions = self.accessDicts.getDictionary("mappings")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = reindexing(dict_of_reindexing_functions.get(self.content.parameter_box.currentText()),
                                   dict_of_sets.get(self.content.input_box.currentText()),
                                   dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = reindexing_hash(dict_of_reindexing_functions.get(self.content.parameter_box.currentText()),
                                             dict_of_sets.get(self.content.input_box.currentText()),
                                             dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = reindexing_iota(dict_of_reindexing_functions.get(self.content.parameter_box.currentText()),
                                             dict_of_sets.get(self.content.input_box.currentText()),
                                             dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("REINDEXING - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("REINDEXING - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("REINDEXING - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_MINIMUM)
class FPTNode_Minimum(FPTNode):
    icon = "fixpointtool/icons/minimum.png"
    op_code = OP_CODE_MINIMUM
    op_title = "Minimum"
    content_label = "min"
    content_label_objname = "fpt_node_minimum"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addRelation)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        self.content.parameter_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("relations").keys())
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            pass
        elif category == "relations":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addRelation(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "":

            new_relation_name = "new relation"
            counter = 1
            while True:
                if new_relation_name + str(counter) not in self.accessDicts.getDictionaryWithoutTransformation("relations").keys():
                    new_relation_name = new_relation_name + str(counter)
                    break
                counter += 1

            new_relation = FPTRelation(new_relation_name, set(), input_set_name, output_set_name)
            self.accessDicts.addElementToDictionary("relations", new_relation_name, new_relation)
            pop = QDMContentListWidgetRelationPopup(new_relation)

            if pop.exec():
                if new_relation_name != pop.relation.name:
                    self.accessDicts.deleteElementFromDictionary("relations", new_relation_name)
                self.accessDicts.addElementToDictionary("relations", pop.relation.name, pop.relation)

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("relations", new_name=pop.relation.name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                self.content.parameter_box.setCurrentText(pop.relation.name)
            else:
                self.accessDicts.deleteElementFromDictionary("relations", new_relation_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "min"
        dict_of_relations = self.accessDicts.getDictionary("relations")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = min(dict_of_relations.get(self.content.parameter_box.currentText()),
                            dict_of_sets.get(self.content.input_box.currentText()),
                            dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = min_hash(dict_of_relations.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = min_iota(dict_of_relations.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("MINIMUM - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("MINIMUM - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("MINIMUM - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_MAXIMUM)
class FPTNode_Maximum(FPTNode):
    icon = "fixpointtool/icons/maximum.png"
    op_code = OP_CODE_MAXIMUM
    op_title = "Maximum"
    content_label = "max"
    content_label_objname = "fpt_node_maximum"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionContent(self)

        self.fillComboBoxes()

        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.content.parameter_add.clicked.connect(self.addRelation)

        self.grNode = FPTGraphicsFunctionNode(self)

    def fillComboBoxes(self):
        self.content.parameter_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("relations").keys())
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.parameter_box.currentIndexChanged.disconnect()
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            pass
        elif category == "relations":
            if old_name is not None and new_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(
                    self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                if parameterText == old_name:
                    self.content.parameter_box.setCurrentText(new_name)
                else:
                    self.content.parameter_box.setCurrentText(parameterText)
            elif old_name is not None:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(
                    self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                if parameterText != old_name:
                    self.content.parameter_box.setCurrentText(parameterText)
            else:
                parameterText = self.content.parameter_box.currentText()
                self.content.parameter_box.clear()

                self.content.parameter_box.addItems(
                    self.accessDicts.getDictionaryWithoutTransformation("relations").keys())

                self.content.parameter_box.setCurrentText(parameterText)
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.parameter_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def addRelation(self):
        input_set_name = self.content.input_box.currentText()
        output_set_name = self.content.output_box.currentText()
        input_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[input_set_name]
        output_set = self.accessDicts.getDictionaryWithoutTransformation("sets")[output_set_name]

        if input_set_name != "" and output_set_name != "" and len(input_set) > 0 and len(output_set) > 0:

            new_relation_name = "new relation"
            counter = 1
            while True:
                if new_relation_name + str(counter) not in self.accessDicts.getDictionaryWithoutTransformation("relations").keys():
                    new_relation_name = new_relation_name + str(counter)
                    break
                counter += 1

            new_relation = FPTRelation(new_relation_name, set(), input_set_name, output_set_name)
            self.accessDicts.addElementToDictionary("relations", new_relation_name, new_relation)
            pop = QDMContentListWidgetRelationPopup(new_relation)

            if pop.exec():
                if new_relation_name != pop.relation.name:
                    self.accessDicts.deleteElementFromDictionary("relations", new_relation_name)
                self.accessDicts.addElementToDictionary("relations", pop.relation.name, pop.relation)

                for subwnd in self.scene.node_editor_widget.window.mdiArea.subWindowList():
                    for node in subwnd.widget().scene.nodes:
                        node.onDictChanged("relations", new_name=pop.relation.name)
                    for node in subwnd.widget().scene.nodes:
                        node.eval()

                self.scene.node_editor_widget.window.content_changed = True

                self.content.parameter_box.setCurrentText(pop.relation.name)
            else:
                self.accessDicts.deleteElementFromDictionary("relations", new_relation_name)

            QDMContentWidget.reconnectAllDictionaries()

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "max"
        dict_of_relations = self.accessDicts.getDictionary("relations")
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = max(dict_of_relations.get(self.content.parameter_box.currentText()),
                            dict_of_sets.get(self.content.input_box.currentText()),
                            dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = max_hash(dict_of_relations.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = max_iota(dict_of_relations.get(self.content.parameter_box.currentText()),
                                      dict_of_sets.get(self.content.input_box.currentText()),
                                      dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("MAXIMUM - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("MAXIMUM - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("MAXIMUM - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_AVERAGE)
class FPTNode_Average(FPTNode):
    icon = "fixpointtool/icons/average.png"
    op_code = OP_CODE_AVERAGE
    op_title = "Average"
    content_label = "av"
    content_label_objname = "fpt_node_average"

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionAverageContent(self)

        self.fillComboBoxes()

        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

        self.grNode = FPTGraphicsAverageNode(self)

    def fillComboBoxes(self):
        self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

    def onDictChanged(self, category, old_name=None, new_name=None):
        self.content.input_box.currentIndexChanged.disconnect()
        self.content.output_box.currentIndexChanged.disconnect()
        if category == "mappings":
            pass
        elif category == "relations":
            pass
        elif category == "sets":
            if old_name is not None and new_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText == old_name:
                    self.content.input_box.setCurrentText(new_name)
                else:
                    self.content.input_box.setCurrentText(inputText)
                if outputText == old_name:
                    self.content.output_box.setCurrentText(new_name)
                else:
                    self.content.output_box.setCurrentText(outputText)
            elif old_name is not None:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                if inputText != old_name:
                    self.content.input_box.setCurrentText(inputText)
                if outputText != old_name:
                    self.content.output_box.setCurrentText(outputText)
            else:
                inputText = self.content.input_box.currentText()
                outputText = self.content.output_box.currentText()
                self.content.input_box.clear()
                self.content.output_box.clear()

                self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
                self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())

                self.content.input_box.setCurrentText(inputText)
                self.content.output_box.setCurrentText(outputText)
        else:
            print("WARNING: onDictChanged() has been used incorrectly")
        self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        self.content.output_box.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")

        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)
        self.value = "av"
        dict_of_sets = self.accessDicts.getDictionary("sets")
        self.function = av(dict_of_sets.get(self.content.input_box.currentText()),
                           dict_of_sets.get(self.content.output_box.currentText()))
        self.hash_function = av_hash(dict_of_sets.get(self.content.input_box.currentText()),
                                     dict_of_sets.get(self.content.output_box.currentText()))
        self.iota_function = av_iota(dict_of_sets.get(self.content.input_box.currentText()),
                                     dict_of_sets.get(self.content.output_box.currentText()))

        if len(output_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Output is not connected")
            if DEBUG: print("AVERAGE - EVALUATION DONE")
            return self.value
        if len(input_nodes) == 1:
            self.value += " \u2218 " + input_nodes[0].eval()
            try:
                self.function = composition(self.function, input_nodes[0].function)
                self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
            except IncompatibleSetsError as e:
                self.markInvalid()
                self.grNode.setToolTip("Input set does not match the given set")
                if DEBUG: print("AVERAGE - EVALUATION DONE")
                return self.value
        if len(input_nodes) > 1:
            self.value += " \u2218 ("
            if len(input_nodes[0].getInputs(0)) > 0:
                self.value += "(" + input_nodes[0].eval() + ")"
            else:
                self.value += input_nodes[0].eval()
            for connected_node in input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()
            self.value += ")"
            input_functions = []
            input_hash_functions = []
            input_iota_functions = []
            for node in input_nodes:
                input_functions.append(node.function)
                input_hash_functions.append(node.hash_function)
                input_iota_functions.append(node.iota_function)
            try:
                self.function = composition(self.function, disjoint_union(*input_functions))
                self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Input sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Input set does not match the given set")
                self.markInvalid()

        if DEBUG: print("AVERAGE - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_HIGHER_ORDER_FUNCTION)
class FPTNode_Higher_Order_Function(FPTNode):
    icon = "fixpointtool/icons/higher_order_function.png"
    op_code = OP_CODE_HIGHER_ORDER_FUNCTION
    op_title = "Higher-Order Function"
    content_label = ""
    content_label_objname = "fpt_node_higher_order_function"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], additional=[1])

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTFunctionHigherOrderFunctionContent(self)
        self.grNode = FPTGraphicsHigherOrderFunctionNode(self)

    def onDictChanged(self, category, old_name=None, new_name=None):
        # self.content.input_box.currentIndexChanged.disconnect()
        # self.content.output_box.currentIndexChanged.disconnect()
        # if category == "functions":
        #     pass
        # elif category == "relations":
        #     pass
        # elif category == "sets":
        #     if old_name is not None and new_name is not None:
        #         inputText = self.content.input_box.currentText()
        #         outputText = self.content.output_box.currentText()
        #         self.content.input_box.clear()
        #         self.content.output_box.clear()
        #
        #         self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #         self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #
        #         if inputText == old_name:
        #             self.content.input_box.setCurrentText(new_name)
        #         else:
        #             self.content.input_box.setCurrentText(inputText)
        #         if outputText == old_name:
        #             self.content.output_box.setCurrentText(new_name)
        #         else:
        #             self.content.output_box.setCurrentText(outputText)
        #     elif old_name is not None:
        #         inputText = self.content.input_box.currentText()
        #         outputText = self.content.output_box.currentText()
        #         self.content.input_box.clear()
        #         self.content.output_box.clear()
        #
        #         self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #         self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #
        #         if inputText != old_name:
        #             self.content.input_box.setCurrentText(inputText)
        #         if outputText != old_name:
        #             self.content.output_box.setCurrentText(outputText)
        #     else:
        #         inputText = self.content.input_box.currentText()
        #         outputText = self.content.output_box.currentText()
        #         self.content.input_box.clear()
        #         self.content.output_box.clear()
        #
        #         self.content.input_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #         self.content.output_box.addItems(self.accessDicts.getDictionaryWithoutTransformation("sets").keys())
        #
        #         self.content.input_box.setCurrentText(inputText)
        #         self.content.output_box.setCurrentText(outputText)
        # else:
        #     print("WARNING: onDictChanged() has been used incorrectly")
        # self.content.input_box.currentIndexChanged.connect(self.onInputChanged)
        # self.content.output_box.currentIndexChanged.connect(self.onInputChanged)
        pass

    def evalImplementation(self):
        # reset flags and tooltips
        self.markInvalid(False)
        self.grNode.setToolTip("")
        font = QFont("ubuntu", 20)
        fm = QFontMetrics(font)

        self.content.function_label.setText("f(a)")

        # update width of grNode and socket/edge position
        self.grNode.width = 240
        self.grNode.update()
        for socket in (self.outputs + self.additional):
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

        higher_order_function_input_nodes = self.getAdditional(0)
        input_nodes = self.getInputs(0)
        output_nodes = self.getOutputs(0)

        if len(higher_order_function_input_nodes) == 0:
            self.markInvalid()
            self.grNode.setToolTip("Higher-Order Function is not connected")
            if DEBUG: print("HIGHER-ORDER FUNCTION - EVALUATION DONE")
            return self.value
        elif len(higher_order_function_input_nodes) == 1:
            self.value = higher_order_function_input_nodes[0].eval()
            self.function = higher_order_function_input_nodes[0].function
            self.hash_function = higher_order_function_input_nodes[0].hash_function
            self.iota_function = higher_order_function_input_nodes[0].iota_function
        elif len(higher_order_function_input_nodes) > 1:
            if len(higher_order_function_input_nodes[0].getInputs(0)) > 0:
                self.value = "(" + higher_order_function_input_nodes[0].eval() + ")"
            else:
                self.value = higher_order_function_input_nodes[0].eval()
            for connected_node in higher_order_function_input_nodes[1:]:
                if len(connected_node.getInputs(0)) > 0:
                    self.value += " \u228E (" + connected_node.eval() + ")"
                else:
                    self.value += " \u228E " + connected_node.eval()

            higher_order_function_input_functions = []
            higher_order_function_input_hash_functions = []
            higher_order_function_input_iota_functions = []
            for node in higher_order_function_input_nodes:
                higher_order_function_input_functions.append(node.function)
                higher_order_function_input_hash_functions.append(node.hash_function)
                higher_order_function_input_iota_functions.append(node.iota_function)
            try:
                self.function = disjoint_union(*higher_order_function_input_functions)
                self.hash_function = disjoint_union_hash(*higher_order_function_input_hash_functions)
                self.iota_function = disjoint_union_iota(*higher_order_function_input_iota_functions)
            except IncompatibleFunctionsError:
                self.grNode.setToolTip("Higher-Order Function output sets are not disjoint")
                self.markInvalid()
            except IncompatibleSetsError:
                self.grNode.setToolTip("Higher-Order Function output set does not match the given set")
                self.markInvalid()

        self.content.function_label.setText("f(a) = " + self.value)

        # update width of grNode and socket/edge position
        if fm.width(self.content.function_label.text()) >= 220:
            self.grNode.width = fm.width(self.content.function_label.text()) + 20
        else:
            self.grNode.width = 240
        self.grNode.update()
        for socket in (self.outputs + self.additional):
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

        if not self.isInvalid():
            if len(output_nodes) == 0:
                self.markInvalid()
                self.grNode.setToolTip("Output is not connected")
                if DEBUG: print("HIGHER-ORDER FUNCTION - EVALUATION DONE")
                return self.value
            if len(input_nodes) == 1:
                self.value = "(" + self.value + ")" + " \u2218 " + input_nodes[0].eval()
                try:
                    self.function = composition(self.function, input_nodes[0].function)
                    self.hash_function = composition_hash(self.hash_function, input_nodes[0].hash_function)
                    self.iota_function = composition_iota(self.iota_function, input_nodes[0].iota_function)
                except IncompatibleSetsError as e:
                    self.markInvalid()
                    self.grNode.setToolTip("Input set does not match the given set")
                    if DEBUG: print("HIGHER-ORDER FUNCTION - EVALUATION DONE")
                    return self.value
            if len(input_nodes) > 1:
                self.value = "(" + self.value + ")" + " \u2218 ("
                if len(input_nodes[0].getInputs(0)) > 0:
                    self.value += "(" + input_nodes[0].eval() + ")"
                else:
                    self.value += input_nodes[0].eval()
                for connected_node in input_nodes[1:]:
                    if len(connected_node.getInputs(0)) > 0:
                        self.value += " \u228E (" + connected_node.eval() + ")"
                    else:
                        self.value += " \u228E " + connected_node.eval()
                self.value += ")"
                input_functions = []
                input_hash_functions = []
                input_iota_functions = []
                for node in input_nodes:
                    input_functions.append(node.function)
                    input_hash_functions.append(node.hash_function)
                    input_iota_functions.append(node.iota_function)
                try:
                    self.function = composition(self.function, disjoint_union(*input_functions))
                    self.hash_function = composition_hash(self.hash_function, disjoint_union_hash(*input_hash_functions))
                    self.iota_function = composition_iota(self.iota_function, disjoint_union_iota(*input_iota_functions))
                except IncompatibleFunctionsError:
                    self.grNode.setToolTip("Input sets are not disjoint")
                    self.markInvalid()
                except IncompatibleSetsError:
                    self.grNode.setToolTip("Input set does not match the given set")
                    self.markInvalid()

        if DEBUG: print("HIGHER-ORDER FUNCTION - EVALUATION DONE")
        return self.value


@register_node(OP_CODE_SEPARATOR)
class FPTSeparator:
    icon = ""
    op_code = OP_CODE_SEPARATOR
    op_title = "SEPARATOR"
