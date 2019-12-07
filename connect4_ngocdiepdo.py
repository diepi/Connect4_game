#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 12:09:58 2017

This Python module runs connect4 game. 
It allows the game to be played by 2 humans, a human against a computer, or computer against itself.
In this game two players take turns dropping objects from the top into a seven-column, six-row vertically suspended grid. 
The pieces fall straight down, occupying the next available space within the column. 
The objective of the game is to be the first to form a horizonala, vertical, or diagonal line of four of one's own discs.
The module should also allow the current game to be saved, and a previously saved game to be loaded and continued.

Ngoc Diep Do
SI:9643942
"""

from copy import deepcopy 
import random
from sys import exit

#Task1

def newGame(player1,player2):
    """ 
    Returns 'game' dictionary, which has 4 key-value pairs.
    1. player1: a nonempty string representing the name of the player 1, if value is the single letter C then it is controlled by the computer
    2. player2: a nonempty string representing the name of the player 2 or C.
    3. who: an integer which is either 1 or 2, representing whose turn is next
    4. board: a list of 6 lists with seven integer entries, 0,1 or 2. 0 means empty position, 1 or 2 means position occupied by player 1 or 2.
    This functon returns a game dictionary, with who =1 and where all the positions of the board are empty.
    """

    game = {
            'player1' : player1,
            'player2' : player2,
            'who' : 1,
            'board' :[[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0], 
                      [0,0,0,0,0,0,0], 
                      [0,0,0,0,0,0,0], 
                      [0,0,0,0,0,0,0], 
                      [0,0,0,0,0,0,0]]}

    return game

#Task2


def printBoard(board):
    """
    Takes a list of a lists as an input and prints the 7x6 Connect Four board.
    Positions occupied by player 1 will be marked by X.
    Positions occupied by player 2 will be marked by O.
    Positions not occupied by any player will be printed empty.
    """
    print("|1|2|3|4|5|6|7| \n+-+-+-+-+-+-+-+")
    for r in range(6):
        for c in range(7):
            if board[r][c] == 1:
                board[r][c] = "X"                
            elif board[r][c] == 2:
                board[r][c] = "O"
            else:
                board[r][c] = " "               
    print(str("|" + board[0][0] + "|" + board[0][1] + "|" + 
               board[0][2] + "|" + board[0][3] + "|" + board[0][4] 
               + "|" + board[0][5] + "|" + board[0][6] + "| \n|" + 
               board[1][0] + "|" + board[1][1] + "|" + board[1][2] 
               + "|" + board[1][3] + "|" + board[1][4] + "|" + 
               board[1][5] + "|" + board[1][6] + "| \n|" + 
               board[2][0] + "|" + board[2][1] + "|" + board[2][2] 
               + "|" + board[2][3] + "|" + board[2][4] + "|" + 
               board[2][5] + "|" + board[2][6] + "| \n|" + 
               board[3][0] + "|" + board[3][1] + "|" + board[3][2] 
               + "|" + board[3][3] + "|" + board[3][4] + "|" + 
               board[3][5] + "|" + board[3][6] + "| \n|" + 
               board[4][0] + "|" + board[4][1] + "|" + board[4][2] 
               + "|" + board[4][3] + "|" + board[4][4] + "|" + 
               board[4][5] + "|" + board[4][6] + "| \n|" + 
               board[5][0] + "|" + board[5][1] + "|" + board[5][2] 
               + "|" + board[5][3] + "|" + board[5][4] + "|" + 
               board[5][5] + "|" + board[5][6] + "|"))
    

#Task3

def loadGame():
    """
    The function attempts to open the text file 'game.txt' 
    and returns its content in form of a game dictionary 
    as specified in function newGame(). 
    The format of 'game.txt' is as follows:
        - Line 1 contains a string corresponding to player1 (either a name or the letter 'C')
        - Line 2 contains a string corresponding to player2 (either a name or the letter 'C')
        - Line 3 contains an integer 1 or 2 corresponding to the value of who
        - Lines 4-9 correspond to the six rows of the Connect Four board, starting with the upper row.
          Each line is a comma-separated string of 7 characters, each character being either 0, 1, or 2.
    Function raises an Exception if the file 'game.txt' cannot 
    be loaded or its content is not of the correct format.
    """
    try:
        f = open("game.txt", mode="rt", encoding="utf8")
        lines = f.readlines()
        player1 = list(lines[0])
        for i in player1:
            if i == '\n':
                player1.remove(i)
        player1 = ''.join(player1)
        player2 = list(lines[1])
        for i in player2:
            if i == '\n':
                player2.remove(i)
        player2 = ''.join(player2)
        who = int(lines[2])
        board = list()
        for r in lines[3:9]:
            line = list()
            for i in r:
                if (i == '0') or (i == '1') or (i == '2'):
                    line.append(int(i))
            if len(line) == 7:
                board.append(line)
        
        if len(board) != 6:
            raise Exception
        game = {'player1':player1,'player2':player2,'who':who,'board':board}
        
        return game
    
    except FileNotFoundError:
        print("There is no such file.")
        
 
    except ValueError:
        print("The file is not in right format.")
        
        
    except Exception:
        print("The file is not in right format.")
        
#Task4

def getValidMoves(board):
    """
    Takes a list of lists as an input and returns a list of integers 
    between 0,...,6 corresponding to the indices of the board columns 
    which are not completely filled. Every integer should appear 
    at most once. If no valid move is possible (i.e., the board is completely filled), 
    the function returns an empty list.
    """
    LoVM = list()
    for i in range(7):
        if board[0][i] == 0:
            LoVM.append(i)
    return LoVM

#Task5

def makeMove(board, move, who):
    """
    Takes as input a list board representing the Connect Four board, 
    An integer move between 0,1,...,6. 
    An integer who with possible values 1 or 2
    The parameter move corresponds to the column index into which the player with number who will insert their “disc”. 
    The function then returns the updated board variable.
    The function does not perform any checks as to whether the move input is valid. 
    """
    while move >= 0:
        for i in range(6):
            b2 = board[::-1]
            if b2[i][move] == 0:
                b2[i][move] = who
                break
        return b2[::-1]
    
#Task6

def hasWon(board,who):
    """
    The function takes as input a list board representing the Connect Four board.
    An integer who with possible values 1 or 2. 
    Then it returns True if the player with number who occupies 
    four adjacent positions which form a horizontal, vertical, or diagonal line. 
    And returns False otherwise.
    """
    for r in range(6):
        for c in range(4):
            if (board[r][c] == board[r][c+1] == board[r][c+2] ==\
                board[r][c+3] == who) and (board[r][c] != 0):
                return True
    for c in range(7):
        for r in range(3):
            if (board[r][c] == board[r+1][c] == board[r+2][c] ==\
                board[r+3][c] == who) and (board[r][c] != 0):
                return True
    for r in range(3):
        for c in range(4):
            if (board[r][c] == board[r+1][c+1] == board[r+2][c+2] ==\
                board[r+3][c+3] == who) and (board[r][c] != 0):
                return True
    for r in range(5,2,-1):
        for c in range(4):
            if (board[r][c] == board[r-1][c+1] == board[r-2][c+2] ==\
                board[r-3][c+3] == who) and (board[r][c] != 0):
                return True
    return False

#Task7
def switchTurn(who):
    """
    Function switches users.
    """
    if (who == 1):
        return 2
    else:
        return 1

def suggestMove1(board, who):
    """
    Takes as inputs a list board representing the Connect Four board and 
    an integer who with possible values 1 or 2. 
    The function returns an integer between 0,1,...,6 corresponding 
    to a column index of the board into which player number who 
    should insert their "disc" in the folowing way:
    - If among all valid moves of player number who there is a move which leads 
    to an immediate win of this player. In this case, return such a winning move.
    - If there is no winning move for player number who, we will try to prevent 
    the other player from winning by returning their winning column.
    - If there is no immediate winning move for both players, 
    the function simply returns a valid move.
    """
    L = getValidMoves(board)  
    try:
        while True:
            for m in L:               
                b1 = makeMove(deepcopy(board), m, who)                 
                if hasWon(b1,who):
                    move1 = m
                    break
            for n in L:
                b2 = makeMove(deepcopy(board), n, switchTurn(who))
                if hasWon(b2,switchTurn(who)):
                    move2 = n
                    break  
            try:
                return move1
            except UnboundLocalError:
                return move2
    except UnboundLocalError:
        return random.choice(L) 

 
#Task9            
    
def saveGame(game):
    """
    Takes as input a game dictionary as specified in function newGame(),
    and writes its content into the text file 'game.txt' in the format 
    specified in loadGame() function. 
    If saving fails (for whatever reason), the function will return an exception.
    """
    try:
        f = open("game.txt", mode="wt", encoding="utf8")                
        for el in game.values():
            if type(el) is list:
                for i in range(6):
                    f.write(",".join(str(x) for x in el[i]) + '\n')
            else:
                f.write(str(el)+'\n')
    except Exception:
        print("Game can not be saved. Please try again later.")
        
#functions for Task8

def humanMove(board):
    """
    Returns a valid move that user chose.
    If input is "s" the function will return the string "s" used for saving in play() function.
    Otherwise the column is specified by the user as an integer 1,2,...,7. 
    The function needs to check that the user input 
    corresponds to a valid move and otherwise print a warning message 
    and repeat asking for a valid input.
    """
    while True:
            try:       
                c = input("Which column you want to choose? ")
                if c == "s":
                    return "s" 
                    break
                else:
                    c = int(c)                 
                    for r in range(6):
                        if 1<=c<=7 and board[r][c-1] == 0:
                            return c-1
                            break
                    else:
                        print("You can not choose this column.")
         
            except ValueError:
                print("Please choose a column from 1-7.")
            

def fullBoard(board):
    """
    Takes as inputs a list board representing the Connect Four board.
    If there is no valid move left, the function returns True, otherwise returns False.
    """
    for r in range(6):
        for c in range(7):
            if board[r][c] == 0:
                return False
    return True



#Task10

def Threesome(board,who):
    """
    The function takes as input a list board representing the Connect Four board.
    An integer who with possible values 1 or 2. 
    Then it returns True if the player with number who occupies 
    3 adjacent positions which form a horizontal, vertical, or diagonal line. 
    And returns False otherwise.
    """
    for r in range(6):
        for c in range(5):
            if (board[r][c] == board[r][c+1] == board[r][c+2] == who) and (board[r][c] != 0):
                return True
    for c in range(7):
        for r in range(4):
            if (board[r][c] == board[r+1][c] == board[r+2][c] == who) and (board[r][c] != 0):
                return True
    for r in range(4):
        for c in range(5):
            if (board[r][c] == board[r+1][c+1] == board[r+2][c+2]  == who) and (board[r][c] != 0):
                return True
    for r in range(5,1,-1):
        for c in range(5):
            if (board[r][c] == board[r-1][c+1] == board[r-2][c+2] == who) and (board[r][c] != 0):
                return True
    return False

def secondMove(board):
    """
    Takes as inputs a list board representing the Connect Four board.
    If there is only one column with "disc", 
    the function will suggest the moves next to it or above it.
    """
    L = list()
    L2 = list()
    for c in range(7):    
        if board[5][c] != 0:
            L.append(c)
    if len(L) == 1:
        for c in L:
            L2.append(c)
            L2.append(c-1)
            L2.append(c+1)
            return L2
            

def suggestMove2(board, who):
    """
    Takes as inputs a list board representing the Connect Four board.
    An integer who with possible values 1 or 2. 
    The function returns an integer between 0,1,...,6 corresponding 
    to a column index of the board into which player number who 
    should insert their "disc".
    """
    L = getValidMoves(board)   
    while True:
        for m1 in L:               
            b1 = makeMove(deepcopy(board), m1, who)                 
            if hasWon(b1,who):
                move1 = m1
                break
        for m2 in L:
            b2 = makeMove(deepcopy(board), m2, switchTurn(who))
            if hasWon(b2,switchTurn(who)):
                move2 = m2
                break 
        for m3 in L:
            for user in {1,2}:
                b3 = makeMove(deepcopy(board), m3, user) 
                if Threesome(b3, user):
                    move3 = m3
                    break
        try:return move1
        except UnboundLocalError:
            try:return move2
            except UnboundLocalError:
                try:return move3
                except UnboundLocalError:
                    if secondMove(board) != None:
                        return random.choice(secondMove(board)) 
                    else:
                        return random.choice(L)
                        

#Task8       

# ------------------- Main function --------------------

def play():
    """ 
    Function will first print a welcome message to the user.
    
    It will then ask for the names of player 1 and player 2. 
    These names are inputted as nonempty strings and their first letter will be automatically capitalized. 
    If the user enters an empty string, the program will keep on asking for the user name.
    
     - If one of the players’ names (or both) is the letter 'C', 
       then corresponding user is played automatically by the computer.
       
     - If the name of player 1 is entered as the letter 'L' (for load), 
       the function will skip asking for the name of player 2 and 
       attempt to load a game dictionary from 'game.txt'.
       If the loading fails the game just ends with an error message.
       
     - Otherwise the function creates a new game dictionary with the two players’ names, 
       an empty board, and with player 1 being active. With the game structure being set, 
       the game play can begin, with both players taking turns alternatingly.
     
    If the active player is human, the function asks which column they want to select. 
    The column is specified by the user as an integer 1,2,...,7. 
    The function checks that the user input corresponds to a valid move and 
    otherwise it prints a warning message and repeats asking for a valid input.
    
    If the active player’s name is 'C', the function will make a move automatically.
    
    If after a move the function finds that a player has won, the game prints this information and
    then ends.
    
    If there is no valid move left, the game prints that there was a draw and ends.
    
    Otherwise, the active player switches and the program continues with Step 6.
    """
    print("*"*55)
    print("***"+" "*8+"WELCOME TO CONNECT FOUR GAME!"+" "*8+"***")
    print("*"*55,"\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    while True:
        player1 = input("Name of 1. player: ").title()
        if player1 == "L":
            ngame = loadGame() 
            if ngame == None:
                exit()
            else:
                break           
        if player1 != "":                    
            player2 = input("Name of 2. player: ").title()
            if player2 == "":
                print("Please enter again the names.")
            else:               
                ngame = newGame(player1,player2)
                break
       
    b = ngame['board']
    b2 = deepcopy(ngame['board'])
    printBoard(b2)
    who = ngame['who']     
    gameover = False

    
    while not gameover: 
        if who == 1:
            active=ngame['player1']
        else:
            active=ngame['player2']
                
        if active != "C":           
            print("Now it is your turn, {}".format(active))
            move = humanMove(b)
            if move == "s":
                saveGame(ngame)
                print("Game is saved.")           
            else:
                b2 = deepcopy(makeMove(b,move,who)) 
                printBoard(b2)        
                if hasWon(b, who) is True:
                    print("Good job {},you won!".format(active))
                    gameover = True
                    break 
                elif fullBoard(b):
                    print("It is a tie.")
                    gameover = True
                    break
                else:                                         
                    who = switchTurn(who)                   
                    for key,value in ngame.items():
                        ngame['who'] = who
                                       
        if active == "C":             
            move = suggestMove2(b,who)
            print("Computer has selected column {}.".format(move + 1))
            b2 = deepcopy(makeMove(b,move,who)) 
            printBoard(b2)
            if hasWon(b, who) is True:
                print("Player{} Computer has won!".format(who))
                gameover = True
                break
                         
            elif fullBoard(b):
                print("It is a tie!")
                gameover = True
                break
            else:               
                who = switchTurn(who)               
                for key,value in ngame.items():
                        ngame['who'] = who


if __name__ == '__main__' or __name__ == 'builtins':
    play()