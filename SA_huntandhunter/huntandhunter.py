import numpy as np
import math
class State:
    def __init__(self,order):
        self.order = order
    def findNeighbor(self,graph):
        a1 = np.random.choice(self.order,1)[0]
        index = np.where(self.order ==a1)[0][0]
        for i in range(len(self.order)):
            if(graph[a1][self.order[i]] == 1 and i > index):
                self.order[index] , self.order[i] = self.order[i] , self.order[index]
                break
        
        return self.order
    def goalFunction(self,graph):
        diff = 0
        for i in range(len(self.order)):
            for j in range(len(self.order)):
                if(graph[self.order[i]][self.order[j]]==1 and i < j):
                    diff-=1
        return diff
def huntAndHunter(graph , num , T,z,start = []):
    #making a random order for start :
    start = np.random.permutation(num)
    xbest = State(start)
    while T > 0.000001:
        T=T*z
        newOrder = xbest.findNeighbor(graph)     
        xnow = State(newOrder)
        deftaF = xnow.goalFunction(graph) - xbest.goalFunction(graph)
        if(deftaF > 0):
            xbest = xnow
        elif(np.random.choice([0,1],1,True,p = [1 - math.exp(deftaF/T),math.exp(deftaF/T)])):
            xbest = xnow
            
    return xbest.order
inputfile = open("input.txt",'r')
num = int(inputfile.readline())
row = []
graph = []
for i in range(num):
    for j in range(num):
        row.append(0)
    graph.append(row)
    row = []
    
for ed in inputfile:
  ed =ed.split(' ') 
  graph[int(ed[0]) - 1][int(ed[1]) - 1] = 1
answer = huntAndHunter(graph ,num , 100000, 0.95)
for i in np.flip(answer):
    print(i+1,end=" ")

    