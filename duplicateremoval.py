import pandas as pd

def remove_duplicates(input_file,output_file):
    data = pd.read_csv(input_file)
    
    unique_data = data.drop_duplicates(subset='id', keep='first')
    
    unique_data.to_csv(output_file, index=False)
    
remove_duplicates('games.csv','dataset.csv')