# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:25:08 2024

@author: user2
"""

import pandas as pd

def remove_duplicates(input_file,output_file):
    data = pd.read_csv(input_file)
    
    unique_data = data.drop_duplicates(subset='id', keep='first')
    
    unique_data.to_csv(output_file, index=False)
    
remove_duplicates('games.csv','games_noduplicate.csv')