import numpy as np
import pandas as pd
from setup import Setup
from datetime import datetime
from matplotlib import pyplot as plt

class Draw(Setup):
    def __init__(self):
        Setup.__init__(self)

    def plot_save_fitness(self):
        #Get the data
        df=pd.read_csv(self.Path)

        for i in range(len(df)):
            try:
                #Get fitness per generations
                fitness=np.fromstring(df.iloc[i,-1], dtype=float, sep=chr(32))
                #Check if solution has found a fitness then 1 must be on the array otherwise append to the last position
                #This is because when getting the statistics the last fitness was not appended
                if df.loc[i,'Fitness'] not in fitness:
                   fitness=np.append(fitness, [df.loc[i,'Fitness']])
                #Get generations
                #generation = np.arange(0,int(df.loc[i,'Generation'])+1)
                generation = np.arange(0,np.size(fitness))
                #Get puzzle complexity
                name=df.loc[i,'index']
                #Update path for image storing
                nPath=chr(47).join(self.Path.split('/')[:-1])
                tot = datetime.strptime(df.iloc[i,5], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(df.iloc[i,4], '%Y-%m-%d %H:%M:%S.%f')
                plt.title(f'Sudoku Fitness Landscape : {name}') 
                plt.xlabel('Generation') 
                plt.ylabel('Fitness') 
                plt.plot(generation,fitness, label=f'Time: {tot.total_seconds()} sec')
                plt.legend(loc='best')
                #Save image
                plt.savefig(f'{nPath}/{name}.png', dpi=300, bbox_inches='tight')
                plt.show()
            except TypeError:
                pass

#Draw().plot_save_fitness()