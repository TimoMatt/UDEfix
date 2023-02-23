from math import *
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_socket import *
from nodeeditor.utils import dumpException, pp


DEBUG = False


class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[], additional=[]):
        super().__init__()
        self._title = title
        self.scene = scene

        self.content = None
        self.grNode = None

        self.initInnerClasses()
        self.initSettings()

        self.title = title

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        # create socket for input and outputs
        self.inputs = []
        self.outputs = []
        self.additional = []
        self.initSockets(inputs, outputs, additional)

        # dirty and evaluation
        self._is_dirty = False
        self._is_invalid = False

    def initInnerClasses(self):
        self.content = QDMNodeContentWidget(self)
        self.grNode = QDMGraphicsNode(self)

    def initSettings(self):
        self.socket_spacing = 22

        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP
        self.additional_socket_position = BOTTOM
        self.input_multi_edged = True
        self.output_multi_edged = True
        self.additional_multi_edged = True
        self.socket_offsets = {
            LEFT_BOTTOM: -1,
            LEFT_CENTER: -1,
            LEFT_TOP: -1,
            RIGHT_BOTTOM: 1,
            RIGHT_CENTER: 1,
            RIGHT_TOP: 1,
            BOTTOM: 0
        }

    def initSockets(self, inputs, outputs, additional, reset=True):
        """ Create sockets for inputs and outputs """

        if reset:
            # clear old sockets
            if hasattr(self, "inputs") and hasattr(self, "outputs") and hasattr(self, "additional"):
                # remove grSockets from scene
                for socket in (self.inputs+self.outputs+self.additional):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []
                self.additional = []

        # create new sockets
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=self.input_socket_position, socket_type=item,
                            multi_edges=self.input_multi_edged,
                            count_on_this_node_side=len(inputs), input_type=1)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=self.output_socket_position, socket_type=item,
                            multi_edges=self.output_multi_edged,
                            count_on_this_node_side=len(outputs), input_type=2)
            counter += 1
            self.outputs.append(socket)

        counter = 0
        for item in additional:
            socket = Socket(node=self, index=counter, position=self.additional_socket_position, socket_type=item,
                            multi_edges=self.additional_multi_edged,
                            count_on_this_node_side=len(additional), input_type=3)
            counter += 1
            self.additional.append(socket)

    def onEdgeConnectionChanged(self, new_edge):
        print("%s::onEdgeConnectionChanged" %  self.__class__.__name__, new_edge)

    def onInputChanged(self, new_edge):
        print("%s::onInputChanged" %  self.__class__.__name__, new_edge)

    def onDeserialized(self, data):
        pass

    def onDoubleClicked(self, event):
        pass

    def doSelect(self, new_state=True):
        self.grNode.doSelect(new_state)

    def isSelected(self):
        return self.grNode.isSelected()

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title

    def getSocketPosition(self, index, position, num_out_of=1):
        if position in (LEFT_BOTTOM, LEFT_CENTER, LEFT_TOP):
            x = self.socket_offsets[position]
        elif position == BOTTOM:
            x = self.grNode.width/2
        else:
            x = self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_roundness - self.grNode.title_vertical_padding - index * self.socket_spacing
        elif position in (LEFT_CENTER, RIGHT_CENTER):
            num_sockets = num_out_of
            node_height = self.grNode.height
            top_offset = self.grNode.title_height + 2 * self.grNode.title_vertical_padding + self.grNode.edge_padding
            available_height = node_height - top_offset

            total_height_of_all_sockets = num_sockets * self.socket_spacing
            new_top = available_height - total_height_of_all_sockets

            y = top_offset + available_height/2 + (index-0.5)*self.socket_spacing
            if num_sockets > 1:
                y -= self.socket_spacing * (num_sockets-1)/2
        elif position in (LEFT_TOP, RIGHT_TOP):
            # start from top
            y = self.grNode.title_height + self.grNode.title_vertical_padding + self.grNode.edge_roundness + index * self.socket_spacing
        elif position == BOTTOM:
            y = self.grNode.height
        else:
            # this should never happen
            y = 0

        return [x, y]

    def getSocketScenePosition(self, socket):
        nodepos = self.grNode.pos()
        socketpos = self.getSocketPosition(socket.index, socket.position, socket.count_on_this_node_side)
        return (nodepos.x() + socketpos[0], nodepos.y() + socketpos[1])

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs + self.additional:
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.updatePositions()

    def remove(self):
        if DEBUG: print(">Removing Node", self)
        if DEBUG: print(" - remove all edges from sockets")
        for socket in (self.inputs + self.outputs + self.additional):
            for i in range(len(socket.edges)):
                socket.edges[0].remove()

            # for edge in socket.edges:
            #     if DEBUG: print("    - removing from socket:", socket, "edge:", edge)
            #     edge.remove()
        if DEBUG: print(" - remove grNode")
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG: print(" - remove node from the scene")
        self.scene.removeNode(self)
        if DEBUG: print(" - everything was done.")

    # node evaluation stuff

    def isDirty(self):
        return self._is_dirty

    def markDirty(self, new_value=True):
        self._is_dirty = new_value
        if self._is_dirty: self.onMarkedDirty()

    def onMarkedDirty(self): pass

    def markChildrenDirty(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markDirty(new_value)

    def markDescendantsDirty(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markDirty(new_value)
            other_node.markDescendantsDirty(new_value)

    def isInvalid(self):
        return self._is_invalid

    def markInvalid(self, new_value=True):
        self._is_invalid = new_value
        if self._is_invalid: self.onMarkedInvalid()

    def onMarkedInvalid(self): pass

    def markChildrenInvalid(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markInvalid(new_value)

    def markDescendantsInvalid(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markInvalid(new_value)
            other_node.markDescendantsInvalid(new_value)

    def eval(self):
        self.markInvalid(False)
        return 0

    def evalChildren(self):
        for node in self.getChildrenNodes():
            node.eval()

    def evalDescendants(self):
        for node in self.getChildrenNodes():
            node.eval()
            node.evalDescendants()

    # traversing nodes functions
    def nodeIsValid(self):
        if self._is_invalid: return False
        other_nodes_valid = []
        for node in self.getInputs():
            if node._is_invalid:
                return False
            other_nodes_valid.append(node.nodeIsValid())
        if len(other_nodes_valid) == 0: return True
        else:
            return_val = True
            for val in other_nodes_valid:
                return_val = return_val and val
            return return_val

    def getChildrenNodes(self):
        if self.outputs == []: return []
        other_nodes = []
        for ix in range(len(self.outputs)):
            for edge in self.outputs[ix].edges:
                other_node = edge.getOtherSocket(self.outputs[0]).node
                other_nodes.append(other_node)
        return other_nodes

    def getInput(self, index=0):
        try:
            input_socket = self.inputs[index]
            if len(input_socket.edges) == 0: return None
            connecting_edge = input_socket.edges[0]
            other_socket = connecting_edge.getOtherSocket(self.inputs[index])
            return other_socket.node
        except Exception as e:
            dumpException(e)
            return None

    def getInputWithSocket(self, index=0):
        try:
            input_socket = self.inputs[index]
            if len(input_socket.edges) == 0: return None, None
            connecting_edge = input_socket.edges[0]
            other_socket = connecting_edge.getOtherSocket(self.inputs[index])
            return other_socket.node, other_socket
        except Exception as e:
            dumpException(e)
            return None, None

    def getInputWithSocketIndex(self, index=0):
        try:
            edge = self.inputs[index].edges[0]
            socket = edge.getOtherSocket(self.inputs[index])
            return socket.node, socket.index
        except IndexError:
            # print("EXC: Trying to get input with socket index %d, but none is attached to" % index, self)
            return None, None
        except Exception as e:
            dumpException(e)
            return None, None

    def getInputs(self, index=0):
        ins = []
        for edge in self.inputs[index].edges:
            other_socket = edge.getOtherSocket(self.inputs[index])
            ins.append(other_socket.node)
        return ins

    def getStartNodes(self):
        ins = self.getInputs()
        if not ins:
            return [self]
        else:
            res = []
            for node in ins:
                res += node.getStartNodes()
            return res

    def getOutputs(self, index=0):
        outs = []
        for edge in self.outputs[index].edges:
            other_socket = edge.getOtherSocket(self.outputs[index])
            outs.append(other_socket.node)
        return outs

    def getAdditional(self, index=0):
        adds = []
        for edge in self.additional[index].edges:
            other_socket = edge.getOtherSocket(self.additional[index])
            adds.append(other_socket.node)
        return adds

    # serialization functions
    def serialize(self):
        inputs, outputs, additional = [], [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        for socket in self.additional: additional.append(socket.serialize())
        ser_content = self.content.serialize() if isinstance(self.content, Serializable) else {}
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('additional', additional),
            ('content', ser_content),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        try:
            if restore_id: self.id = data['id']
            hashmap[data['id']] = self

            self.setPos(data['pos_x'], data['pos_y'])
            self.title = data['title']

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            try:
                data['additional'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            except KeyError:
                print("WARNING: obsolete graph data")
            num_inputs = len(data['inputs'])
            num_outputs = len(data['outputs'])
            try:
                num_additional = len(data['additional'])
            except KeyError:
                print("WARNING: obsolete graph data")

            for socket_data in data['inputs']:
                found = None
                for socket in self.inputs:
                    if socket.index == socket_data['index']:
                        found = socket
                        break
                if found is None:
                    # create new socket
                    found = Socket(
                        node=self, index=socket_data['index'], position=socket_data['position'],
                        socket_type=socket_data['socket_type'], count_on_this_node_side=num_inputs,
                        input_type=1
                    )
                    self.inputs.append(found)
                found.deserialize(socket_data, hashmap, restore_id)

            for socket_data in data['outputs']:
                found = None
                for socket in self.outputs:
                    # print("\t", socket, socket.index, "=?", socket_data['index'])
                    if socket.index == socket_data['index']:
                        found = socket
                        break
                if found is None:
                    # we can create new socket for this
                    found = Socket(
                        node=self, index=socket_data['index'], position=socket_data['position'],
                        socket_type=socket_data['socket_type'], count_on_this_node_side=num_outputs,
                        input_type=2
                    )
                    self.outputs.append(found)  # append newly created output to the list
                found.deserialize(socket_data, hashmap, restore_id)

            try:
                for socket_data in data['additional']:
                    found = None
                    for socket in self.additional:
                        if socket.index == socket_data['index']:
                            found = socket
                            break
                    if found is None:
                        # create new socket
                        found = Socket(
                            node=self, index=socket_data['index'], position=socket_data['position'],
                            socket_type=socket_data['socket_type'], count_on_this_node_side=num_additional,
                            input_type=3
                        )
                        self.additional.append(found)
                    found.deserialize(socket_data, hashmap, restore_id)
            except KeyError:
                print("WARNING: obsolete graph data")
        except Exception as e: dumpException(e)

        # also deserialize the content of the node
        if isinstance(self.content, Serializable):
            res = self.content.deserialize(data['content'], hashmap)
            return res

        return True
