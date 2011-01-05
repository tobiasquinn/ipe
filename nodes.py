# These are the nodes that hold information about a playlist

class NodePlaylist:
    def __init__(self, label):
        self._label = label
        self._children = []

    def addChild(self, child):
        child.setParent(self)
        self._children.append(child)

    def getNumberOfChildren(self):
        return len(self._children)

    def getChild(self, index):
        return self._children[index]

    def setParent(self, parent):
        self._parent = parent

    def getParent(self):
        return self._parent

    def getLabel(self):
        return self._label

    def getIndex(self, childNode):
        # return the index of the childNode
        # (used for tree walking)
        return self._children.index(childNode)
