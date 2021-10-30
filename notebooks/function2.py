
import pandas as pd
import numpy as np

def load_and_process(url_or_path_to_csv_file):
    
    data = pd.read_csv(url_or_path_to_csv_file)
    
    df1 = (
       data
            
            .drop(['ID','name','category','currency','deadline','launched','backers','pledged','goal','usd pledged','country'],axis=1)
        
            .drop(data[(data.state != 'successful') & (data.state != 'failed')].index)
        
            .assign(Amtdiff = data.usd_pledged_real - data.usd_goal_real)
        
            .fillna({'Amtdiff':0})
        
            .rename(columns={'main_category': 'Category','state': 'Success','usd_pledged_real': 'Pledged', 'usd_goal_real': 'Goal', 'Amtdiff': 'Amount Difference'})
        
            .reset_index(drop=True)
            
        )
        
    return df1
