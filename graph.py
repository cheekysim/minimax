from graphviz import Digraph # For type used in plotTree

class Node():
    """Node class for the minimax tree

    :param state: The current state of the game
    :type state: Game
    """
    def __init__(self, state: dict):
        """Init variable, sets up colors and variables"""
        self.state = state
        self.formatted = self.format()
        self.children = []
        self.action = None
        self.value = None
        self.best = False
        self.player = "max"
        self.color = "#FFFFFF"
        if self.getWinner(state) == 1:
            self.color = "#00AA00"
        elif self.getWinner(state) == -1:
            self.color = "#AA0000"
        elif self.getDraw(state):
            self.color = "#AAAAAA"
        else:
            self.color = "#EEEEEE"

    def bestMove(self, position: tuple[int, int]) -> str:
        """Calculates the edge color and pen width based on the best move(s)

        :param position: Position of the move
        :type position: tuple
        :return: Edge color
        :rtype: str
        """
        # Best is used to make one continuous line
        # This avoids random green lines appearing on the opposite side of the graph
        if self.best == False:
            return "#222222", "2"
        
        # Find the best move(s) and return green and a thicker line
        if self.player == "max":
            best = [[(-1, -1), float("-inf")]]

            for child in self.children:
                if child.value > best[0][1]:
                    best = [[child.action, child.value, child]]
                # If there are multiple best moves, turn them all green
                elif child.value == best[0][1]:
                    best.append([child.action, child.value, child])
            # If the child is the best, turn it green
            for action in best:
                action[2].best = True
                if action[0] == position:
                    return "#00AA00", "4"
                
        # Uses min instead of max
        else:
            best = [[(-1, -1), float("+inf")]]

            for child in self.children:
                if child.value < best[0][1]:
                    best = [[child.action, child.value, child]]
                # If there are multiple best moves, turn them all green
                elif child.value == best[0][1]:
                    best.append([child.action, child.value, child])
            # If the child is the best, turn it green
            for action in best:
                # Allows the green line to spread to the next iteration of children
                action[2].best = True
                if action[0] == position:
                    return "#00AA00", "4"
        # If the child is not the best, turn it black
        return "#222222", "2"

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
        graph.node(str(id(node)),
                   label=f'{str(node.formatted)}{node.player}',
                   shape='box',
                   style='filled',
                   fillcolor=node.color)
        
        for child in node.children:
            edgeColor, penWidth = node.bestMove(child.action)
            graph.edge(str(id(node)),
                       str(id(child)),
                       label=f'({child.action[0] + 1}, {child.action[1] + 1}) | {child.value}',
                       style='filled',
                       penwidth=penWidth,
                       color=edgeColor)
            plotTree(child, graph)
