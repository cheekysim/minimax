import re
import math
import os
import subprocess
from graphviz import Digraph

from graph import Node, plotTree
from game import Game

# Used to convert a, b, c to 0, 1, 2
cols = {
    "a": 0,
    "b": 1,
    "c": 2
}

def moveValidation() -> tuple:
    """Prompts the user to input a location
    Ensures the the user enters a valid input

    :return: Row and Col to move to
    :rtype: tuple
    """
    while True:
        while True:
            print()
            moveTo = input("Enter A Move, E.G A1: ").lower()
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

def main(graphvis: bool = False):
    """Main Game"""
    game = Game('X')

    # Reset tree directory
    try:
        files = os.listdir('tree')
        for file in files:
            os.remove('tree/' + file)
    except FileNotFoundError:
        os.mkdir('tree')

    # Game Loop
    while True:
        print()
        game.display()
        # If the game is over stop the game
        if game.gameOver(game.game):
            winner = game.evaluate(game.game, 1)
            if winner > 0:
                print("You Lost!")
            elif winner < 0:
                print("You Won!")
            else:
                print("Its A Draw!")
            break
        
        # Make sure player enters correct values
        while True:
            row, col = moveValidation()
            # Check if the move is available
            move = game.move(-1, row, col)
            if move == False:
                print("That space is already taken.")
            else:
                break # Continues with the program
        
        # Check if graphvis is installed
        # Calculate when to start creating game trees,
        # Otherwise they are massive and break the computer
        # Anything above 7! takes ages
        if graphvis:
            fact = math.factorial(len(game.generateTree(game.game, "max")))
            if fact <= 720:
                root = Node(game.game) # This is used as the root node for the decision tree
                root.player = "max"
                game.tree = root # This makes the tree not Null so the code will add to it
            game.moveAI() # Moves the ai and generates the tree
            if fact <= 720:
                # Creates and formats the graph
                graph = Digraph()
                graph.attr(
                    'graph',
                    rankdir='TB',
                    label=f'Decision Tree For {fact} Moves',
                    labelloc='t',
                    labeljust='c',
                    labelfontsize='80'
                    )
                # Function in graph.py
                plotTree(root, graph)   
                # Saves the graph
                graph.render(str(fact) + '.gv', directory='tree', view=False, format='pdf')
        else:
            game.moveAI()

# This means the file should be run
if __name__ == '__main__':
    try:
        subprocess.check_output(['dot', '-V'], stderr=subprocess.STDOUT)
        main(True)
    except subprocess.CalledProcessError:
        print("Graphviz is not installed")
        print("Please install graphviz from https://graphviz.org/download/")
        main(False)