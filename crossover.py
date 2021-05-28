import random 
import numpy as np
from operator import is_
from copy import deepcopy

from setup import Setup
from candidate import Candidate

random.seed()

class Crossover(Setup):
   #This class will support in the crossover process by mixing 2 parents candidates expecting to get a fitter child candidate 
   def __init__(self):
      Setup.__init__(self)

   def crossover(self, p1, p2):
      #Create 2 new child candidates by crossing over parents 
      offsp1, offsp2 = Candidate(), Candidate()
      #Copy parents before manipulation
      offsp1.values = deepcopy(p1.values)
      offsp2.values = deepcopy(p2.values)

      #Get a random number [0,1] and compare against the crossover rate
      r = random.uniform(0, 1) 
            
      #Verify crossover rate & start the process (otherwise crossover won't happen)
      if (r < self.Crate):
         co_point1, co_point2 = 0,0
         #Checking if points are the same and iterate until a difference is found
         while(co_point1 == co_point2):
             #Crossover must have at least 1 row (and at most Ns-1) rows
             co_point1, co_point2 = random.randint(0, self.Ns-1),random.randint(1, self.Ns)
         
         #Ordering the croosover points and swapping when needed (p2->p1 | oldp1->p2)
         if(co_point1 > co_point2): (co_point1,co_point2)=(co_point2,co_point1)
         
         #Iterate over offsprints and route the process according to the type defined at every generation (Arithmetic, Cycle, PMX)
         for i in range(co_point1, co_point2):
            if self.CType==1:
               offsp1.values[i], offsp2.values[i] = self.arithmetic_co(offsp1.values[i], offsp2.values[i])
            elif self.CType==2:
               offsp1.values[i], offsp2.values[i] = self.cycle_co_upd(offsp1.values[i], offsp2.values[i])
            else:
               offsp1.values[i], offsp2.values[i] = self.pmx_co(offsp1.values[i], offsp2.values[i])
            
      return offsp1, offsp2

   ###Code brought from Dave's Library###
   def cycle_co(self, p1, p2):
      # Offspring placeholders - None values make it easy to debug for errors
      offspring1 = [None] * len(p1)
      offspring2 = [None] * len(p1)
      # While there are still None values in offspring, get the first index of
      # None and start a "cycle" according to the cycle crossover method
      while None in offspring1:
        index = np.where(np.vectorize(is_)(offspring1, None))[0][0]
        #alternate parents between cycles beginning on second cycle
        if index != 0: p1, p2 = p2, p1
        val1 = p1[index]
        val2 = p2[index]
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = np.where(p1==val2)[0][0]
        # In case last values share the same index, fill them in each offspring
        offspring1[index] = p1[index]
        offspring2[index] = p2[index]

      return offspring1, offspring2

   def cycle_co_upd(self, p1, p2):
      iter = 0
      offspring1 = [None] * len(p1)
      offspring2 = [None] * len(p1)
      remaining = list(range(1,self.Ns+1))
      #While child rows not complete
      while((None in offspring1) and (None in offspring2)): 
         #Assign next unused value
         index = self.get_unused(p1, remaining)
         val1 = p1[index]
         remaining.remove(p1[index])
         val2 = p1[index]
         if(iter % 2 == 0):  #Even cycles
            offspring1[index],offspring2[index] = p1[index],p2[index]
            while(val2 != val1): #While cycle not done
               index = self.get_value(p1, val2)
               offspring1[index] = p1[index]
               remaining.remove(p1[index])
               offspring2[index] = p2[index]
               val2 = p2[index]
         else: #Odd cycle - Flip values
            offspring1[index],offspring2[index] = p2[index],p1[index]
            while(val2 != val1):  #While cycle not done
               index = self.get_value(p1, val2)
               offspring1[index] = p2[index]
               remaining.remove(p1[index])
               offspring2[index] = p1[index]
               val2 = p2[index]
         iter += 1
      
      return offspring1, offspring2  
         
   def arithmetic_co(self, p1, p2):
      # Offspring placeholders - None values make it easy to debug for errors
      offsp1 = [None] * len(p1)
      offsp2 = [None] * len(p1)

      # Get a value for alpha between 0 and 1
      r = np.random.uniform(0,1)
      # Take weighted sum of two parents, invert alpha for second offspring
      for i in range(len(p1)):
         offsp1[i] = p1[i] * r + (1 - r) * p2[i]
         offsp2[i] = p2[i] * r + (1 - r) * p1[i]

      return offsp1, offsp2

   def pmx_co(self, p1, p2):
      # Sample 2 random co points
      co_points = random.sample(range(len(p1)), 2)
      co_points.sort()

      def PMX(x, y):
         # Create placeholder for offspring
         o = [None] * len(x)
         # Copy co-segment into offspring
         o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

         # Find set of values not in offspring from co segment in P2
         z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

         # Map values in set to corresponding position in offspring
         for i in z:
               temp = i
               idtmp = np.where(y==temp)[0][0] #index where temp is @ y
               #try:
               index = np.where(y==x[idtmp])[0][0] #get the index (on y) from the given position is @ x
               while o[index] != None:
                  temp = index
                  index = np.where(y==x[temp])[0][0]
               o[index] = i
         # Fill in remaining values
         while None in o:
               index = o.index(None)
               o[index] = y[index]
         return o
      #Call function twice with parents reversed
      return (PMX(p1, p2), PMX(p2, p1))
   
   def get_unused(self, parent_row, remaining):
      for i in range(0, len(parent_row)):
         if(parent_row[i] in remaining):
            return i

   def get_value(self, parent_row, value):
      for i in range(0, len(parent_row)):
         if(parent_row[i] == value):
            return i