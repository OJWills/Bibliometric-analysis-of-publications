import os
import itertools
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def generate_author_sets(authors):
    """
    Generates a set of authors based on how names appear on papers
    Input: List of authors
    Output: List of unique authors based on how they appear
    """
    ambiguous_authors = set()
    for author in authors:
        if len(author) > 2:
            ambiguous_authors.add(author)
    
    return ambiguous_authors 

def generate_author_combinations(ambiguous_authors):
    """
    Generates combinations for all author names 
    Input: List of unique authors
    Output: List of tuples for author name combinations
    """
    ambiguous_authors_list = list(ambiguous_authors)
    pair_list = itertools.combinations(ambiguous_authors_list, 2)

    return pair_list

def generate_author_pair_scores(pair_list, directory):
    """
    Compares author names to identify variations (e.g. David Smith and D Smith)
    Input: List of all pairs of authors on papers
    Output: Dataframe with fuzzy matches for author combinations
    """
    print("Calculating pair scores ...")    
    pair_scores = [[pair[0], pair[1], fuzz.ratio(pair[0], pair[1])] for pair in pair_list] #returns list of pair_scores
    df1 = pd.DataFrame(pair_scores, columns=['name1', 'name2', 'score']) #setup dataframe
    
    df1['above_threshold'] = df1.score > 75 #fuzzy matches from 75-90 typically require validation 
    df1['author match (Y/N)'] = "" #add column for user to manually verify auhtor pairs
    df1 = df1.sort_values(by=['score'], ascending = False) #sort by score to make it easier (highest matches first)
    file_path = os.path.join(directory, 'names_to_check.csv')
    df1.to_csv(file_path, encoding='latin1', index=False) #export to users directory 
    print("Please check names above threshold in 'names_to_check.csv' file saved in your directory")
    print("Once complete please save the file in its current location") #users validates at this stage
       
    while True: 
        x = input("Please press Y to resume:")
        if x in ["y", "Y"]:
            try:
                file_path = os.path.join(directory, 'names_to_check.csv')
                cleaned_names = pd.read_csv(file_path, encoding ='latin1')
                return cleaned_names      
            except:
                print("File not found please save to directory using file name 'names_to_check.csv'")
             
def generate_pairs_of_ambiguous_authors(cleaned_names):
    """
    Generates pairs of ambiguous authors which are equivalent (e.g. David Smith and D Smith)
    Input: Dataframe including cleaned names
    Output: Returns pairs of ambiguous authors
    """
    name_pairs = cleaned_names.loc[(cleaned_names["author match (Y/N)"]=="Y")]
    name_pairs = name_pairs.filter(items=['name1', 'name2'])
    all_pairs = [list(x) for x in name_pairs.values]
    return all_pairs

def generate_dictionary_of_ambiguous_authors(all_pairs):
    """
    Generates dicitonary of related pairs
    Input: List of related pairs
    Output: Dictionary of related pairs with first initial + surname as key
    """
    
    #Note this approach is unable to distinguish between names where first initial and surname are equivalent. Refinements welcome!
    d = {}
     
    for pair in all_pairs:
        for name in pair:
            x = name.split(' ')
            last_name = x[-1]
            first_name_initial = x[0][0]
            temp_name = first_name_initial + " " + last_name
            if temp_name not in d.keys():
                d[temp_name] = [name]
            elif name not in d[temp_name]:
                d[temp_name].append(name)
        ##This code picks up conventions when middle name inital is put first on papers
        
    return(d)

def replace_ambiguous_authors(d, authors, author_lists):
    """
    Generates list of dismbiguated authors
    Input: Dictionary of related names, list of authors from paper
    Output:List of unambiguous authors with related names replaced by consistent name
    """
    
    unambiguous_authors, unambiguous_author_lists = [], []
    
    for author_list in author_lists:
        temp = []
        for author in author_list:
            x = 0
            for key in d:
                if author in d[key]:
                    temp.append(key)
                    unambiguous_authors.append(key)
                    x+=1
            if x == 0:
                temp.append(author)
                unambiguous_authors.append(author)
                
        unambiguous_author_lists.append(temp)
    
    return (unambiguous_authors, unambiguous_author_lists)

def run_programme(directory, file_name, authors, author_lists):  
    ambiguous_authors = generate_author_sets(authors)
    pair_list = generate_author_combinations(ambiguous_authors)
    cleaned_names = generate_author_pair_scores(pair_list, directory)
    all_pairs = generate_pairs_of_ambiguous_authors(cleaned_names)
    dictionary_of_ambiguous_authors = generate_dictionary_of_ambiguous_authors(all_pairs)
    (unambiguous_authors, unambiguous_author_lists) = replace_ambiguous_authors(dictionary_of_ambiguous_authors, authors, author_lists)
    return (unambiguous_authors, unambiguous_author_lists)
