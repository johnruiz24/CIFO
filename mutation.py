import random
import numpy as np
from candidate import Candidate

random.seed()

class Mutation(Candidate):
   #Mutate a candidate by choosing a row and then 2 points (that represents a column) 
   #Before to swap the elements it's required to validate whether or not consistencies on the puzzle could potentially happen
   
   #The output will be a boolean state indicating whether or not the mutation succesfully happened
   def __init__(self):
      Candidate.__init__(self)
      
   def mutate(self, offspring, input):
      success = False
      r = random.uniform(0, 1)
      #Check mutation rate
      if (r < self.Mr):  
         while(not success):
            r1 = random.randint(0, self.Ns-1)
            r2 = r1 #mutation will be applied on the same row
            #Getting two mutations points
            #mut_point[0] -> represents the current column | mutpoints[1] -> the target column 
            mut_points = np.random.choice(self.Ns-1,2,replace=False)

            #Check if two places are free
            if(input.values[r1][mut_points[0]] == 0 and input.values[r1][mut_points[1]] == 0):
               #Verify that the elements are still unique across all rows, blocks and columns (in order to stave off from breaking the sudoku rule)
               if input.check_unique_number(r2, mut_points[1], offspring[r1][mut_points[0]])\
                     and input.check_unique_number(r1, mut_points[0], offspring[r2][mut_points[1]]):
                  #Swapping values from 1 row-column to another row-column
                  (offspring[r1][mut_points[0]],offspring[r2][mut_points[1]]) = (offspring[r2][mut_points[1]],offspring[r1][mut_points[0]])
                  success = True    
      return success

   def swap_mutation(self, input):
      # Get two mutation points
      mut_points = random.sample(range(len(input)), 2)
      # Rename to shorten variable name
      i = input
      i[mut_points[0]], i[mut_points[1]] = i[mut_points[1]], i[mut_points[0]]
      return i