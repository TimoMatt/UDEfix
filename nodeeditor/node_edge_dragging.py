from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.node_edge import Edge, EDGE_TYPE_BEZIER
from nodeeditor.utils import dumpException

DEBUG = False


class EdgeDragging:
    def __init__(self, grView):
        self.grView = grView

    def getEdgeClass(self):
        return self.grView.grScene.scene.getEdgeClass()

    def updateDestination(self, x, y):
        if self.drag_edge is not None and self.drag_edge.grEdge is not None:
            self.drag_edge.grEdge.setDestination(x, y)
            self.drag_edge.grEdge.update()
        else:
            print(">>> Want to update self.drag_edge grEdge, but it's None!")

    def edgeDragStart(self, item):
        try:
            if DEBUG: print("View::edgeDragStart ~ Start dragging edge")
            if DEBUG: print("View::edgeDragStart ~  assign Start Socket to:", item.socket)
            # self.previousEdge = item.socket.edge
            self.drag_start_socket = item.socket
            self.drag_edge = self.getEdgeClass()(item.socket.node.scene, item.socket, None, EDGE_TYPE_BEZIER)
            if DEBUG: print("View::edgeDragStart ~ dragEdge:", self.drag_edge)
        except Exception as e: dumpException(e)

    def edgeDragEnd(self, item):
        # return True if skip the rest of the code
        self.grView.resetMode()

        if DEBUG: print("View::edgeDragEnd ~ End dragging edge")
        self.drag_edge.remove(silent=True)
        self.drag_edge = None

        try:
            if isinstance(item, QDMGraphicsSocket):
                if (item.socket != self.drag_start_socket) and (item.socket.is_additional and self.drag_start_socket.is_output or item.socket.is_output and self.drag_start_socket.is_additional or item.socket.is_input and self.drag_start_socket.is_output or item.socket.is_output and self.drag_start_socket.is_input):
                    # first remove old edges/ send notifications
                    for socket in (item.socket, self.drag_start_socket):

                        if not socket.is_multi_edges:
                            if socket.is_input:
                                socket.removeAllEdges(silent=True)
                            else:
                                socket.removeAllEdges(silent=False)

                    # create new edge
                    new_edge = self.getEdgeClass()(item.socket.node.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                    if DEBUG: print("View::edgeDragEnd ~   created new edge:", new_edge, "connecting", new_edge.start_socket, "<-->", new_edge.end_socket)

                    # sent notifications for the new edge
                    for socket in [self.drag_start_socket, item.socket]:
                        socket.node.onEdgeConnectionChanged(new_edge)
                        if socket.is_input: socket.node.onInputChanged(socket)

                    self.grView.grScene.scene.history.storeHistory("Created new edge by dragging", setModified=True)
                    return True
        except Exception as e: dumpException(e)

        if DEBUG: print("View::edgeDragEnd ~ everything done.")
        return False