from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER, BOTTOM
from nodeeditor.utils import dumpException

DEBUG = False


class FPTGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 240  # 160 before
        self.height = 300  # 260 before
        self.edge_roundness = 5
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("fixpointtool/icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class FPTGraphicsHigherOrderFunctionNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 240
        self.height = 100
        self.edge_roundness = 5
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("fixpointtool/icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class FPTGraphicsFunctionNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 220  # old: 160
        self.height = 220
        self.edge_roundness = 5
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("fixpointtool/icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class FPTGraphicsAverageNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 220  # old: 160
        self.height = 160
        self.edge_roundness = 5
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("fixpointtool/icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class FPTNodeContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class FPTNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "fpt_node_bg"

    def __init__(self, scene, inputs=[2], outputs=[2], additional=[]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs, additional)

        self.value = None
        self.function = None
        self.hash_function = None

        self.markInvalid()
        self.eval()

    def initInnerClasses(self):
        self.content = FPTNodeContent(self)
        self.grNode = FPTGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER
        self.additional_socket_position = BOTTOM
        self.input_multi_edged = True
        self.output_multi_edged = True  # allows splitting up outputs
        self.additional_multi_edged = True

    def evalImplementation(self):
        return ""  # default value

    def eval(self):
        try:
            val = self.evalImplementation()
            return val
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def onEdgeConnectionChanged(self, new_edge):
        # print("%s::__onEdgeConnectionChanged" %  self.__class__.__name__, new_edge)
        # TODO: Prevent double check
        self.markInvalid()
        self.eval()
        self.evalDescendants()

    def onInputChanged(self, socket=None):
        # print("%s::__onInputChanged" % self.__class__.__name__, socket)
        self.eval()
        self.evalDescendants()

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        if DEBUG: print("Deserialized FPTNode '%s'" % self.__class__.__name__, "res:", res)
        return res
