from graph import Node
import copy

class Game():
    """The Game Class

    :param player: The player, either X or O
    :type player: str
    """
    def __init__(self, player: str) -> None:
        self.game = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0],]
        self.tree = None

        self.player = player.upper()
        if player.lower() == 'x':
            self.ai = 'O'
        else:
            self.ai = 'X'

    def display(self):
        """Displays the game in a user friendly way"""
        # Column Selector
        print("  a   b   c")

        formatted = [str(col).replace('-1', self.player).replace('1', self.ai).replace('0', '-') for col in [row for row in self.game]]
        # Row Selector
        for count, row in enumerate(formatted):
            print(count + 1, end=" ")
            print(row.replace('[', '').replace(']', '').replace(', ', ' | '))

    def generateTree(self, game, player="max") -> dict:
        """Generate a tree of all possible moves
        The tree is a dictionary of all possible moves
        The key is the move, the value is the game state
        after that move has been made

        :param game: Current state of the game to generate the tree on
        :type game: Game
        :param player: Wether to use min or max, defaults to "max"
        :type player: str, optional
        :return: A tree containing all the moves that can be made and what they will look like
        :rtype: dict
        """

        # Decides if it plots 1 or -1
        if player == "max":
            player = 1
        else:
            player = -1

        tree = {}

        # Loop through all the rows and columns
        # Make a copy of the game
        # Moves the player to X Y
        # Adds to dictionary
        for x, row in enumerate(game):
            for y, cell in enumerate(row):
                if cell == 0:
                    new_game = copy.deepcopy(game)
                    new_game[x][y] = player
                    tree[(x, y)] = new_game
        return tree

    def getWinner(self, game):
        """Gets whoever has won

        :param game: The current state of the game
        :type game: Game
        :return: Either 1, -1 or None, Depending on who won
        :rtype: int | None
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

    def move(self, player=-1, row=0, col=0):
        """Moves the player to the specified row and column

        :param player: The player to move, defaults to -1
        :type player: int, optional
        :param row: The row to move to, defaults to 0
        :type row: int, optional
        :param col: The column to move to, defaults to 0
        :type col: int, optional
        :return: Returns the new game state if the move was valid, False if it wasnt
        :rtype: False | Game
        """
        # Make a move on the board
        if self.game[row][col] == 0:
            self.game[row][col] = player
            return self.game
        else:
            return False

    def gameOver(self, game) -> bool:
        """Checks if the game has been won or drawn

        :param game: The current state of the game
        :type game: Game
        :return: True if the game is over, False if it isnt
        :rtype: bool
        """
        # Check if the game is over
        if self.getWinner(game) != None:
            return True
        elif self.getDraw(game):
            return True
        else:
            return False

    def evaluate(self, game) -> int:
        """Evaluates the current state of the game

        :param game: The current state of the game
        :type game: Game
        :return: Whoever has won, 1 for player, -1 for AI, 0 for draw
        :rtype: int
        """
        if self.getWinner(game) == None:
            return 0
        elif self.getWinner(game) == 1:
            return 1
        elif self.getWinner(game) == -1:
            return -1

    def minimax(self, state, depth: int, player: str, tree: dict | None = None) -> list[int, int, int]:
        """Minimax algorithm
        Detailed explanation of the algorithm can be found here:
        https://github.com/Cledersonbc/tic-tac-toe-minimax

        :param state: Current state of the game
        :type state: Game
        :param depth: Depth of the tree to search
        :type depth: int
        :param player: Wether to use min or max
        :type player: str
        :param tree: Wether to create a tree or not, defaults to None
        :type tree: dict | None, optional
        :return: Best move
        :rtype: list[int, int, int]
        """
        # Minimax algorithm
        if player == "max":
            nplayer = 1
            best = [-1, -1, float("-inf")]
        else:
            nplayer = -1
            best = [-1, -1, float("inf")]

        if depth == 0 or self.gameOver(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.generateTree(state, player).items():
            x, y = cell[0]
            state[x][y] = nplayer
            if tree:
                node = Node(state)
                node.action = cell[0]
                if player == "max":
                    score = self.minimax(state, depth - 1, "min", node)
                else:
                    score = self.minimax(state, depth - 1, "max", node)
                node.value = score[2]
                tree.children.append(node)
            else:
                if player == "max":
                    score = self.minimax(state, depth - 1, "min")
                else:
                    score = self.minimax(state, depth - 1, "max")
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == "max":
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    def bestMove(self) -> tuple[int, int]:
        """Gets the best move

        :return: Best move
        :rtype: tuple[int, int]
        """
        depth = len(self.generateTree(self.game, "max"))
        if self.tree == None:
            best = self.minimax(self.game, depth, "max")
        else:
            best = self.minimax(self.game, depth, "max", self.tree)
        return best[0], best[1]

    def moveAI(self):
        """Makes the AI move based on the best move"""
        x, y = self.bestMove()
        self.move(1, x, y)
