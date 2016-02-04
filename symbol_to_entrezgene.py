

import re

import pandas as pd
import mygene


"""
symbol http://mygene.info/v2/query?q=symbol:0610005C13Rik
http://mygene.info/v2/query?q=symbol:42430

helper file to return entrezgene IDs, which are needed for
BioGPS data loading

RNAseq data for mouse
"""

species = 'mouse'
symbol = 'symbol'
entrezgene = 'entrezgene'
input_seq_file = 'iN_final_duplicates_normalizedcounts_avg.txt'


def list_of_gene_IDs_and_symbols_from_file(input_seq_file):
    """Take a users input file from their sequencing run and get a list of the
    reporter genes used. They should all be gene IDs, but many are symbols.
    Attempt to find ensembl gene IDs for reporters.
    """
    print("Find entrezgene IDs for reporter genes in RNAseq run")
    lines = []
    with open(input_seq_file, 'U') as input_seq_file:
        next(input_seq_file)
        for line in input_seq_file:
            new_line = line.strip().split('\t')[0]
            new_line = re.sub('"', '', new_line)  # inputs contained quotes
            lines.append(new_line)

    query_list = pd.Series(data=lines).tolist()

    print("length of query list: ", len(query_list))
    return query_list


def query_mygene_for_entrezIDs(query_list):
    """User a query list to query mygene.ifor for the entrezgene ID and make a
    dictionary that can be used to access the entrezgene ID.
    """
    mg = mygene.MyGeneInfo()
    mg_results = mg.querymany(query_list, species=species, scopes=symbol,
                              fields=entrezgene, verbose=False,
                              entrezonly=True)
    mygene_website_dict = {}
    for dic in mg_results:
        try:
            mygene_website_dict[dic['query']] = dic['entrezgene']
        except KeyError:
            pass

    return mygene_website_dict


def new_list_with_IDs_if_available(query_list, mygene_website_dict):
    """Check all the symbols or IDs and find entrezgene/NCBI IDs if they exist.
    If they do not exist, then just keep symbol.

    Returns list in order of input.
    """
    output_list = []
    no_entrez_gene_id_count = 0
    for i in query_list:
        try:
            output_list.append(mygene_website_dict[i])  # get entrezgene ID
        except KeyError:
            output_list.append(i)  # if no entrezgene ID, just keep the symbol
            no_entrez_gene_id_count += 1
    print("number of output list: ", len(output_list))
    print("number of inputs with no gene ID found: ", no_entrez_gene_id_count)
    print("end")
    return output_list


def main():
    query_list = list_of_gene_IDs_and_symbols_from_file(input_seq_file)
    mygene_website_dict = query_mygene_for_entrezIDs(query_list)
    output_list = new_list_with_IDs_if_available(query_list,
                                                 mygene_website_dict)

main()
