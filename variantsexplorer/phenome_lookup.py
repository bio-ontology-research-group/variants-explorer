import requests
import logging
import json
import time

PHENOME_API_URI = 'http://phenomebrowser.net/api'
OBO_PREFIX = 'http://purl.obolibrary.org/obo/'
CONTENT_HEADER = {'content-type': 'application/json'}
HUMAN_ORGANISM_TYPE = "Homo sapiens"
NCBI_GENE_VS = "NCBIGene"
GO_VS = "GO"
HPO_VS = "HP"

logger = logging.getLogger(__name__) 


class PhenomeLookupException(Exception):
    """Base class for other exceptions"""
    pass


def find_entity_by_iris(iris, valueset, retry = 0):
    data = {'iri': iris, 'valueset': valueset}
    response = requests.post(f'{PHENOME_API_URI}/entity/_findbyiri', data=json.dumps(data), headers=CONTENT_HEADER)

    if response.status_code == 200:
        if not response.text and retry < 3:
            time.sleep(1)
            return find_entity_by_iris(iris, valueset, retry + 1)

        return response.json()
    elif response.status_code == 500:
        raise PhenomeLookupException(str(response.json()))
    else:
        return None

def find_gene(gene_symbols, retry = 0):
    data = {'symbols': gene_symbols, 'valueset': NCBI_GENE_VS, 'organism_type': HUMAN_ORGANISM_TYPE}
    response = requests.post(f'{PHENOME_API_URI}/entity/_findgene', data=json.dumps(data), headers=CONTENT_HEADER)

    if response.status_code == 200:
        if not response.text and retry < 3:
            time.sleep(1)
            return find_gene(gene_symbols, retry + 1)

        return response.json()
    elif response.status_code == 500:
        raise PhenomeLookupException(str(response.json()))
    else:
        return None

def find_entity_by_startswith(term, valuesets=[]):
    query_str = f'term={term}'
    for valueset in valuesets:
      query_str = query_str + "&valueset=" + valueset

    response = requests.get(f'{PHENOME_API_URI}/entity/_startswith?{query_str}', headers=CONTENT_HEADER)
    if response.status_code == 200:
        if NCBI_GENE_VS in valuesets:
            return filter(lambda x:x["organism_type"] == HUMAN_ORGANISM_TYPE, response.json())
        return response.json()
    elif response.status_code == 500:
        raise PhenomeLookupException(str(response.json()))
    else:
        return None