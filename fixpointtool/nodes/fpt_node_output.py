from fixpointtool.content.fpt_content_listWidget_mapping_popup import QDMContentListWidgetMappingPopup
from fixpointtool.content.fpt_content_widget import QDMContentWidget
from fixpointtool.fpt_conf import *
import fixpointtool.fpt_conf
from fixpointtool.fpt_node_base import *
from fixpointtool.functions.fpt_functions import *
from fixpointtool.content.fpt_content import *

DEBUG = False


class FPTOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.information_label = QLabel("Function:")
        self.function_label = QLabel("f(a)")
        self.test_function_label = QLabel("Check for fixpoint:")
        self.computed_function_label = QLabel("Fixpoint: ?\nPre-Fixpoint: ?\nPost-Fixpoint: ?")
        self.test_hash_function_label = QLabel("Check for least/greatest fixpoint:")
        self.check_for_gfp_and_lfp_label = QLabel("least Fixpoint: ?\ngreatest Fixpoint: ?")
        self.test_star_function_label_pre = QLabel("Check for \u03bdf \u2291 a:")
        self.test_star_function_label_post = QLabel("Check for a \u2291 \u03bcf:")
        self.star_function_results_pre = QLabel("-")
        self.star_function_results_post = QLabel("-")
        self.compute_iota_label = QLabel("Compute iota:")
        self.compute_iota_results = QLabel("-")

        self.information_label.setObjectName(self.node.content_label_objname + "1")
        self.function_label.setObjectName(self.node.content_label_objname + "2")
        self.test_function_label.setObjectName(self.node.content_label_objname + "3")
        self.computed_function_label.setObjectName(self.node.content_label_objname + "5")
        self.test_hash_function_label.setObjectName(self.node.content_label_objname + "4")
        self.check_for_gfp_and_lfp_label.setObjectName(self.node.content_label_objname + "6")
        self.test_star_function_label_pre.setObjectName(self.node.content_label_objname + "7")
        self.star_function_results_pre.setObjectName(self.node.content_label_objname + "8")
        self.test_star_function_label_post.setObjectName(self.node.content_label_objname + "9")
        self.star_function_results_post.setObjectName(self.node.content_label_objname + "10")
        self.compute_iota_label.setObjectName(self.node.content_label_objname + "11")
        self.compute_iota_results.setObjectName(self.node.content_label_objname + "12")

        self.fixpoint_box = QComboBox()
        self.compute_function_button = QPushButton("Compute")
        self.compute_iota_button = QPushButton("Compute")
        self.iota_case_box = QComboBox()
        self.check_for_gfp_and_lfp_button = QPushButton("Compute")
        self.test_star_function_button_pre = QPushButton("Compute")
        self.test_star_function_button_post = QPushButton("Compute")
        self.fixpoint_box.setFixedWidth(181)
        self.compute_function_button.setFixedWidth(218)
        self.compute_iota_button.setFixedWidth(218)
        self.iota_case_box.setFixedWidth(218)
        self.check_for_gfp_and_lfp_button.setFixedWidth(218)
        self.test_star_function_button_pre.setFixedWidth(218)
        self.test_star_function_button_post.setFixedWidth(218)

        self.parameter_add = QPushButton("+")
        self.parameter_add.setMaximumWidth(30)

        sp_retain = self.test_hash_function_label.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.test_hash_function_label.setSizePolicy(sp_retain)

        sp_retain = self.check_for_gfp_and_lfp_button.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.check_for_gfp_and_lfp_button.setSizePolicy(sp_retain)

        sp_retain = self.check_for_gfp_and_lfp_label.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.check_for_gfp_and_lfp_label.setSizePolicy(sp_retain)

        sp_retain = self.test_star_function_label_pre.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.test_star_function_label_pre.setSizePolicy(sp_retain)

        sp_retain = self.star_function_results_pre.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.star_function_results_pre.setSizePolicy(sp_retain)

        sp_retain = self.test_star_function_button_pre.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.test_star_function_button_pre.setSizePolicy(sp_retain)

        sp_retain = self.test_star_function_label_post.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.test_star_function_label_post.setSizePolicy(sp_retain)

        sp_retain = self.star_function_results_post.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.star_function_results_post.setSizePolicy(sp_retain)

        sp_retain = self.test_star_function_button_post.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.test_star_function_button_post.setSizePolicy(sp_retain)

        sp_retain = self.compute_iota_label.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.compute_iota_label.setSizePolicy(sp_retain)

        sp_retain = self.compute_iota_results.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.compute_iota_results.setSizePolicy(sp_retain)

        sp_retain = self.compute_iota_button.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.compute_iota_button.setSizePolicy(sp_retain)

        sp_retain = self.iota_case_box.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.iota_case_box.setSizePolicy(sp_retain)

        self.function_label.setContentsMargins(0, 0, 0, 10)
        self.computed_function_label.setContentsMargins(0, 10, 0, 10)
        self.check_for_gfp_and_lfp_label.setContentsMargins(0, 10, 0, 10)
        self.star_function_results_pre.setContentsMargins(0, 10, 0, 10)
        self.star_function_results_post.setContentsMargins(0, 10, 0, 10)

        self.spacer = QWidget()
        sp = self.spacer.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.spacer.setSizePolicy(sp)

        self.fixpoint_hbox = QHBoxLayout()
        self.fixpoint_hbox.addWidget(self.fixpoint_box, alignment=Qt.AlignLeft)
        self.fixpoint_hbox.addWidget(self.parameter_add, alignment=Qt.AlignLeft)
        self.fixpoint_hbox.addWidget(self.spacer)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.information_label)
        self.vbox.addWidget(self.function_label)
        self.vbox.addWidget(self.test_function_label)
        self.vbox.addLayout(self.fixpoint_hbox)
        self.vbox.addWidget(self.compute_function_button)
        self.vbox.addWidget(self.computed_function_label)
        self.vbox.addWidget(self.test_hash_function_label)
        self.vbox.addWidget(self.check_for_gfp_and_lfp_button)
        self.vbox.addWidget(self.check_for_gfp_and_lfp_label)
        self.vbox.addWidget(self.compute_iota_label)
        self.vbox.addWidget(self.iota_case_box)
        self.vbox.addWidget(self.compute_iota_button)
        self.vbox.addWidget(self.compute_iota_results)
        self.vbox.addWidget(self.test_star_function_label_pre)
        self.vbox.addWidget(self.test_star_function_button_pre)
        self.vbox.addWidget(self.star_function_results_pre)
        self.vbox.addWidget(self.test_star_function_label_post)
        self.vbox.addWidget(self.test_star_function_button_post)
        self.vbox.addWidget(self.star_function_results_post)

        # self.vbox.addWidget(self.test_function_button)
        # self.vbox.addWidget(self.fixpoint_type_box)

        self.setLayout(self.vbox)

    def serialize(self):
        res = super().serialize()
        res['fixpoint_box'] = self.fixpoint_box.currentText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            name1 = data['fixpoint_box']
            self.fixpoint_box.setCurrentText(name1)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_CODE_TESTING)
