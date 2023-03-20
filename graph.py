from game import Game
from graphviz import Digraph # For type used in plotTree

class Node():
    def __init__(self, state):
        """Init variable, sets up colors and variables"""
        self.state = state
        self.formatted = self.format()
        self.children = []
        self.action = None
        self.value = 0
        self.color = "#FFFFFF"
        __tempGame = Game('O')
        if __tempGame.getWinner(state) == 1:
            self.color = "#00AA00"
        elif __tempGame.getWinner(state) == -1:
            self.color = "#AA0000"
        elif __tempGame.getDraw(state):
            self.color = "#AAAAAA"
        else:
            self.color = "#EEEEEE"
    

    def isLeaf(self) -> bool:
        """If the node has no children its a leaf

        :return: True or False if children or not
        :rtype: bool
        """
        return len(self.children) == 0
    

    
    def format(self) -> str:
        """Returns a string instead of a dictionary

        :return: Game formatted as a string
        :rtype: str
        """
        result = ""
        for row in self.state:
            for cell in row:
                if cell == 0:
                    result += "-"
                elif cell == 1:
                    result += "O"
                elif cell == -1:
                    result += "X"
            result += "\n"
        return result


def plotTree(node: Node, graph: Digraph) -> None:
    """Adds all the nodes to the tree

    :param node: Parent Node
    :type node: Node
    :param graph: Graph to add to
    :type graph: Digraph
    """

    if node.isLeaf():
        graph.node(str(id(node)), label=str(node.formatted), shape='circle', style='filled', fillcolor=node.color)
    else:
        graph.node(str(id(node)), label=str(node.formatted), shape='box', style='filled', fillcolor=node.color)
        for child in node.children:
            plotTree(child, graph)
            graph.edge(str(id(node)), str(id(child)), label=f'({child.action[0] + 1}, {child.action[1] + 1}) {child.value}')
