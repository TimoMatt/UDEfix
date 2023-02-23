import os
import json
from collections import OrderedDict
from nodeeditor.utils import dumpException
from nodeeditor.node_serializable import Serializable
from nodeeditor.node_graphics_scene import QDMGraphicsScene
from nodeeditor.node_node import Node
from nodeeditor.node_edge import Edge
from nodeeditor.node_scene_history import SceneHistory
from nodeeditor.node_scene_clipboard import SceneClipboard

DEBUG = False


class InvalidFile(Exception): pass


class Scene(Serializable):
    def __init__(self, node_editor_widget=None):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.node_editor_widget = node_editor_widget

        self.scene_width = 64000
        self.scene_height = 64000

        # custom flag used to suppress triggering onItemSelected
        self._silent_selection_events = False

        self._has_been_modified = False
        self._last_selected_items = None

        # initialize all listeners
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        # store callback for retrieving the class for Node
        self.node_class_selector = None

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.grScene.itemSelected.connect(self.onItemSelected)
        self.grScene.itemsDeselected.connect(self.onItemsDeselected)

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def getNodeByID(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def setSilentSelectionEvents(self, value=True):
        self._silent_selection_events = value

    def onItemSelected(self, silent=False):

        if self._silent_selection_events: return

        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            if not silent:
                for callback in self._item_selected_listeners: callback()
                self.history.storeHistory("Selection Changed")

    def onItemsDeselected(self, silent=False):
        # event is being triggered when start dragging file outside of this application
        current_selected_items = self.getSelectedItems()
        if current_selected_items == self._last_selected_items:
            return

        self.resetLastSelectedStates()
        if current_selected_items == []:
            self._last_selected_items = []
            if not silent:
                self.history.storeHistory("Deselected everything")
                for callback in self._items_deselected_listeners: callback()

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.grScene.selectedItems()

    def doDeselectItems(self, silent=False):
        for item in self.getSelectedItems():
            item.setSelected(False)
        if not silent:
            self.onItemsDeselected()

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = True

            # call all registered listeners
            for callback in self._has_been_modified_listeners: callback()
        elif self._has_been_modified and not value:  # test-case for resetting * in window name
            self._has_been_modified = False

            # call all registered listeners
            for callback in self._has_been_modified_listeners: callback()

        self._has_been_modified = value

    # helper listener functions
    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def addItemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback)

    def addItemsDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    def addDragEnterListener(self, callback):
        self.getView().addDragEnterListener(callback)

    def addDropListener(self, callback):
        self.getView().addDropListener(callback)

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.grNode._last_selected_state = False
        for edge in self.edges:
            edge.grEdge._last_selected_state = False

    def getView(self):
        return self.grScene.views()[0]

    def getItemAt(self, pos):
        return self.getView().itemAt(pos)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes: self.nodes.remove(node)
        # commented because it resulted in redundant warnings
        # else: print("!W:", "Scene::removeNode", "wanna remove node", node, "from self.nodes but it's not in the list!")

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        # commented because it resulted in redundant warnings
        # else: print("!W:", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            if DEBUG: print("saving to", filename, "was successfull.")

            self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data, encoding='utf-8')
                self.deserialize(data)
                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

    def getEdgeClass(self):
        return Edge

    def setNodeClassSelector(self, class_selecting_function):
        """ When the function self.node_class_selector is set, we can use different Node Classes"""
        self.node_class_selector = class_selecting_function

    def getNodeClassFromData(self, data):
        return Node if self.node_class_selector is None else self.node_class_selector(data)

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        hashmap = {}

        if restore_id: self.id = data['id']

        # instead of recreating all the nodes, reuse existing ones
        # get list of all current nodes:
        all_nodes = self.nodes.copy()

        # go through deserialized nodes:
        for node_data in data['nodes']:
            found = False
            for node in all_nodes:
                if node.id == node_data['id']:
                    found = node
                    break

            if not found:
                new_node = self.getNodeClassFromData(node_data)(self)
                new_node.deserialize(node_data, hashmap, restore_id)
                new_node.onDeserialized(node_data)
                # print("New node for", node_data['title'])
            else:
                found.deserialize(node_data, hashmap, restore_id)
                found.onDeserialized(node_data)
                all_nodes.remove(found)
                # print("Reused", node_data['title'])

        # remove nodes which are left in the scene and were NOT in the serialized data!
        # that means they were not in the graph before
        while all_nodes != []:
            node = all_nodes.pop()
            node.remove()

        # instead of recreating all the edges, reuse existing ones
        # get list of all current edges:
        all_edges = self.edges.copy()

        # go through deserialized edges:
        for edge_data in data['edges']:
            found = False
            for edge in all_edges:
                if edge.id == edge_data['id']:
                    found = edge
                    break

            if not found:
                new_edge = Edge(self).deserialize(edge_data, hashmap, restore_id)
                # print("New edge for", edge_data)
            else:
                found.deserialize(edge_data, hashmap, restore_id)
                all_edges.remove(found)

        # remove nodes which are left in the scene and were NOT in the serialized data!
        # that means they were not in the graph before...
        while all_edges != []:
            edge = all_edges.pop()
            edge.remove()

        return True

