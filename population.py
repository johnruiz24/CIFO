import random
import numpy as np

from setup import Setup
from candidate import Candidate

random.seed()

class Population(Setup):
    #Inherting the configuration from setup
   def __init__(self):
      Setup.__init__(self)
      self.candidates = []

   def representation(self, input):
      n = 0
      self.candidates = []       
      #Instantiate a candidate object to get the set of possible values across every cell
      oInitial = Candidate()
      oInitial.values = [[[] for j in range(self.Ns)] for i in range(self.Ns)]
      
      #For every row and column iterate each given number
      for r in range(self.Ns): 
         for c in range(self.Ns): 
            for nbr in range(1, self.Ns+1):
               if (input.check_unique_number(r, c, nbr) and input.values[r][c]==0):
                  #The value can then be appended to the candidate solution
                  oInitial.values[r][c].append(nbr)
               elif (input.values[r][c] != 0):
                  #Value given from file
                  oInitial.values[r][c].append(input.values[r][c])
                  break
      
      #Generates a set of different candidates
      while n<self.Nc:
         #Refresh the object before to each candidate generation
         oCandidate = Candidate()
         for i in range(self.Ns):
            row = np.zeros(self.Ns)
            for j in range(self.Ns):
               #Check if value is already given and update the 
               if input.values[i][j]!= 0:
                  row[j] = input.values[i][j]  
               elif input.values[i][j] == 0:
                  row[j] = oInitial.values[i][j][random.randint(0, len(oInitial.values[i][j])-1)]
            #Keep iterating until a final matrix is built 
            while(len(list(set(row)))!= self.Ns):
               for j in range(self.Ns):
                  if(input.values[i][j] == 0):
                     row[j] = oInitial.values[i][j][random.randint(0, len(oInitial.values[i][j])-1)]
            oCandidate.values[i] = row
         self.candidates.append(oCandidate)
         n+=1
      
      #Compute the fitness of all candidates in the population
      self.compute_fitness()
      
   def compute_fitness(self):
      for candidate in self.candidates:
         candidate.compute_fitness()
      return
   
   def sort(self):
      #Sorting the population based on fitness this will then be used to narrow down the fittest solutions as part of ellitism 
      self.candidates = sorted(self.candidates, key=lambda f: f.fitness, reverse=True)
      return