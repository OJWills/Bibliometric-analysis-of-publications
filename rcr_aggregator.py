import os
import pandas as pd

def build_dataframe(unambiguous_authors, author_RCRs):
    """
    Builds dataframe with unique authors and associated RCRs for each paper
    Input: Author and RCR lists
    Output: Dataframe
    """
    
    df1 = pd.DataFrame({'Author':unambiguous_authors,'RCR':author_RCRs})

    return df1

def aggregate_RCRs(df1, directory):
    """
    Aggregates RCRs, counting number of authors and summing RCR score
    Input: Dataframe and file directort
    Output: Final dataframe
    """

    #Could consider methods of imputation for RCR values of NaN
    df1.loc[(df1.RCR >3.45), 'Paper > 3.45'] = 1
    #print(df1)
    
    df1['No. of papers'] = df1.groupby('Author')['Author'].transform(pd.Series.value_counts) #count papers
    df1['No. papers RCR > 3.45'] = df1.groupby('Author')['Paper > 3.45'].transform('sum')
    df1['Total RCR'] = df1.groupby('Author')['RCR'].transform('sum') # sum RCRs
    df1['Median RCR'] = df1.groupby('Author')['RCR'].transform('median')
    df1['Max RCR'] = df1.groupby('Author')['RCR'].transform('max')
    df1['Min RCR'] = df1.groupby('Author')['RCR'].transform('min')
    
    df1 = df1.drop_duplicates(subset = ['Author', 'Total RCR', 'No. of papers', 'No. papers RCR > 3.45']) # drop duplicates
    df1 = df1.sort_values(by=['Total RCR'], ascending = False) #sort by score to make it easier (highest matches first)
    df1 = df1.loc[:, ['Author','No. of papers','Total RCR', 'Max RCR', 'Min RCR', 'Median RCR', 'No. papers RCR > 3.45']]
    
    file_path = os.path.join(directory, 'final_results.csv')
    df1.to_csv(file_path, encoding='latin1', index=False)
    return df1 

def run_programme(directory, file_name, unambiguous_authors, author_RCRs):
    df1 = build_dataframe(unambiguous_authors, author_RCRs)
    aggregated_scores = aggregate_RCRs(df1, directory)
    print("Please check your directory for the full named 'final_results.csv'")
    return aggregated_scores 
