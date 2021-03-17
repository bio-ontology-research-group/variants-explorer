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
  col = db.jobs_col
  return col.insert_one(doc)

def drop_data():
  col = db.jobs_col
  col.drop()

# def delete_by_disease_ranktype(disease_code, rank_type):
#   col = db.ukb_col
#   query = { 'disease_code': disease_code,  "rank_type": rank_type }
#   result = col.delete_many(query)
#   logger.info("deleted documents: %d", result.deleted_count)

def find():
  col = db.jobs_col
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
  col = db.jobs_col
  return col.find_one({"_id": ObjectId(str(id))})

def find_records(job_id, filter, limit=None, offset=None):
  col = db.records_col
  filter['job_id'] = job_id

  for key in filter:
    if isinstance(filter[key], list):
      rangeFilter = None
      for item in filter[key]:
        if item.startswith('le'):
          if rangeFilter:
            rangeFilter['$lte'] = float(item[2:])
          else:
            rangeFilter = {'$lte' : float(item[2:])}

        elif item.startswith('ge'):
          if rangeFilter:
            rangeFilter['$gte'] = float(item[2:])
          else:
            rangeFilter = {'$gte' : float(item[2:])}

      if rangeFilter:
        filter[key] = rangeFilter
      else :
        filter[key] = {"$in": filter[key]}

    else: 
      if 'le' == filter[key][:2]:
        filter[key] = {'$lte': float(filter[key][2:])}
      elif 'ge' == filter[key][:2]:
        filter[key] = {'$gte': float(filter[key][2:])}

  print(filter)

  data = list(col.find(filter, limit=limit, skip=offset))
  for obj in data:
      obj['_id']=str(obj['_id'])
  count = col.count_documents(filter)

  result = {'data': data, 'total': count}
  return result

def delete(id):
  col = db.jobs_col
  return col.delete_one({"_id": ObjectId(str(id))})

def update(id, doc):
  col = db.jobs_col
  return col.update_one({"_id": id}, {"$set" : doc})

def insert_record(doc):
  col = db.records_col
  return col.insert_one(doc)

def delete_records(job_id):
  col = db.records_col
  return col.delete_many({"job_id": str(id)})

def next_seq_number(seq_name):
  print(seq_name, ">>>>>>>>>>>")
  seq = db.seqs_col.find_and_modify(
        query={ '_id' : seq_name },
        update={'$inc': {'count': 1}},
        new=True)

  if not seq: 
    seq = {'_id': seq_name, "count":1}
    db.seqs_col.insert_one({'_id': seq_name, "count":1})
  
  return seq['count']


