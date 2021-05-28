import os

class Setup():
    #Class for defining the attributes that will be used across the sudoku generation process
    def __init__(self):
        #Webscrapping parameters
        self.Path = os.path.join(os.getcwd(),'data/sdk_data.csv')
        self.Url='http://sudoku.becher-sundstroem.de'
        self.Complex=['Very Easy','Easy','Moderate','Difficult']

        #Puzzle and GA parameters
        self.Ns = 9 #Shape of the puzzle
        self.Nc = 1000 #Number of candidates
        self.Optim = 'max'
        self.Ptype = 1 #Penalization type for those solutions who have a duplicates number across any row, block or column
        
        self.Ne = 70  #Number of elites
        self.Ng = 1000  #Number of generations
        self.Stale = 0 #Number of generations in which the solution got stalled

        #Crossover & Mutation parameters
        self.Crate = 0.98 #Crossover rate set at 0.95 this is to get higher chances to apply crossover at each generation the higher the number the fastest the convergence (in average)
        self.CType = 0 #Set Croosover type per generation ('PMX','Cycle Crossover','Arithmetic')
        #there's a rate which is being constrasted previous the triggering of crossover
        self.Nm = 0  #Number of mutations
        self.Phi = 0 
        self.Sigma = 1
        self.Mr = 0.07 #Mutation Rate

    def reset_settings(self):
        self.Stale = 0
        self.Phi = 0
        self.Nm = 0
        self.Sigma = 1
        self.Mr = 0.07