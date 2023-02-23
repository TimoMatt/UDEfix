from collections import OrderedDict
from nodeeditor.node_graphics_edge import *
from nodeeditor.node_serializable import Serializable
from nodeeditor.utils import dumpException


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False


class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT):
        super().__init__()

        self.scene = scene

        # default init
        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self._edge_type = edge_type

        # create Graphics Edge instance
        self.grEdge = self.createEdgeClassInstance()

        self.scene.addEdge(self)

    def getOtherSocket(self, known_socket):
        return self.start_socket if known_socket == self.end_socket else self.end_socket

    def doSelect(self, new_state=True):
        self.grEdge.doSelect(new_state)

    def __str__(self):
        return "<Edge %s..%s -- S:%s E: %s>" % (
            hex(id(self))[2:5], hex(id(self))[-3:], self.start_socket, self.end_socket
        )

    @property
    def start_socket(self): return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        # assign new start socket
        self._start_socket = value
        # addEdge to the Socket class
        if self.start_socket is not None:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self): return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)

        # assign new end socket
        self._end_socket = value
        # addEdge to the Socket class
        if self.end_socket is not None:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self): return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        # assign new value
        self._edge_type = value

        # update the grEdge pathCalculator
        self.grEdge.createEdgePathCalculator()

        if self.start_socket is not None:
            self.updatePositions()

    def getGraphicsEdgeClass(self):
        return QDMGraphicsEdge

    def createEdgeClassInstance(self):
        self.grEdge = self.getGraphicsEdgeClass()(self)
        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePositions()
        return self.grEdge

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.removeEdge(None)
        if self.end_socket is not None:
            self.end_socket.removeEdge(None)
        self.end_socket = None
        self.start_socket = None

    def remove(self, silent_for_socket=None, silent=False):
        old_sockets = [self.start_socket, self.end_socket]

        if self.grEdge is not None: self.grEdge.hide()
        self.scene.grScene.removeItem(self.grEdge)
        self.scene.grScene.update()
        if DEBUG: print("# Removing Edge", self)
        if DEBUG: print(" - remove edge from all sockets")
        self.remove_from_sockets()
        if DEBUG: print(" - remove grEdge")
        self.grEdge = None
        if DEBUG: print(" - remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass
        if DEBUG: print(" - everything is done")

        try:
            # notify nodes from old sockets
            for socket in old_sockets:
                if socket and socket.node:
                    if silent:
                        continue
                    if silent_for_socket is not None and socket == silent_for_socket:
                        continue

                    # notify socket's node
                    socket.node.onEdgeConnectionChanged(self)
                    if socket.is_input: socket.node.onInputChanged(socket)
        except Exception as e: dumpException(e)

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id if self.start_socket is not None else None),
            ('end', self.end_socket.id if self.end_socket is not None else None),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
