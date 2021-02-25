import logging
import uuid

from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)

client = None

if not client:
  client = MongoClient()
  logger.info("Connected to mongodb server: %s", str(client))

db = client['variantexplorer']

def insert(doc):
  col = db.ve_col
  return col.insert_one(doc)

def drop_data():
  col = db.ve_col
  col.drop()

# def delete_by_disease_ranktype(disease_code, rank_type):
#   col = db.ukb_col
#   query = { 'disease_code': disease_code,  "rank_type": rank_type }
#   result = col.delete_many(query)
#   logger.info("deleted documents: %d", result.deleted_count)

def find(disease_code, rank_type=None):
  col = db.ve_col
  query = { 'disease_code': disease_code } #, 'pvalue' : { '$lte' : 0.05}
  if rank_type:
    query["rank_type"] = rank_type

  result = list(col.find(query))#.sort("gene_symbol"))
  for obj in result:
      obj['_id']=str(obj['_id'])

  return result



