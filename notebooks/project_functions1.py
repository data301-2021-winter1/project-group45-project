import pandas as pd
import numpy as np
pd.set_option('use_inf_as_na', True)

def load_and_process(url_or_path_to_csv_file):
    
    data = pd.read_csv(url_or_path_to_csv_file)
    
    df1 = (
        data
        #Converting both datetime columns from string -> datetime + Removing the time section from launched datetime (not nearly as feasible using method chains)
        .assign(Launched = pd.to_datetime(data.launched).dt.normalize())
        .assign(Deadline = pd.to_datetime(data.deadline).dt.normalize())
    )
    
    
    df2 = (
        df1
        
        #Drop unused / duplicate columns
        .drop(['ID', 'name', 'category', 'goal', 'pledged', 'usd pledged', 'launched', 'deadline'], axis=1)
        
        #Drops any rows that didn't result in an explicit project success or failure (canceled, live, undefined, suspended)
        .drop(df1[(df1.state != 'successful') & (df1.state != 'failed')].index)
        
        # Inserts a new column that calculates the average amount pledged per person in a project by dividing (usd_pledged_real / backers)
        .assign(AvgPledged = df1.usd_pledged_real / df1.backers)
        
        # Inserts a new column that calculates duration of the project in days by subtracting (deadline - launched)
        .assign(Duration = (df1.Deadline - df1.Launched).dt.days)
        
        # Fixes divide by zero outputting NaN in the avg_pledged column and replaces with 0
        .fillna({'AvgPledged':0})
        
        #Rename columns
        .rename(columns={'main_category': 'Category', 'currency': 'Currency', 'state': 'Success', 'backers': 'Supporters', 'country': 'Country', 'usd_pledged_real': 'Pledged', 'usd_goal_real': 'Goal'})
        
        #Resets all indexes since we deleted rows
        .reset_index(drop=True)
    )
    
    return df2