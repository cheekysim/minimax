from graphviz import Digraph # For type used in plotTree

class Node():
    """Node class for the minimax tree

    :param state: The current state of the game
    :type state: Game
    """
    def __init__(self, state):
        """Init variable, sets up colors and variables"""
        self.state = state
        self.formatted = self.format()
        self.children = []
        self.action = None
        self.value = 0
        self.color = "#FFFFFF"
        if self.getWinner(state) == 1:
            self.color = "#00AA00"
        elif self.getWinner(state) == -1:
            self.color = "#AA0000"
        elif self.getDraw(state):
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
    
    # From game.py to avoid circular imports
    def getWinner(self, game):
        """Gets whoever has won

        :param game: The current state of the game
        :type game: Game
        :return: Either 1, -1 or None, Depending on who won
        :rtype: int or None
        """
        # Check row
        rows = [sum(row) for row in game]
        if 3 in rows:
            return 1
        elif -3 in rows:
            return -1

        cols = [sum(col) for col in zip(*game)]
        if 3 in cols:
            return 1
        elif -3 in cols:
            return -1

        diags = [game[0][0] + game[1][1] + game[2]
                 [2], game[0][2] + game[1][1] + game[2][0]]
        if 3 in diags:
            return 1
        elif -3 in diags:
            return -1

    def getDraw(self, game) -> bool:
        """Detects if a draw has happened

        :param game: Current state of the game
        :type game: Game
        :return: True if there is a draw, False if there isnt
        :rtype: bool
        """
        for row in game:
            for cell in row:
                if cell == 0:
                    return False
        return True


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