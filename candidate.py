import numpy as np
from setup import Setup
from itertools import chain                                                                                            

class Candidate(Setup):
    #Defining a set of candidates
    def __init__(self):
      Setup.__init__(self)
      #Getting the puzzle shape from setup
      self.values = np.zeros((self.Ns, self.Ns), dtype=int)
      self.fitness = None

    def compute_fitness(self):
      #To compute the fitness of a candidate solution we count how many uniquess elements are across each row,column and block and penalize those having duplicated elements
      #Those numbers will then be divided by the total number of elements that are encomprised on the puzzle (squaring the shape (Ns) to the power of 2)
      #Sum up of those 3 metrics and get the mean (was tested first then I reaize that we should strength a bit more the search of possibilities by multiplying its values leading to a lower fitness)

      def check_do_penalty(array):
          #In order to perform a deep search of fittest solutions (priorizating those which are having a fitness=1)
          #It's required to penalize those solutions with duplicated elements
          #Dividing the total distinct numbers per iteration (row,block,column) by the number of duplicates
          return np.sum(list(map(lambda x: x/(self.Ns-x+1) if self.Ptype!=0 else x/(self.Ns-x) if x!=self.Ns else x, array)))
      
      def get_block(r,c):           
         return chain(*[self.values[i][3*r:3*(r+1)] for i in range(3*c,3*(c+1))])                                               

      #Each of these elements should contains the number from 1-9 without duplicates, if this arises the solution will be penalized decreasing its fitness
      #for every row count the number of different elements 
      row = [len(set(self.values[i])) for i in range(self.Ns)]
      #divide the total number of distinct values / pow(Ns,2)
      row_mean = check_do_penalty(row)/pow(self.Ns,2)

      #for every column count the number of different elements
      column = [len(set(self.values[:,i])) for i in range(self.Ns)]
      #divide the total number of distinct values  / pow(Ns,2)
      column_mean = check_do_penalty(column)/pow(self.Ns,2)

      block = [len(set(get_block(r,c))) for r in range(int(self.Ns/3)) for c in range(int(self.Ns/3))]
      block_mean = check_do_penalty(block)/pow(self.Ns,2)

      #Calculate fitness
      #self.fitness = np.mean([column_mean,block_mean])
      self.fitness = row_mean*column_mean*block_mean
      return self.fitness

class Input(Candidate):
    #Set of rules to support the process of defining the set of candidate solutions, applying the 3 main criterias of any sudoky puzzle
    def __init__(self, values):
      #Grid with the set of webscrappred numbers 
      Candidate.__init__(self)
      self.values = values

    #Not a single number could exist more than once at any row, column or 3x(Ns/3) block
    def check_unique_number(self, row, column, value):
      #Check for uniqueness of a number on a given row and column 
      if (value in self.values[row,:]) or \
             (value in self.values[:,column]):
         return False

      #Check for uniqueness of a number on a given given block
      r = 3*(row//3)
      c = 3*(column//3)

      #Get the block and flatten it to verify the existance of the number
      if value in np.ravel(self.values[r:r+int(self.Ns/3), c:c+int(self.Ns/3)]):
         return False

      return True
