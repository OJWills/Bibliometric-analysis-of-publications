# Bibliometric analysis of publications

### Description 
This repository provides Python code to identify influential researchers from an input file of publications by aggregating Relative Citation Ratio (RCR) scores. The RCR is a field-normalised citation metric which can be calculated by using the following tool https://icite.od.nih.gov/ or by downloading papers from UberResearch. The code takes an input csv file containing authors, publications and RCR scores and converts it to an output dataframe consisting of unique authors and their aggregated RCR scores including total, max, min and median RCR. The tool is useful for rapidly identifying influential researchers and could be used to develop tools for peer review.

### Prerequisites
Pandas, fuzzywuzzy, itertools

### Directions on use
1) Save spreadsheet containing publications and RCR sores as a CSV file.
2) Ensure author field is marked 'Author' and RCR field is marked 'RCR'.
3) Update the main.py file with correct directory and file_name.
4) Run mian.py. Respond to prompts. Code can analyse all authors or first and last author only.
