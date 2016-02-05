import json


"""factors are where sample and misc. information go.
Originally, we wanted a check sheet for users to enter their information, but
this looks to be too confusing for a user. I.e. it is easier for them to
enter things into an excel sheet (.txt) and organize that way.

I liked the metadata sheet I received and think it's clear, and organized.
More discussion around this (TODO).
"""
rna_seq_metadata_file = 'Baldwin-Metadata-InducedNeurons.txt'


def create_factors_metadata_json(rna_seq_metadata_file):
    """Create the "factors" section which has the information about the samples
    """
    lines = []
    with open(rna_seq_metadata_file, 'U') as rna_seq_metadata_file:
        for line in rna_seq_metadata_file:
            new_line = line.strip().split('\t')
            lines.append(new_line)

    factor_list = []
    column_name_list = lines[0]

    for line in lines[1:]:
        small_data_json_1 = {}
        small_data_json_2 = {}
        small_data_json_3 = {}
        sample_name = line[2]
        count = 1

        for column_name in column_name_list:
            small_data_json_1[column_name] = line[count]
            count += 1

        small_data_json_2['comment'] = small_data_json_1
        small_data_json_3[sample_name] = small_data_json_2
        factor_list.append(small_data_json_3)

    test_file = open('printed_json.txt', 'w')
    json_out = json.dumps(factor_list, sort_keys=True, indent=4,
                          separators=(',', ': '))
    test_file.write(json_out)
    test_file.close()


def complete_metadata():

    meta = {
                'geo_gds_id': '', 'name': '',
                'default': False, 'display_params': {},
                'summary': '', 'source': 'local_data_load', 'geo_gse_id': '',
                'pubmed_id': '', 'owner': 'ArrayExpress Uploader',
                'geo_gpl_id': '', 'secondaryaccession':
                '', 'factors': ''

                }


def main():
    create_factors_metadata_json(rna_seq_metadata_file)
    complete_metadata()


main()
