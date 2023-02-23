from nodeeditor.node_graphics_edge import QDMGraphicsEdge
from nodeeditor.utils import dumpException


DEBUG = False


class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        self.history_limit = 32

        self.undo_selection_has_changed = False

        # listeners
        self._history_modified_listeners = []
        self._history_stored_listeners = []
        self._history_restored_listeners = []

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def addHistoryModifiedListener(self, callback):
        self._history_modified_listeners.append(callback)

    def addHistoryStoredListener(self, callback):
        self._history_stored_listeners.append(callback)

    def addHistoryRestoredListener(self, callback):
        self._history_restored_listeners.append(callback)

    def storeInitialHistoryStamp(self):
        self.storeHistory("Initial History Stamp")

    def canUndo(self):
        return self.history_current_step > 0

    def canRedo(self):
        return self.history_current_step + 1 < len(self.history_stack)

    def undo(self):
        if DEBUG: print("UNDO")

        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()

            if self.history_stack[self.history_current_step]['desc'] == "Initial History Stamp":
                self.scene.has_been_modified = False
            else:
                self.scene.has_been_modified = True

    def redo(self):
        if DEBUG: print("REDO")

        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def restoreHistory(self):
        if DEBUG: print("Restoring history",
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])
        for callback in self._history_modified_listeners: callback()
        for callback in self._history_restored_listeners: callback()

    def storeHistory(self, desc, setModified=False):
        if setModified:
            self.scene.has_been_modified = True

        if DEBUG: print("Storing history", '"%s"' % desc,
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))

        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print("  -- setting step to:", self.history_current_step)

        # always trigger history modified
        for callback in self._history_modified_listeners: callback()
        for callback in self._history_stored_listeners: callback()

    def captureCurrentSelection(self):
        sel_obj = {
            'nodes': [],
            'edges': [],
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'): sel_obj['nodes'].append(item.node.id)
            elif hasattr(item, 'edge'): sel_obj['edges'].append(item.edge.id)
        return sel_obj

    def createHistoryStamp(self, desc):
        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': self.captureCurrentSelection(),
        }

        return history_stamp

    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp['desc'])

        try:
            self.undo_selection_has_changed = False
            previous_selection = self.captureCurrentSelection()

            self.scene.deserialize(history_stamp['snapshot'])

            # restore selection
            # first clear all selection on edges
            for edge in self.scene.edges: edge.grEdge.setSelected(False)
            # now restore selected nodes from history_stamp
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.grEdge.setSelected(True)
                        break

            # first clear all selection on nodes
            for node in self.scene.nodes: node.grNode.setSelected(False)
            # now restore selected nodes from history_stamp
            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.grNode.setSelected(True)
                        break

            current_selection = self.captureCurrentSelection()

            # reset the last_selected_items
            self.scene._last_selected_items = self.scene.getSelectedItems()

            # if the selection of nodes differ before and after restoration, set flag
            if current_selection['nodes'] != previous_selection['nodes'] or current_selection['edges'] != previous_selection['edges']:
                self.undo_selection_has_changed = True

        except Exception as e: dumpException(e)
