# Drive ya nuts!
#   Midgie Williams COSI 101a
#           I've used the random and the time package from python
#           Order: first nut is center, then the one that matches the 1, 2, ...n
#           As for numbers on the nut, just arranged clockwise
import random
import time

#My editor didn't support input to so I added a testing variable that would just
#let me type in the user input when set to True
testing = False
n = 6
count = 0
max_perm = 0

def MAIN():
    global testing, n, count, max_perm
    nuts = []
    exit = False
    if not testing:
        print 'To exit, type \'-1\' at any point you are able to give input'
        while not exit:
            if not testing:
                randORgiv = input('\n(0) To do a random puzzle with entered size \n(1) To do the given 6 sided example \n>> ')
                if randORgiv == 0:
                    n = input('How many sides does your nut have? >> ')
                    if n == -1:
                        exit = True
                        break
                    nuts = generate()
                elif randORgiv == 1:
                    n = 6
                    nuts = [[1, 6, 5, 4, 3, 2],
                      [1, 6, 4, 2, 5, 3],
                      [1, 2, 3, 4, 5, 6],
                      [1, 6, 2, 4, 5, 3],
                      [1, 4, 3, 6, 5, 2],
                      [1, 4, 6, 2, 3, 5],
                      [1, 6, 5, 3, 2, 4]]
                elif randORgiv == -1:
                    exit = True
            if not exit:
                max_perm = fact(1, n+1)
                solution = prune_solve([], nuts)

                if solution is None:
                    print 'No solution found for:'
                    for nut in nuts:
                        print nut
                else:
                    for nut in solution:
                        print nut
    else:
        nuts = generate()
        max_perm = fact(1, n+1)
        solution = prune_solve([], nuts)
        if solution is None:
            print 'No solution found for:'
            for nut in nuts:
                print nut

#Attempts to give the answer for number 5 of the questions; generates 1000 random
#puzzles and counts how many solutions each has for nuts sized 5-13
def number_5():
    global n
    for x in range(5, 13):
        n = x
        zeroSol = 0
        oneSol = 0
        multSol = 0
        size = 1000
        before = time.time()
        puzzles = uniquePuzzles(size)
        i = 0
        for puzzle in puzzles:
            solutions = []
            counting([], puzzle, solutions)
            if len(solutions) == 0:
                zeroSol += 1
            elif len(solutions) == 1:
                oneSol += 1
            else:
                multSol += 1
            i += 1
            if x > 8 and i%100 == 0:
                progress = (time.time() - before)
                print 'It has been', progress,'\bs since starting', x

        after = time.time()
        total = after-before
        print 'For',size, 'puzzles of', n, 'sides there are: '
        print zeroSol, 'with no solutions'
        print oneSol, 'with one solution'
        print multSol, 'with more than one solution \n Found in',total,'seconds\n'

# Makes 'total' number of unique puzzles; used in number 5 to make sure there
# aren't duplicate puzzles tainting the count
def uniquePuzzles(total):
    global n
    puzzles = []
    while len(puzzles) < total:
        cur = generate()
        cur.sort()
        while cur in puzzles:
            cur = generate()
            cur.sort()
        puzzles.append(cur)
    return puzzles


#Returns the number of solutions for a particular puzzle (nuts)
def countSol(nuts):
    solutions = []
    counting([], nuts, solutions)
    return len(solutions)

#Compares the speeds of the brute force vs the pruned solution for the same
#puzzle
def compare(nuts):
    before = time.time()
    brute_solve([], nuts)
    between = time.time()
    prune_solve([], nuts)
    after = time.time()

    print 'SPEEDS'
    print 'Brute: ', between - before
    print 'Prune: ', after - between

#Uses the same method as prune, but instead of returning the first solution it
#finds all of the solutions and puts them into a list that was created before
def counting(placed, need, solutions):
    left = len(need)

    if left > 0:
        if prune_check(placed):
            for i in range(0, left):
                cur = need[i]
                temp_placed = list(placed)
                temp_placed.append(cur)
                temp_need = list(need)
                temp_need.remove(cur)
                solution = counting(temp_placed, temp_need, solutions)
    else:
        if check_solution(placed):
            solutions.append(placed)

#Recurses in the same way as brute, but checks after each additional nut if it
#can make a solution
def prune_solve(placed, need):
    left = len(need)

    if left > 0:
        if prune_check(placed):
            for i in range(0, left):
                cur = need[i]
                temp_placed = list(placed)
                temp_placed.append(cur)
                temp_need = list(need)
                temp_need.remove(cur)
                solution = prune_solve(temp_placed, temp_need)
                if solution != None: #Check so that it doesn't stop prematurely
                    return solution

    else:
        if check_solution(placed):
            print 'Solution: '
            for nut in placed:
                print nut
            return placed

