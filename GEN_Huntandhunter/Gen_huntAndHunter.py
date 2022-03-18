import numpy as np
import random
import matplotlib.pyplot as plt
class Chrom:
    def __init__(self, order):
        self.order = order
    def objective(self,graph,totalCost):
        diff = 0
        for i in range(len(self.order)):
            for j in range(len(self.order)):
                if(graph[self.order[i]][self.order[j]]==1 and i < j):
                    diff+=j - i
        return  totalCost- diff
    def prob(self,sum,graph,totalCost):
        return self.objective(graph,totalCost)/sum
    def __add__(self , other):
        temp = np.random.randint(len(self.order))
        child1 = self.order[0:temp]
        child2 = other.order[0:temp]
        for i in other.order:
            if i not in child1:
                child1.append(i)
        for i in self.order:
            if i not in child2:
                child2.append(i)
        return (Chrom(child1) , Chrom(child2))  
    def mutate(self):
      ind = [i for i in range(n)]
      r = random.sample(ind, 2)
      temp = self.order.copy()
      temp[r[0]],temp[r[1]] = temp[r[1]] , temp[r[0]]
      return Chrom(temp)
    def __str__(self):
        for i in range(len(self.order)):
            self.order[i] +=1
        self.order.reverse()
        st = ""
        for i in self.order:
            st+=" " + str(i)
        return st
def best_Chrom(best_obj,pop,graph,totalCost):
    for i in pop:
        if(i.objective(graph,totalCost) == best_obj):
            return i
def checkGoal(li,graph):
        diff = 0
        for i in range(len(li.order)):
            for j in range(len(li.order)):
                if(graph[li.order[i]][li.order[j]]==1 and i < j):
                    diff-=1
        return diff
inputfile = open("input.txt",'r')
num = int(inputfile.readline())
row = []
graph = []
ploty=[]
for i in range(num):
    for j in range(num):
        row.append(0)
    graph.append(row)
    row = []
    
for ed in inputfile:
  ed =ed.split(' ') 
  graph[int(ed[0]) - 1][int(ed[1]) - 1] = 1
n = num
totalCost = 0
for i in range(n):
    for j in range(n):
        totalCost +=j
population_size = 30
max_pop_size = 50
crossover_coeff = 0.9
mutation_coeff = 0.4
max_iteration =300
num_crossover = round(population_size*crossover_coeff)
num_mutation = round(population_size*mutation_coeff)
total = population_size+num_crossover+num_mutation
population = []
best_objective = 0
while len(population) < population_size:
    temp = np.random.permutation(n).tolist()
    population.append(Chrom(temp))
ind = 0
while ind < max_iteration:
    sum = 0
    for i in population:
        sum += i.objective(graph,totalCost)
    pr = []
    temp = []
    for i in population:
        pr.append(i.prob(sum , graph,totalCost))
        temp.append(i)
    population_size = len(population)
    for i in range(0,int(num_crossover),2):    
        ch1= np.random.choice(temp,1,True ,pr)
        ch2 = ch1
        while ch1[0].order == ch2[0].order:
            ch2 = np.random.choice(temp,1,True,pr)
        (child1 , child2) = ch1[0]+ch2[0]
        population.append(child1)   
        population.append(child2)
    for i in range(num_mutation):
        temp = np.random.randint(num_crossover)
        temp = population_size + temp
        mut = population[temp].mutate()
        population.append(mut)
    ojbs = []
    for i in population:
        ojbs.append(i.objective(graph,totalCost))
    best_objective = max(ojbs)
    ploty.append(best_objective)
    bestCh = best_Chrom(best_objective,population,graph,totalCost)
    print(bestCh.objective(graph,totalCost))
    if(len(population) > max_pop_size):
        temp_population = [] 
        ojbs = []
        for i in population:
            ojbs.append(i.objective(graph,totalCost))
        args = np.argsort(ojbs)
        for i in range(max_pop_size):
            t = len(population)-1 - i
            temp_population.append(population[args[t]])
        population = temp_population
        population_size = max_pop_size
    ind+=1
    
print("conflicts : " ,checkGoal(bestCh,graph))
print("final order",bestCh)
print("best objective found:",best_objective)
plotx = [i for i in range(max_iteration)]
plt.plot(plotx, ploty)
plt.show()
