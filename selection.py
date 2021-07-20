import random
import numpy as np
from operator import attrgetter
from candidate import Candidate

random.seed()

class Selection(Candidate):
    def __init__(self):
        Candidate.__init__(self)

    def manage_selection(self, candidates):
        #This function routes the types of selection methods for population selection the ouput (set of individuals) will be pushed towards the stage 
        choice=np.random.choice(np.arange(1,4),replace=False) 
        if choice==1:
            return self.tournament(candidates)
        elif choice==2:
            return self.rank(candidates)
        else:
            return self.fps(candidates)

    def tournament(self, candidates):
        c1 = candidates[random.randint(0, len(candidates)-1)]
        c2 = candidates[random.randint(0, len(candidates)-1)]
        f1, f2 = c1.fitness, c2.fitness

        #Find the fittest and the weakest.
        (fittest, weakest) = (c1, c2) if f1 > f2 else (c2, c1)
        
        selection_rate = 0.85
        r = random.uniform(0, 1)

        return fittest if (r<selection_rate) else weakest

    def rank(self, candidates):
        candidates.sort(key=attrgetter('fitness'))
        # Sum all ranks
        total = sum(range(self.Nc+1))
        #Get random position
        spin = random.uniform(0, total)
        position = 0
        # Iterate until spin is found
        for count, individual in enumerate(candidates):
            position += count + 1
            if position > spin:
                return individual
        return 

    def fps(self, candidates):
        """Fitness proportionate selection implementation
        Args: candidates or called on this work as population: The population we want to select from
        Returns: Individual: selected individual.
        """
        #if optimization == 'max':
        total_fitness = sum([i.fitness for i in candidates])
        #Get a 'position' on the wheel
        spin = random.uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in candidates:
            position += individual.fitness
            if position > spin:
               return individual
