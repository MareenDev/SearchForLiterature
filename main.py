import logging
import arxiv
from pandas import DataFrame
import argparse


def parseInput():

    parser = argparse.ArgumentParser()
    parser.add_argument('--term', type=str, help='Suchbegriff', required=True)

    parser.add_argument('--max', type=float,  default=float('inf'),
                        help='Maximale Trefferanzahl')

    return parser.parse_args()


def main(args):
    logging.basicConfig(level=logging.INFO)

    search = arxiv.Search(query="ti:"+args.term, max_results=args.max,
                          sort_by=arxiv.SortCriterion.LastUpdatedDate)

    # create csv with relevant data
    wanted_result = []

    for result in search.results():
        # https://arxiv.org/category_taxonomy
        set_wanted_cats = set(['cs.CV', 'cs.CR', 'cs.LG', 'cs.AI'])
        intersect = set(result.categories).intersection(set_wanted_cats)

        if len(intersect) > 0:
            nr_papers = len(wanted_result)
        # save dataframe as a csv file with the given headers
            r = [nr_papers, result.entry_id, result.updated,
                 result.title, result.summary]            
            wanted_result.append(r)
    header_ls = ['Counter', 'Paper-ID', 'LastUpdate', 'Title', 'Abstract']
    df = DataFrame(wanted_result, columns=header_ls)
    df.to_csv("lit.csv", header=header_ls, index=False, sep=";")


args = parseInput()
main(args)