#Checks if an incomplete puzzle can be solved based on what is already placed.
# Only needs to check most recently placed nut, because if it made it this far
# all other edges match.
def prune_check(placed):
    global n
    num_down = len(placed)
    cur_num = num_down-1 #This is the most recently placed nut

    # If only the center is placed or nothing is placed, there are legal moves
    if num_down < 2:
        return True

    cntr = placed[0]
    nxt = next(cur_num, cntr)
    prv = prev(cur_num, cntr)
    cur = placed[cur_num]
    cur_ind = cur.index(cur_num)

    if nxt < num_down:
        nxt_n = placed[nxt]
        nxt_ind = nxt_n.index(nxt)
        if cur[(cur_ind - 1)%n] != nxt_n[(nxt_ind + 1)%n]:
            return False
    else:
        if cur[(cur_ind - 1)%n] == cntr[(cntr.index(cur_num) + 1)%n]:
            return False

    if prv < num_down:
        prv_n = placed[prv]
        prv_ind = prv_n.index(prv)
        if cur[(cur_ind + 1)%n] != prv_n[(prv_ind - 1)%n]:
            return False
    else:
        if cur[(cur_ind + 1)%n] == cntr[(cntr.index(cur_num) - 1)%n]:
            return False


    # If it gets to the end, there are still legal moves
    return True

# Recursively adds nuts so that it creates a unique permutation and checks if that
# permutation works, returns if it does and keeps going if not
def brute_solve(placed, need):
    global count, max_perm

    left = len(need)
    if left > 0:
    # Adds another nut to the potential solution, recurses, then when that
    # returns put it back in the list so the for loop grabs the correct nut
    # the next time
        for i in range(0, left):
            cur = need[i]
            temp_placed = list(placed)
            temp_placed.append(cur)
            temp_need = list(need)
            temp_need.remove(cur)
            solution = brute_solve(temp_placed, temp_need)
            if solution != None: #Check so that it doesn't stop prematurely
                return solution

    else:
        # If the 'need' list is empty, that means all nuts are placed so it can
        # be checked to see if it passes
        count += 1
        if check_solution(placed):
            # print 'Solution found on try', count
            # for nut in placed:
            #     print nut
            return placed
        #Checks if that permutation is the last possible; syas so if it was and
        #Still didn't pass
        if count == max_perm:
            # print "No Solution for:"
            # for nut in placed:
            #     print nut
            # print "Tried", count, "ways"
            return None

#Checks a solution to see if it works
def check_solution(nuts):
    global n, count
    cntr = nuts[0]
    # print 'TEST ', count

    for i in range(1,n+1):

        cur_nut = nuts[i]  # Nut that matches the 'i' on the center one
        cur_edge = cur_nut.index(i) #Index of the i edge on the nut

        # Checks if clockwise edges match return false if they don't
        nex = next(i, cntr)
        nex_nut = nuts[nex] # Nut clockwise to cur
        nex_edge = nex_nut.index(nex)
        # print 'index', (cur_edge - 1)%n, 'of nut', i, 'vs index', (nex_edge + 1)%n, 'of nut', nex

        if cur_nut[(cur_edge - 1)%n] != nex_nut[(nex_edge + 1)%n]:
            return False

    #If it made it through the whole loop, they all matched!
    return True

# Used to find next number since need to look in order of how the occur on the
# center nut
def next(i, cntr):
    global n
    index = cntr.index(i)
    return cntr[(index+1)%n]
def prev(i, cntr):
    global n
    index = cntr.index(i)
    return cntr[(index-1)%n]

# Makes the n+1 nuts with n sides; shuffles and then rotates to 1 in first
# position to check if they're unique under rotation. When it finds a new one,
# adds it
def generate():
    global n
    nuts = []
    for x in range(n+1):
        cur = []
        for i in range(1,n+1):
            cur.append(i)
        while cur in nuts:
            random.shuffle(cur)
            while cur[0] is not 1:
                firstDig = cur[0]
                cur.remove(firstDig)
                cur.append(firstDig)
        nuts.append(cur)
    return nuts

#Factorial for knowing if it's possible to solve
def fact(acc, n):
    if n > 1:
        return fact(acc*n, n-1)
    else:
        return acc

MAIN()
