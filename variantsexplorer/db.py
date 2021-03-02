import logging
import uuid

from pymongo import MongoClient
from bson import ObjectId
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

def find():
  col = db.ve_col
  # query = { 'disease_code': disease_code } #, 'pvalue' : { '$lte' : 0.05}
  # if rank_type:
  #   query["rank_type"] = rank_type
  query = {}
  result = list(col.find(query, {"filepath":0, "output_filepath":0, "output_data":0}).sort("submitted_at", -1))
  for obj in result:
      obj['_id']=str(obj['_id'])
      obj['submitted_at']=str(obj['submitted_at'])
      if 'modified_at' in obj:
        obj['modified_at']=str(obj['modified_at'])

  return result

def get(id):
  col = db.ve_col
  return col.find_one({"_id": ObjectId(str(id))})

def delete(id):
  col = db.ve_col
  return col.delete_one({"_id": ObjectId(str(id))})

def update(id, doc):
  col = db.ve_col
  return col.update_one({"_id": id}, {"$set" : doc})
  


