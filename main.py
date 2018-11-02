%reload_ext autoreload
%autoreload 2

# Select directory and file_name
directory = '<INSERT_DIRECTORY'
file_name = '<INSERT_NAME>.csv'

from util import run_programme as run_util
from author_name_disambiguator import run_programme as run_name_disambiguator
from rcr_aggregator import run_programme as run_rcr_aggregator

(authors, author_RCRs, author_lists) = run_util(directory, file_name)
(unambiguous_authors, unambiguous_author_lists) = run_name_disambiguator(directory, file_name, authors, author_lists)
rcr_results = run_rcr_aggregator(directory, file_name, unambiguous_authors, author_RCRs)

rcr_results
