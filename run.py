import pandas as pd
from plot import Draw
from setup import Setup
from sudoku import Sudoku
from create import Generator

draw = Draw()
setup = Setup()
sudoku = Sudoku()
generator = Generator()

#Scrapping the data
#==========================
#1.Download the data from internet
#2.Save the data into the 'data' folder
generator.message()
pd.DataFrame(generator.get_sudoku_data(list(map(lambda i: int(input(f'{i}: ')),generator.Complex))),columns=['Data']).to_csv(sudoku.Path)

#Loading the data
#==========================
sudoku.upload(sudoku.Path)

#Solving the Set of Puzzles
#==========================
#1.Run GA algorithms
#2.Choose solutions according to the type of maximization or miminization
#3.Update statistically summary
#4.Print solutions per generation
list(map(lambda i: sudoku.solve(i[0],i[1]), enumerate(sudoku.input)))

#Post-Processing
#==========================
#1.Plotting the fitness landscape per generation
#2.The images will be saved into the 'data' folder
draw.plot_save_fitness()
