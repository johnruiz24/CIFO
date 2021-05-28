import numpy as np
import pandas as pd

from tqdm import tqdm
from time import sleep
from setup import Setup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Generator(Setup):
    #Class for webscrapping the data according to different levels of difficulty filled in by the user
    def __init__(self):
        Setup.__init__(self)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument('disable-gpu')
        self.data=pd.DataFrame([])
        return
    
    def get_sudoku_data(self,args):
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.options)
        driver.get(self.Url)
        element = driver.find_element_by_id('level_field').find_elements_by_name('auswahl_level')
        draw = driver.find_element_by_id('mode_field').find_elements_by_id('button1')
        for idx,option in enumerate(tqdm(element)): #iterate over different level of complexities
            while args[idx]>0: #generate puzzle n times
                aSudoku=[]
                option.click()
                for d in draw: 
                    d.click() #click on each of the elements 
                    sleep(2) #sleep as the website has a delay before to come up with a new puzzle
                    for e in driver.find_element_by_id('virtual_feld').find_elements_by_class_name('eing'):
                        id=e.get_attribute('id')
                        value=driver.find_element_by_id(id.replace(id[0],'I')).get_attribute('value')
                        aSudoku.append(0 if value=='' else int(value))
                self.data[f'{self.Complex[idx]} {args[idx]}']=np.ravel(np.array(np.array(aSudoku).reshape(self.Ns,self.Ns)).reshape((3,3,3,3)).transpose((0,2,1,3)).reshape(self.Ns,self.Ns))
                args[idx]-=1
        #Transpose dataframe
        self.data=self.data.T
        return self.data[self.data.columns].apply(lambda i: chr(32).join(i.values.astype(str)), axis=1)
    
    def message(self):
        return print('Sudoku Generator...','Input the number of puzzles by complexity from 0-10','=========================================================',sep='\n')