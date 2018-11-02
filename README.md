# Author-Name-Disambiguator

### Description 
This repository provides Python code to disambiguate author names using fuzzy matching and a

. The code pulls in author names from publications, generates all possible combinations and uses fuzzy matching to flag names which may be the same for example John Smith and J Smith. Part-way through the programme there is an optional pause for the user to manually validate the matches if required. A more effective approach could be to use relational machine learning as discussed here: https://ieeexplore.ieee.org/document/7891792.

### Directions on use
1) Save spreadsheet containing publications and RCR sores as a CSV file.
2) Ensure author field is marked 'Author' and RCR field is marked 'RCR'.
3) Update the code below with correct directory and file_name.
4) Run code. Respond to prompts. Code can analyse all authors or first and last author only.



