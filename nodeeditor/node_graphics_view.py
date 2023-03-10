from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.node_graphics_edge import QDMGraphicsEdge
from nodeeditor.node_edge_dragging import EdgeDragging
from nodeeditor.node_graphics_cutline import QDMCutLine
from nodeeditor.utils import dumpException


MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 50

DEBUG = False


class QDMGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False

        # edge dragging
        self.dragging = EdgeDragging(self)

        # cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

        self.last_scene_mouse_position = QPoint(0, 0)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 8
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # listeners
        self._drag_enter_listeners = []
        self._drop_listeners = []

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        # enable dropping
        self.setAcceptDrops(True)

    def resetMode(self):
        self.mode = MODE_NOOP

    def dragEnterEvent(self, event):
        for callback in self._drag_enter_listeners: callback(event)

    def dropEvent(self, event):
        for callback in self._drop_listeners: callback(event)

    def addDragEnterListener(self, callback):
        self._drag_enter_listeners.append(callback)

    def addDropListener(self, callback):
        self._drop_listeners.append(callback)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):

        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): print("RMB DEBUG:", item.edge, "connecting sockets:",
                                                        item.edge.start_socket, "<-->", item.edge.end_socket)
            if type(item) is QDMGraphicsSocket: print("RMB DEBUG:", item.socket, "has edges:", item.socket.edges)

            if item is None:
                print("SCENE:")
                print("  Nodes:")
                for node in self.grScene.scene.nodes: print("    ", node)
                print("  Edges:")
                for edge in self.grScene.scene.edges: print("    ", edge)

        # faking events to enable MMB dragging the scene
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):
        # get item which is clicked on
        item = self.getItemAtClick(event)

        # store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if DEBUG: print("LMB Click on", item, self.debug_modifiers(event))

        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if isinstance(item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.dragging.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.dragging.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubberBandDraggingRectangle = True

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which is at the position where LMB got released
        item = self.getItemAtClick(event)

        try:
            # logic
            if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
                if event.modifiers() & Qt.ShiftModifier:
                    event.ignore()
                    fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                            Qt.LeftButton, Qt.NoButton,
                                            event.modifiers() | Qt.ControlModifier)
                    super().mouseReleaseEvent(fakeEvent)
                    return

            if self.mode == MODE_EDGE_DRAG:
                if self.distanceBetweenClickAndReleaseIsOff(event):
                    res = self.dragging.edgeDragEnd(item)
                    if res: return

            if self.mode == MODE_EDGE_CUT:
                self.cutIntersectingEdges()
                self.cutline.line_points = []
                self.cutline.update()
                QApplication.setOverrideCursor(Qt.ArrowCursor)
                self.mode = MODE_NOOP
                return

            if self.rubberBandDraggingRectangle:
                self.rubberBandDraggingRectangle = False
                current_selected_items = self.grScene.selectedItems()

                if current_selected_items != self.grScene.scene._last_selected_items:
                    if current_selected_items == []:
                        self.grScene.itemsDeselected.emit()
                    else:
                        self.grScene.itemSelected.emit()
                    self.grScene.scene._last_selected_items = current_selected_items

                # hacky fix to stop rubber band drag immediately
                self.setDragMode(QGraphicsView.ScrollHandDrag)
                self.setDragMode(QGraphicsView.RubberBandDrag)

                return

            # otherwise deselect everything
            if item is None:
                self.grScene.itemsDeselected.emit()

        except Exception as e: dumpException(e)

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        scenepos = self.mapToScene(event.pos())

        if self.mode == MODE_EDGE_DRAG:
            self.dragging.updateDestination(scenepos.x(), scenepos.y())

        if self.mode == MODE_EDGE_CUT and self.cutline is not None:
            self.cutline.line_points.append(scenepos)
            self.cutline.update()

        self.last_scene_mouse_position = scenepos

        self.scenePosChanged.emit(
            int(scenepos.x()),
            int(scenepos.y())
        )

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Delete:
        #     if not self.editingFlag:
        #         self.deleteSelected()
        #     else:
        #         super().keyPressEvent(event)
        # elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.saveToFile("graph.json.txt")
        # elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.loadFromFile("graph.json.txt")
        # elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
        #     self.grScene.scene.history.undo()
        # elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
        #     self.grScene.scene.history.redo()
        # elif event.key() == Qt.Key_H:
        #     print("HISTORY:     len(%d)" % len(self.grScene.scene.history.history_stack),
        #           "  --  current_step", self.grScene.scene.history.history_current_step)
        #     ix = 0
        #     for item in self.grScene.scene.history.history_stack:
        #         print("#", ix, "--", item['desc'])
        #         ix += 1
        # else:
        super().keyPressEvent(event)

    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()
        self.grScene.scene.history.storeHistory("Delete cutted edges", setModified=True)

    def deleteSelected(self):
        try:
            while len(self.grScene.selectedItems()) > 0:
                item = self.grScene.selectedItems()[0]
                if isinstance(item, QDMGraphicsEdge):
                    item.edge.remove()
                elif hasattr(item, "node"):
                    item.node.remove()
            # for item in self.grScene.selectedItems():
            #     if isinstance(item, QDMGraphicsEdge):
            #         item.edge.remove()
            #     elif hasattr(item, "node"):
            #         item.node.remove()
            self.grScene.scene.history.storeHistory("Delete selected", setModified=True)
        except Exception as e:
            print(e)

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out

    # return the object which is clicked on
    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    # measures if the mouse is too far from the last LMB click scene position
    def distanceBetweenClickAndReleaseIsOff(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):
        # calculate zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