class FPTNode_Output(FPTNode):
    icon = "fixpointtool/icons/testing.png"
    op_code = OP_CODE_TESTING
    op_title = "Testing"
    content_label_objname = "fpt_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def startLayout(self, initial=False):
        self.grNode.height = 280  # old: 280
        self.grNode.update()

        self.content.test_hash_function_label.setVisible(False)
        self.content.check_for_gfp_and_lfp_button.setVisible(False)
        self.content.check_for_gfp_and_lfp_label.setVisible(False)
        self.content.compute_iota_label.setVisible(False)
        self.content.compute_iota_button.setVisible(False)
        self.content.iota_case_box.setVisible(False)
        self.content.compute_iota_results.setVisible(False)
        self.content.test_star_function_label_pre.setVisible(False)
        self.content.test_star_function_button_pre.setVisible(False)
        self.content.star_function_results_pre.setVisible(False)
        self.content.test_star_function_label_post.setVisible(False)
        self.content.test_star_function_button_post.setVisible(False)
        self.content.star_function_results_post.setVisible(False)

        self.content.test_hash_function_label.setGeometry(QRect(0,0,0,0))
        self.content.check_for_gfp_and_lfp_button.setGeometry(QRect(0,0,0,0))
        self.content.check_for_gfp_and_lfp_label.setGeometry(QRect(0,0,0,0))
        self.content.compute_iota_label.setGeometry(QRect(0,0,0,0))
        self.content.compute_iota_button.setGeometry(QRect(0,0,0,0))
        self.content.iota_case_box.setGeometry(QRect(0,0,0,0))
        self.content.compute_iota_results.setGeometry(QRect(0,0,0,0))
        self.content.test_star_function_label_pre.setGeometry(QRect(0,0,0,0))
        self.content.test_star_function_button_pre.setGeometry(QRect(0,0,0,0))
        self.content.star_function_results_pre.setGeometry(QRect(0,0,0,0))
        self.content.test_star_function_label_post.setGeometry(QRect(0,0,0,0))
        self.content.test_star_function_button_post.setGeometry(QRect(0,0,0,0))
        self.content.star_function_results_post.setGeometry(QRect(0,0,0,0))

        if not initial:
            self.grNode.update()
            for socket in self.inputs:
                socket.setSocketPosition()
                for edge in socket.edges:
                    edge.updatePositions()

    def fixpointLayout(self):
        self.grNode.height = 410  # old: 410
        self.grNode.update()

        self.content.vbox.removeWidget(self.content.test_star_function_label_pre)
        self.content.vbox.removeWidget(self.content.test_star_function_button_pre)
        self.content.vbox.removeWidget(self.content.star_function_results_pre)
        self.content.vbox.removeWidget(self.content.test_star_function_label_post)
        self.content.vbox.removeWidget(self.content.test_star_function_button_post)
        self.content.vbox.removeWidget(self.content.star_function_results_post)
        self.content.vbox.removeWidget(self.content.compute_iota_label)
        self.content.vbox.removeWidget(self.content.iota_case_box)
        self.content.vbox.removeWidget(self.content.compute_iota_button)
        self.content.vbox.removeWidget(self.content.compute_iota_results)
        self.content.vbox.addWidget(self.content.test_star_function_label_pre)
        self.content.vbox.addWidget(self.content.test_star_function_button_pre)
        self.content.vbox.addWidget(self.content.star_function_results_pre)
        self.content.vbox.addWidget(self.content.test_star_function_label_post)
        self.content.vbox.addWidget(self.content.test_star_function_button_post)
        self.content.vbox.addWidget(self.content.star_function_results_post)
        self.content.vbox.addWidget(self.content.compute_iota_label)
        self.content.vbox.addWidget(self.content.iota_case_box)
        self.content.vbox.addWidget(self.content.compute_iota_button)
        self.content.vbox.addWidget(self.content.compute_iota_results)

        self.content.test_hash_function_label.setVisible(True)
        self.content.check_for_gfp_and_lfp_button.setVisible(True)
        self.content.check_for_gfp_and_lfp_label.setVisible(True)
        self.content.compute_iota_label.setVisible(False)
        self.content.compute_iota_button.setVisible(False)
        self.content.iota_case_box.setVisible(False)
        self.content.compute_iota_results.setVisible(False)
        self.content.test_star_function_label_pre.setVisible(False)
        self.content.test_star_function_button_pre.setVisible(False)
        self.content.star_function_results_pre.setVisible(False)
        self.content.test_star_function_label_post.setVisible(False)
        self.content.test_star_function_button_post.setVisible(False)
        self.content.star_function_results_post.setVisible(False)

        self.grNode.update()
        for socket in self.inputs:
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

    def prefixpointLayout(self):
        self.grNode.height = 390  # old: 390
        self.grNode.update()

        self.content.vbox.removeWidget(self.content.test_hash_function_label)
        self.content.vbox.removeWidget(self.content.check_for_gfp_and_lfp_button)
        self.content.vbox.removeWidget(self.content.check_for_gfp_and_lfp_label)
        self.content.vbox.removeWidget(self.content.test_star_function_label_post)
        self.content.vbox.removeWidget(self.content.test_star_function_button_post)
        self.content.vbox.removeWidget(self.content.star_function_results_post)
        self.content.vbox.removeWidget(self.content.compute_iota_label)
        self.content.vbox.removeWidget(self.content.iota_case_box)
        self.content.vbox.removeWidget(self.content.compute_iota_button)
        self.content.vbox.removeWidget(self.content.compute_iota_results)
        self.content.vbox.addWidget(self.content.test_hash_function_label)
        self.content.vbox.addWidget(self.content.check_for_gfp_and_lfp_button)
        self.content.vbox.addWidget(self.content.check_for_gfp_and_lfp_label)
        self.content.vbox.addWidget(self.content.test_star_function_label_post)
        self.content.vbox.addWidget(self.content.test_star_function_button_post)
        self.content.vbox.addWidget(self.content.star_function_results_post)
        self.content.vbox.addWidget(self.content.compute_iota_label)
        self.content.vbox.addWidget(self.content.iota_case_box)
        self.content.vbox.addWidget(self.content.compute_iota_button)
        self.content.vbox.addWidget(self.content.compute_iota_results)

        self.content.test_hash_function_label.setVisible(False)
        self.content.check_for_gfp_and_lfp_button.setVisible(False)
        self.content.check_for_gfp_and_lfp_label.setVisible(False)
        self.content.compute_iota_label.setVisible(False)
        self.content.compute_iota_button.setVisible(False)
        self.content.iota_case_box.setVisible(False)
        self.content.compute_iota_results.setVisible(False)
        self.content.test_star_function_label_pre.setVisible(True)
        self.content.test_star_function_button_pre.setVisible(True)
        self.content.star_function_results_pre.setVisible(True)
        self.content.test_star_function_label_post.setVisible(False)
        self.content.test_star_function_button_post.setVisible(False)
        self.content.star_function_results_post.setVisible(False)

        self.grNode.update()
        for socket in self.inputs:
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

    def postfixpointlayout(self):
        self.grNode.height = 390  # old: 390
        self.grNode.update()

        self.content.vbox.removeWidget(self.content.test_hash_function_label)
        self.content.vbox.removeWidget(self.content.check_for_gfp_and_lfp_button)
        self.content.vbox.removeWidget(self.content.check_for_gfp_and_lfp_label)
        self.content.vbox.removeWidget(self.content.test_star_function_label_pre)
        self.content.vbox.removeWidget(self.content.test_star_function_button_pre)
        self.content.vbox.removeWidget(self.content.star_function_results_pre)
        self.content.vbox.removeWidget(self.content.compute_iota_label)
        self.content.vbox.removeWidget(self.content.iota_case_box)
        self.content.vbox.removeWidget(self.content.compute_iota_button)
        self.content.vbox.removeWidget(self.content.compute_iota_results)
        self.content.vbox.addWidget(self.content.test_hash_function_label)
        self.content.vbox.addWidget(self.content.check_for_gfp_and_lfp_button)
        self.content.vbox.addWidget(self.content.check_for_gfp_and_lfp_label)
        self.content.vbox.addWidget(self.content.test_star_function_label_pre)
        self.content.vbox.addWidget(self.content.test_star_function_button_pre)
        self.content.vbox.addWidget(self.content.star_function_results_pre)
        self.content.vbox.addWidget(self.content.compute_iota_label)
        self.content.vbox.addWidget(self.content.iota_case_box)
        self.content.vbox.addWidget(self.content.compute_iota_button)
        self.content.vbox.addWidget(self.content.compute_iota_results)

        self.content.test_hash_function_label.setVisible(False)
        self.content.check_for_gfp_and_lfp_button.setVisible(False)
        self.content.check_for_gfp_and_lfp_label.setVisible(False)
        self.content.compute_iota_label.setVisible(False)
        self.content.compute_iota_button.setVisible(False)
        self.content.iota_case_box.setVisible(False)
        self.content.compute_iota_results.setVisible(False)
        self.content.test_star_function_label_pre.setVisible(False)
        self.content.test_star_function_button_pre.setVisible(False)
        self.content.star_function_results_pre.setVisible(False)
        self.content.test_star_function_label_post.setVisible(True)
        self.content.test_star_function_button_post.setVisible(True)
        self.content.star_function_results_post.setVisible(True)

        self.grNode.update()
        for socket in self.inputs:
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

    def iotaLayout(self):
        self.grNode.height = 540
        self.grNode.update()

        self.content.vbox.removeWidget(self.content.test_star_function_label_pre)
        self.content.vbox.removeWidget(self.content.test_star_function_button_pre)
        self.content.vbox.removeWidget(self.content.star_function_results_pre)
        self.content.vbox.removeWidget(self.content.test_star_function_label_post)
        self.content.vbox.removeWidget(self.content.test_star_function_button_post)
        self.content.vbox.removeWidget(self.content.star_function_results_post)
        self.content.vbox.removeWidget(self.content.compute_iota_label)
        self.content.vbox.removeWidget(self.content.iota_case_box)
        self.content.vbox.removeWidget(self.content.compute_iota_button)
        self.content.vbox.removeWidget(self.content.compute_iota_results)
        self.content.vbox.addWidget(self.content.compute_iota_label)
        self.content.vbox.addWidget(self.content.iota_case_box)
        self.content.vbox.addWidget(self.content.compute_iota_button)
        self.content.vbox.addWidget(self.content.compute_iota_results)
        self.content.vbox.addWidget(self.content.test_star_function_label_pre)
        self.content.vbox.addWidget(self.content.test_star_function_button_pre)
        self.content.vbox.addWidget(self.content.star_function_results_pre)
        self.content.vbox.addWidget(self.content.test_star_function_label_post)
        self.content.vbox.addWidget(self.content.test_star_function_button_post)
        self.content.vbox.addWidget(self.content.star_function_results_post)

        self.content.test_hash_function_label.setVisible(True)
        self.content.check_for_gfp_and_lfp_button.setVisible(True)
        self.content.check_for_gfp_and_lfp_label.setVisible(True)
        self.content.compute_iota_label.setVisible(True)
        self.content.compute_iota_button.setVisible(True)
        self.content.iota_case_box.setVisible(True)
        self.content.compute_iota_results.setVisible(True)
        self.content.test_star_function_label_pre.setVisible(False)
        self.content.test_star_function_button_pre.setVisible(False)
        self.content.star_function_results_pre.setVisible(False)
        self.content.test_star_function_label_post.setVisible(False)
        self.content.test_star_function_button_post.setVisible(False)
        self.content.star_function_results_post.setVisible(False)

        self.grNode.update()
        for socket in self.inputs:
            socket.setSocketPosition()
            for edge in socket.edges:
                edge.updatePositions()

    def initInnerClasses(self):
        self.accessDicts = AccessDictionaries()

        self.content = FPTOutputContent(self)
        self.grNode = FPTGraphicsNode(self)

        self.fillComboBoxes()

        self.content.fixpoint_box.currentTextChanged.connect(self.onTestFunctionChanged)
        self.content.compute_function_button.clicked.connect(self.onComputeFunctionButtonClicked)
        self.content.check_for_gfp_and_lfp_button.clicked.connect(self.checkForGFPAndLFP)
        self.content.test_star_function_button_pre.clicked.connect(self.onTestStarFunctionButtonPreClicked)
        self.content.test_star_function_button_post.clicked.connect(self.onTestStarFunctionButtonPostClicked)

        self.content.parameter_add.clicked.connect(self.addTestMapping)

        self.content.compute_iota_button.clicked.connect(self.computeIotaButtonClicked)
        self.content.iota_case_box.addItems(["primal", "dual"])
        self.content.iota_case_box.currentIndexChanged.connect(self.onIotaCaseChanged)

        # initialize width of grNode
        self.grNode.width = 160

        self.startLayout(initial=True)

    def fillComboBoxes(self):
        dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
        listOfAvailableFunctions = []
        for func in dictOfFunctions:
            if dictOfFunctions[func].mappingType == "testing" or dictOfFunctions[func].mappingType == "all":
                listOfAvailableFunctions.append(func)

        self.content.fixpoint_box.addItems(listOfAvailableFunctions)

    def onDictChanged(self, category, old_name=None, new_name=None):
        if category == "mappings":
            if old_name is not None and new_name is not None:
                startText = self.content.fixpoint_box.currentText()
                self.content.fixpoint_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "testing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.fixpoint_box.addItems(listOfAvailableFunctions)

                if startText == old_name:
                    self.content.fixpoint_box.setCurrentText(new_name)
                else:
                    self.content.fixpoint_box.setCurrentText(startText)
            elif old_name is not None:
                startText = self.content.fixpoint_box.currentText()
                self.content.fixpoint_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "testing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.fixpoint_box.addItems(listOfAvailableFunctions)

                if startText != old_name:
                    self.content.fixpoint_box.setCurrentText(startText)
            else:
                startText = self.content.fixpoint_box.currentText()
                self.content.fixpoint_box.clear()

                dictOfFunctions = self.accessDicts.getDictionaryWithoutTransformation("mappings")
                listOfAvailableFunctions = []
                for func in dictOfFunctions:
                    if dictOfFunctions[func].mappingType == "testing" or dictOfFunctions[func].mappingType == "all":
                        listOfAvailableFunctions.append(func)
                self.content.fixpoint_box.addItems(listOfAvailableFunctions)

                self.content.fixpoint_box.setCurrentText(startText)
        elif category == "relations":
            pass
        elif category == "sets":
            pass
        else:
            print("WARNING: onDictChanged() has been used incorrectly")

    def addTestMapping(self):
        startNodes = self.getStartNodes()
        input_names = []
        for node in startNodes:
            input_names.append(node.content.input_box.currentText())

        if len(input_names) > 1:
            input_set_name = "-"
        else:
            input_set_name = input_names[0]

        if input_set_name != "":
            config = ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

            new_mapping_name = FPTMapping.getNewMappingName()
            new_mapping = FPTMapping(new_mapping_name, [], "testing", input_set_name=input_set_name,
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

                if pop.mapping_type == "testing" or pop.mapping_type == "all":
                    self.content.fixpoint_box.setCurrentText(pop.func_name)

            else:
                self.accessDicts.deleteElementFromDictionary("mappings", new_mapping_name)
                FPTMapping.dictOfFPTMappings.pop(new_mapping_name)
                FPTMapping.dictOfMappings.pop(new_mapping_name)

            QDMContentWidget.reconnectAllDictionaries()

    def onTestFunctionChanged(self):
        self.content.computed_function_label.setText("Fixpoint: ?\nPre-Fixpoint: ?\nPost-Fixpoint: ?")
        self.content.check_for_gfp_and_lfp_label.setText("least Fixpoint: ?\ngreatest Fixpoint: ?")
        self.content.star_function_results_pre.setText("-")
        self.content.star_function_results_post.setText("-")
        self.content.compute_iota_results.setText("-")

        self.startLayout()

    def onTestStarFunctionButtonPreClicked(self):
        try:
            changeGFP("GFP")
            self.eval()

            # calculate potential values
            Y = self.hash_function[1]
            a = self.accessDicts.getDictionary("mappings").get(self.content.fixpoint_box.currentText())

            if fixpointtool.fpt_conf.GFP:
                pot_values = set([y for y in Y if a(y) != ALGEBRA.complement(ALGEBRA.e)])
            else:
                pot_values = set([y for y in Y if a(y) != ALGEBRA.e])

            # calculate star function
            f_a = self.function[0](a)
            f_hash = self.hash_function[0](a)

            narrowed_pot_values = set([x for x in pot_values if a(x) == f_a(x)])
            print()
            print(narrowed_pot_values)

            pot_values = narrowed_pot_values
            while pot_values != (f_hash(pot_values) & narrowed_pot_values):
                print(f_hash(pot_values) & narrowed_pot_values)
                pot_values = (f_hash(pot_values) & narrowed_pot_values)

            if not pot_values:
                self.content.star_function_results_pre.setText("\u03bdf \u2291 a")
            else:
                self.content.star_function_results_pre.setText("no implication possible")
        except Exception as e:
            dumpException(e)

    def onTestStarFunctionButtonPostClicked(self):
        try:
            changeGFP("LFP")
            self.eval()

            # calculate potential values
            Y = self.hash_function[1]
            a = self.accessDicts.getDictionary("mappings").get(self.content.fixpoint_box.currentText())

            if fixpointtool.fpt_conf.GFP:
                pot_values = set([y for y in Y if a(y) != ALGEBRA.complement(ALGEBRA.e)])
            else:
                pot_values = set([y for y in Y if a(y) != ALGEBRA.e])

            # calculate star function
            f_a = self.function[0](a)
            f_hash = self.hash_function[0](a)

            narrowed_pot_values = set([x for x in pot_values if a(x) == f_a(x)])
            print()
            print(narrowed_pot_values)

            pot_values = narrowed_pot_values
            while pot_values != (f_hash(pot_values) & narrowed_pot_values):
                print(f_hash(pot_values) & narrowed_pot_values)
                pot_values = (f_hash(pot_values) & narrowed_pot_values)

            if not pot_values:
                self.content.star_function_results_post.setText("a \u2291 \u03bcf")
            else:
                self.content.star_function_results_post.setText("a \u22e4 \u03bcf")
        except Exception as e:
            dumpException(e)

    def onComputeFunctionButtonClicked(self):
        try:
            self.eval()

            a = self.accessDicts.getDictionary("mappings").get(self.content.fixpoint_box.currentText())
            f_a = self.function[0](a)

            isFixpoint = True
            isPreFixpoint = True
            isPostFixpoint = True

            print()
            for val in self.function[1]:
                a_val = a(val)
                f_a_val = f_a(val)
                if fixpointtool.fpt_conf.ALGEBRA.neq(a_val, f_a_val):
                    isFixpoint = False
                if fixpointtool.fpt_conf.ALGEBRA.lt(a_val, f_a_val):
                    isPreFixpoint = False
                if fixpointtool.fpt_conf.ALGEBRA.gt(a_val, f_a_val):
                    isPostFixpoint = False

                print(val, a_val, f_a_val)

            self.content.computed_function_label.setText("Fixpoint: " + ("Yes" if isFixpoint else "No") +
                                                         "\nPre-Fixpoint: " + ("Yes" if isPreFixpoint else "No") +
                                                         "\nPost-Fixpoint: " + ("Yes" if isPostFixpoint else "No"))

            if isFixpoint:
                self.fixpointLayout()
            elif isPreFixpoint:
                self.prefixpointLayout()
            elif isPostFixpoint:
                self.postfixpointlayout()
            else:
                self.startLayout()

        except NotDefinedError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning:\nError while calculating\n"
                        "Sets possibly not matching defined mappings/relations")
            msg.exec()
            self.startLayout()
        except Exception as e:
            dumpException(e)

    def computeIotaButtonClicked(self):
        try:
            if self.content.iota_case_box.currentText() == "primal":
                changeGFP("GFP")
            else:
                changeGFP("LFP")
            self.eval()

            iota_a = self.iota_function[0](self.accessDicts.getDictionary("mappings").get(self.content.fixpoint_box.currentText()))
            self.content.compute_iota_results.setText(str(iota_a))

        except Exception as e:
            dumpException(e)

    def onIotaCaseChanged(self):
        self.content.compute_iota_results.setText("-")

    def checkForGFPAndLFP(self):
        try:
            isGFP = False
            isLFP = False

            for fixType in ["GFP", "LFP"]:
                print("\n", fixType)
                changeGFP(fixType)
                self.eval()

                # calculate potential values
                Y = self.hash_function[1]
                a = self.accessDicts.getDictionary("mappings").get(self.content.fixpoint_box.currentText())

                if fixpointtool.fpt_conf.GFP:
                    pot_values = set([y for y in Y if a(y) != ALGEBRA.complement(ALGEBRA.e)])
                else:
                    pot_values = set([y for y in Y if a(y) != ALGEBRA.e])
                print(pot_values)

                # calculate least/greatest fixpoint
                f_hash = self.hash_function[0](a)
                while pot_values != f_hash(pot_values):
                    print(f_hash(pot_values))
                    pot_values = f_hash(pot_values)

                if not pot_values:
                    if fixType == "GFP":
                        isGFP = True
                    else:
                        isLFP = True

            self.content.check_for_gfp_and_lfp_label.setText("least Fixpoint: " + ("Yes" if isLFP else "No") +
                                                             "\ngreatest Fixpoint: " + ("Yes" if isGFP else "No"))
            if (not isLFP) or (not isGFP):
                self.iotaLayout()
        except Exception as e:
            dumpException(e)

        # try:
        #     changeGFP(self.content.fixpoint_type_box.currentText())
        #     self.eval()
        #
        #     # calculate potential values
        #     Y = self.hash_function[1]
        #     a = self.accessDicts.getDictionary("functions").get(self.content.fixpoint_box.currentText())
        #
        #     if fixpointtool.fpt_conf.GFP:
        #         pot_values = set([y for y in Y if a(y) != ALGEBRA.complement(ALGEBRA.e)])
        #     else:
        #         pot_values = set([y for y in Y if a(y) != ALGEBRA.e])
        #     print("POTENTIAL VALUES: ", pot_values)
        #
        #     # calculate greatest/least fixpoint
        #     f_hash = self.hash_function[0](a)
        #     i = 1
        #     while pot_values != f_hash(pot_values):
        #         print(i, ". Schritt", f_hash(pot_values))
        #         i += 1
        #         pot_values = f_hash(pot_values)
        #     if self.content.fixpoint_type_box.currentText() == "GFP":
        #         print("GREATEST FIXPOINT: ", pot_values)
        #     else:
        #         print("LEAST FIXPOINT: ", pot_values)
        # except Exception as e:
        #     dumpException(e)

    def evalImplementation(self):
        try:
            # reset flags and tooltips
            self.grNode.setToolTip("")
            self.markDirty(False)
            self.markInvalid(False)

            input_nodes = self.getInputs(0)
            self.value = "f(a) ="
            font = QFont("ubuntu", 20)
            fm = QFontMetrics(font)

            if len(input_nodes) == 0:
                self.markInvalid()
                self.grNode.setToolTip("Input is not connected")
            if len(input_nodes) == 1:
                self.value += " " + input_nodes[0].eval()
                self.function = input_nodes[0].function
                self.hash_function = input_nodes[0].hash_function
                self.iota_function = input_nodes[0].iota_function
            if len(input_nodes) > 1:
                if len(input_nodes[0].getInputs(0)) > 0:
                    self.value += " (" + input_nodes[0].eval() + ")"
                else:
                    self.value += " " + input_nodes[0].eval()
                for connected_node in input_nodes[1:]:
                    if len(connected_node.getInputs(0)) > 0:
                        self.value += " \u228E (" + connected_node.eval() + ")"
                    else:
                        self.value += " \u228E " + connected_node.eval()
                input_functions = []
                input_hash_functions = []
                input_iota_functions = []
                for node in input_nodes:
                    input_functions.append(node.function)
                    input_hash_functions.append(node.hash_function)
                    input_iota_functions.append(node.iota_function)
                try:
                    self.function = disjoint_union(*input_functions)
                    self.hash_function = disjoint_union_hash(*input_hash_functions)
                    self.iota_function = disjoint_union_iota(*input_iota_functions)
                except IncompatibleFunctionsError as e:
                    self.grNode.setToolTip("Input sets are not disjoint")
                    self.markInvalid()

            self.content.function_label.setText(self.value)

            # update width of grNode
            if fm.width(self.content.function_label.text()) >= 220:
                self.grNode.width = fm.width(self.content.function_label.text()) + 20
            else:
                self.grNode.width = 240
            self.grNode.update()

            is_valid = self.nodeIsValid()
            if not is_valid and not self.isInvalid():
                self.grNode.setToolTip("Fix all errors before testing the function")
                self.markDirty(True)
            self.content.compute_function_button.setDisabled(not is_valid)
            self.content.compute_iota_button.setDisabled(not is_valid)
            self.content.check_for_gfp_and_lfp_button.setDisabled(not is_valid)
            self.content.parameter_add.setDisabled(not is_valid)

            if DEBUG: print("TESTING - EVALUATION DONE")
            return self.value
        except TypeError as e:
            print("WARNING: TypeError")
        except Exception as e:
            dumpException(e)
