import random
#MAKE A CLASS FOR PLAYER AND FOR PIECES

board_size = 6
checker_cnt = 3
die_size = 6

board = []

def printboard():
    global board
    for spot in board:
        if spot == 0:
            print '_',
        else:
            print spot,


def makefreshboard():
    global board_size, checker_cnt, die_size, board
    board = []
    for i in range(0,board_size+2): #Additional two for both "homes"
        if i == 0:
            board.append([1])
        elif i == board_size+1:
            board.append([2])
        elif i < checker_cnt:
            board.append(1)
        elif i >= board_size - checker_cnt + 2:
            board.append(2)
        else:
            board.append(0)

def roll():
    global die_size
    return random.randint(1,6)

# If it's positive, p1 goes first. Neg, p2
def firstroll():
    while True:
        p1_roll = roll()
        p2_roll = roll()
        dif = p1_roll - p2_roll
        if dif != 0:
            break;
    return dif

makefreshboard()
printboard()
