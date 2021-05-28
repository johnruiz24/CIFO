import random
import numpy as np
import pandas as pd
from copy import deepcopy
from datetime import datetime

from tqdm import tqdm
from setup import Setup
from mutation import Mutation
from crossover import Crossover
from selection import Selection
from population import Population
from candidate import Input, Candidate

random.seed()

class Sudoku(Setup):
    def __init__(self):
      Setup.__init__(self)
      self.input = []
      self.generation_fitness = []
      self.df=pd.DataFrame([])
    
    def upload(self, path):
        self.df = pd.read_csv(path,index_col=0).reset_index()
        print('Loading the data')
        self.input = [Input(np.fromstring(self.df.iloc[i,1], dtype=int, sep=chr(32)).reshape(self.Ns, self.Ns)) for i in tqdm(range(len(self.df)))]
        return self.input

    def set_metrics(self, index, **metrics):
        for key,value in metrics.items(): 
            self.df.at[index,key]=value
        return self.df.to_csv(self.Path)

    def check_solution(self, *param):
        #param[0] -> index | param[1] -> generation | param[2] -> population | param[3] -> best generation fitnesses
        dStart=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'Generation #{param[1]}')
        best_fitness = 0.0
        for c in range(self.Nc):
            fitness = param[2].candidates[c].fitness
            if(fitness==1):
                solution = param[2].candidates[c].values
                print(f'Solution Found at Generation #{param[1]} :\n {solution}')
                dEnd=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                #Update statistics summary
                self.set_metrics(param[0],**{'Generation':param[1], 'Fitness':fitness, 'Start Time':dStart, 'End Time':dEnd, 'Candidate Fitnesses':chr(32).join(map(str,param[3]))})
                best_fitness=fitness
                break
            #Find the best fitness
            if(fitness > best_fitness): best_fitness = fitness
        return best_fitness, fitness

    def solve(self, *args):
        #Create an initial population
        self.population = Population()
        #Pass on the set of values to get the set of candidate solutions
        self.population.representation(args[1])

        #Process generations
        dInit=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') #Getting the timestart before any iteration (in case no solution was found this variable will be used)
        for generation in range(self.Ng):  
            #Check solution & return the best fitness and its value associated
            best_fitness, fitness = self.check_solution(args[0], generation, self.population, self.generation_fitness)
            print(f'Best Fitness -> {best_fitness}')
            self.generation_fitness.append(np.round(best_fitness,2))
            #if a solution has been found end the iteration on the current generation and push towards the next one
            if best_fitness==1:
                #clean before next generation
                self.generation_fitness = []
                return 
            
            #Set a range to route the crossover process defining whether it's aritmethic or cycle or PMX
            #As the PMX has retrieved better results in terms of speed we're giving a higher chance a PMX to happen
            self.CType=np.random.choice(np.arange(1,4), 1, p=[0.2, 0.35, 0.45])

            #Create the next population 
            self.next_population = []
            #Select elites (the fittest candidates) and preserve them for the next generation
            self.population.sort()
            elites = []
            for e in range(self.Ne):
                oElite = Candidate()
                oElite.values = deepcopy(self.population.candidates[e].values)
                elites.append(oElite)
            
            #Create the rest of the candidates
            for _ in range(self.Ne, self.Nc, 2):
                #Select parents from population via any selection method (FPS, Rank, Tournament)
                oSelection = Selection()
                p1 = oSelection.manage_selection(self.population.candidates) 
                p2 = oSelection.manage_selection(self.population.candidates)

                #Cross-Over this method apply cycle_crossover
                offspring1, offspring2 = Crossover().crossover(p1, p2)

                #Start Mutation (offpsring1 & offspring2) -> these 2 will be passed as parameters
                oMutation = Mutation()
                old_fitness=0 if offspring1.fitness is None else offspring2.fitness
                #Passig the values of the child1
                success = oMutation.mutate(offspring1.values, args[1])
                #Update fitness before to compare with the previous fitness (from crossover)
                offspring1.compute_fitness()
                if(success):
                    #Update the number of mutations and phi related to the success rate of mutations
                    if(offspring1.fitness > old_fitness): self.Phi+= 1
                    self.Nm += 1
            
                old_fitness=0 if offspring2.fitness is None else offspring2.fitness
                success = oMutation.mutate(offspring2.values, args[1])
                #Update fitness after mutation§
                offspring2.compute_fitness()
                if(success):
                    #Update the number of mutations and phi related to the success rate of mutations
                    if(offspring2.fitness > old_fitness): self.Phi+= 1
                    self.Nm+= 1
                #Add children to new population
                self.next_population.extend([offspring1,offspring2])

            #Append elites into the end of the population. These will not have been affected by crossover or mutation
            for e in range(self.Ne): self.next_population.append(elites[e])

            #Select next generation.
            self.population.candidates = self.next_population
            self.population.compute_fitness()

            #Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule) that meassures the strenght in the mutation process
            #This is to avoid an overexcess of mutation as the fitness progresses towards unity
            self.Phi = 0 if self.Nm==0 else self.Phi/self.Nm
            
            if(self.Phi >0.2): self.Sigma = self.Sigma/0.98
            elif(self.Phi <0.2): self.Sigma = self.Sigma*0.98

            #Before to move on with the next generation update mutation rate and its attributes
            self.Mr = abs(np.random.normal(loc=0.0, scale=self.Sigma, size=None))
            self.Nm, self.Phi  = 0,0

            #Sort and check for stale population if so then get the 2 fittest candidates 
            self.population.sort()
            self.Stale = 0 if(self.population.candidates[0].fitness != self.population.candidates[1].fitness) else self.Stale+1

            #Re-seed the population if 30 generations(3%) have passed with the fittest two candidates always having the same fitness
            if(self.Stale >= 30):
                print('Re-seeding')
                self.population.representation(args[1])
                self.reset_settings()
            
        print('No Solution Found')
        dEnd=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.set_metrics(args[0],**{'Generation':generation, 'Fitness':fitness, 'Start Time':dInit, 'End Time':dEnd, 'Candidate Fitnesses': chr(32).join(map(str,self.generation_fitness))})
        return None