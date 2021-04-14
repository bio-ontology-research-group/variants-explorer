import requests
import logging

ABEROWL_API_URI = 'http://aber-owl.net/api'
OBO_PREFIX = 'http://purl.obolibrary.org/obo/'
CONTENT_HEADER = {'content-type': 'application/json'}

logger = logging.getLogger(__name__) 


class AberowlException(Exception):
    """Base class for Aberowl exceptions"""
    pass


def executeDlQuery(query, type, ontology):
    queryStr = f'query={query}&type={type}&ontology={ontology}&direct=true'
    print(queryStr)
    response = requests.get(f'{ABEROWL_API_URI}/dlquery?{queryStr}', headers=CONTENT_HEADER)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 500:
        raise AberowlException(str(response.json()))
    else:
        return None