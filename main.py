import copy
import re

class Game():
    def __init__(self, player: str) -> None:
        self.game = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0],]

        self.player = player.upper()
        if player.lower() == 'x':
            self.ai = 'O'
        else:
            self.ai = 'X'

    def display(self):
        # Column Selector
        print("  a   b   c")

        formatted = [str(col).replace('-1', self.player).replace('1', self.ai).replace('0', '-') for col in [row for row in self.game]]
        # Row Selector
        for count, row in enumerate(formatted):
            print(count + 1, end=" ")
            print(row.replace('[', '').replace(']', '').replace(', ', ' | '))

    def generateTree(self, game, player="max"):
        # Generate a tree of all possible moves
        # The tree is a dictionary of all possible moves
        # The key is the move, the value is the game state
        # after that move has been made
        if player == "max":
            player = 1
        else:
            player = -1
        tree = {}
        for x, row in enumerate(game):
            for y, cell in enumerate(row):
                if cell == 0:
                    new_game = copy.deepcopy(game)
                    new_game[x][y] = player
                    tree[(x, y)] = new_game
        return tree

    def getWinner(self, game):
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

    def getDraw(self, game):
        for row in game:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def move(self, player=-1, row=0, col=0):
        # Make a move on the board
        if self.game[row][col] == 0:
            self.game[row][col] = player
            return self.game
        else:
            return False

    def gameOver(self, game):
        # Check if the game is over
        if self.getWinner(game) != None:
            return True
        elif self.getDraw(game):
            return True
        else:
            return False

    def evaluate(self, game):
        if self.getWinner(game) == None:
            return 0
        elif self.getWinner(game) == 1:
            return 1
        elif self.getWinner(game) == -1:
            return -1

    def minimax(self, state, depth, player):
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

    def bestMove(self):
        depth = len(self.generateTree(self.game, "max"))
        best = self.minimax(self.game, depth, "max")
        return best[0], best[1]

    def moveAI(self):
        # Make a move based on the best move
        x, y = self.bestMove()
        self.move(1, x, y)


cols = {
    "a": 0,
    "b": 1,
    "c": 2
}

def moveCheck():
    while True:
        while True:
            print()
            moveTo = input("Enter a move: ").lower()
            if len(moveTo) != 2:
                print("Please enter a valid move.")
            elif re.match("\S\d", moveTo) == None:
                print("Please enter a valid move.")
            else:
                break
        col = int(cols.get(moveTo[0], 3))
        row = int(moveTo[1]) - 1
        if col > 3 or row > 3:
            print("Please Enter A Valid Location")
        else:
            return row, col

while True:
    cursor = input("Would you like to be X or O | ").lower()
    if cursor == 'x' or cursor == 'o':
        break
    else:
        print("Please Enter X or O")

game = Game(cursor.lower())

while True:
    print()
    game.display()
    if game.gameOver(game.game):
        winner = game.evaluate(game.game)
        if winner == 1:
            print("You Lost!")
        elif winner == -1:
            print("You Won!")
        else:
            print("Its A Draw!")
        break
        
    while True:
        row, col = moveCheck()
        move = game.move(-1, row, col)
        if move == False:
            print("That space is already taken.")
        else:
            break
    game.moveAI()
