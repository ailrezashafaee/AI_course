from heapq import heappush, heappop
import copy
from select import select
actions = ["up" , "left" , "down", "right"]
class State:
    def __init__(self , before,puzzle,h, g, emptyX,emptyY,prevAction):
        #keeping before for print#
        self.before = before
        self.puzzle = puzzle
        self.h = h
        self.g = g
        self.emptyX= emptyX     
        self.emptyY= emptyY  
        self.action = prevAction
    def getFscore(self):
        return self.h + self.g
    def __lt__(self, next):
        #f  = h + g for comparison in queue #
        return  self.g + self.h < next.g + next.h
def Print(state,n):
    if state ==None:
        return
    else:
        Print(state.before,n)
        print(state.action)
        for i in range(n):
            for j in range(n):
                print(state.puzzle[i][j] ,end=' ')
            print("")
        print(state.getFscore())
        print("")
        
def move(x,y,action):
    if(action =="right" or action == 'r'):
        return x , y+1
    if(action == "down" or action == 'd'):
        return x+1,y
    if(action == "left" or action == 'l'):
        return x , y-1
    if(action == "up" or action == 'u'):
        return x-1 , y
def searchTile(tile, goal,n):
    for i in range(n):
        for j in range(n):
            if(goal[i][j] ==tile):
                return i , j
    print("error in SearchTile, can't find the tile in goal puzzle")
def manhattanH(puzzle,goal,n):
    #h function#
    cost = 0
    for i in range(n):
        for j in range(n):
            gx,gy = searchTile(puzzle[i][j],goal,n)
            gx = abs(gx-i)
            gy = abs(gy - j)
            cost += gy + gx
            #finding the manhattan distance of a tile 
    return cost
def doAction(before,goal,newEmptyX,newEmptyY,n,action):
    newPuzzle = copy.deepcopy(before.puzzle)
    newPuzzle[before.emptyX][before.emptyY] = before.puzzle[newEmptyX][newEmptyY]
    newPuzzle[newEmptyX][newEmptyY] = before.puzzle[before.emptyX][before.emptyY]
    cost = manhattanH(newPuzzle,goal,n)
    newState = State(before , newPuzzle , cost , before.g + 1,newEmptyX , newEmptyY,action)
    return newState
def NPuzzle(start, goal ,emptyX , emptyY,n):
    lQueue = [] #heap queue#
    root = State(None, start ,manhattanH(start , goal , n),0 ,emptyX , emptyY,"Start!")
    heappush(lQueue,root)
    while True:
        #finding min f = g + h with the help of heap #
        minF = heappop(lQueue)
        if minF.h ==0:
            #we sovled the puzzle#
            Print(minF,n)
            return
        # we should make states by doing actions (moving empty tile) : #
        #top#
        for i in actions:
            newX , newY = move(minF.emptyX,minF.emptyY,i)
            #checking if that action is possible : #
            if(newX >= 0 and newX < n and newY >= 0 and newY < n):
                newState = doAction(minF,goal,newX,newY,n,i)
                heappush(lQueue,newState)
def matrixInput(n):
    matrix = []
    for i in range(n):
       row = list(map(int, input().split()))
       matrix.append(row)
    print(matrix)
    return matrix
n = int(input("enter the size of puzzle:"))
emptyTile =int(input("enter your empty tile number : "))

print("pleas enter your puzzle matrix:")
puzzle = matrixInput(n)
print("please enter your goal matrix:")
goal = matrixInput(n)
for i in range(n):
    for j in range(n):
        if(puzzle[i][j] == emptyTile):
            emptyX = i
            emptyY = j
NPuzzle(puzzle,goal,emptyX,emptyY,n)



        