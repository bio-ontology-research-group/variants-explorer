import logging
import os
import uuid
import multiprocessing
import subprocess
import json
import pandas as pd
import variantsexplorer.db as db
import docker
from docker.errors import ContainerError

from datetime import datetime
from django.conf import settings
from sys import platform

from variantsexplorer.phenome_lookup import GO_VS, HPO_VS, OBO_PREFIX, find_entity_by_iris

logger = logging.getLogger(__name__) 
client = None

if not client:
    client = docker.from_env()

MIME_TYPE_JSON = "application/json"
QUEUED = 'Queued'
PROCESSING = 'Processing'
DONE = 'Done'
FAILED = 'Failed'
CHUNK_SIZE = 10 ** 5

def execute(id):
    os.makedirs(os.path.join(settings.DATA_DIR, settings.OUTPUT_DIR), exist_ok=True)
    conn = db.get_connection()
    job = db.get(id,conn)
    logger.info("Start executing job: %s", str(job))

    try:

        rel_input_filepath = os.path.join(settings.VEP_CONTAINER_BASE_DIR, settings.INPUT_DIR, job['filepath'].rsplit("/", 1)[1])
        out_filepath = os.path.join(settings.OUTPUT_DIR, job['filepath'].rsplit("/", 1)[1])
        rel_out_filepath = os.path.join(settings.VEP_CONTAINER_BASE_DIR, out_filepath)
        GO_ANNO_DATA_FILE = os.path.join(settings.VEP_CONTAINER_BASE_DIR, 'Plugins', 'sorted.plugin.go.bed.gz')
        PHENO_DATA_FILE = os.path.join(settings.VEP_CONTAINER_BASE_DIR, 'Plugins', 'sorted.plugin.pheno.bed.gz')
        PPI_DATA_FILE = os.path.join(settings.VEP_CONTAINER_BASE_DIR, 'Plugins', 'sorted.plugin.ppi.bed.gz')
        # dbNSFP_DATA_FILE = os.path.join(settings.VEP_CONTAINER_BASE_DIR, 'Plugins', 'sorted.plugin.pheno.bed.gz')
        assembly = job['assembly']

        job['status'] = PROCESSING
        db.update(id, job, conn)

        CMD = f'./vep -input_file {rel_input_filepath} -output_file {rel_out_filepath} --buffer_size 500 \
            --species homo_sapiens --assembly {assembly} --symbol --transcript_version --tsl --numbers  --check_existing --hgvs --biotype --cache --tab --no_stats --polyphen b --sift b --af --af_gnomad --pubmed --uniprot --protein \
            --custom {GO_ANNO_DATA_FILE},GO_CLASSES,bed,overlap --custom {PHENO_DATA_FILE},PHENOTYPE,bed,overlap -custom {PPI_DATA_FILE},PPI,bed,overlap'
        print(rel_input_filepath, out_filepath, CMD,  get_mode(), client)
        lines = client.containers.run("ensemblorg/ensembl-vep", CMD, volumes={f'{os.getcwd()}/vep_data': {'bind': '/opt/vep/.vep', 'mode': get_mode()}}, stream=True)
        
        error = ''
        for line in lines:
            error += line
        
        if error.strip():
            logger.error("Error occured while %s", error)
        else:
            logger.info("File is processed by VEP")
        
        if error:
            job['error'] = error
            job['status'] = FAILED
        else:
            job['output_filepath'] = os.path.join(settings.DATA_DIR, out_filepath)
            job['status'] = DONE

            count=1
            with pd.read_csv(job['output_filepath'], chunksize=CHUNK_SIZE, sep='\t', skiprows=75) as reader:
                for chunk in reader:
                    logger.info("processing chunk %d | %s", count, job['output_filepath'])
                    process_dataframe(chunk, job, conn)
                    count += 1

                
            # df = pd.read_csv(job['output_filepath'], sep='\t', skiprows=75)
            # cache = {
            #     "go" : resolve_go(df['GO_CLASSES']),
            #     "hp" : resolve_hp(df['PHENOTYPE'])
            # }
            # records =  df.to_dict('records')
            # save_records(records, job, conn)

            # with open(job['output_filepath'] , 'r') as output_file:
            #     for line in output_file.readlines():
            #         entry = json.loads(line)
            #         job['output_data'].append(entry)

        job['modified_at'] = datetime.now()
        logger.info("Job executed: %s", str(job))
        db.update(id, job, conn)
    

    except ContainerError as e:
        logger.exception("message")
        handle_error(id, job, conn, str(e))
    except Exception as e:
        logger.exception("message")
        handle_error(id, job, conn)


def handle_error(job_id, job, conn, error_msg=''):
    if os.path.exists(job['filepath']):
        os.remove(job['filepath'])
    if 'output_filepath' in job and os.path.exists(job['output_filepath']):
        os.remove(job['output_filepath'])
    db.delete_records(id)

    job['error'] = "Failed to process file. " + error_msg
    job['status'] = FAILED
    db.update(job_id, job, conn)
        


def process_dataframe(df, job, db_conn):
    # df['job_id'] = str(job['_id'])
    df.AF = df.AF.astype(str).str.replace('-', 'nan').astype(float).fillna('')
    df['SIFT_object'] = df.SIFT.astype(str).str.replace('-', '').transform(parse_score_field)
    df['PolyPhen_object'] = df.PolyPhen.astype(str).str.replace('-', '').transform(parse_score_field)
    df.GO_CLASSES = df.GO_CLASSES.astype(str).str.replace('-', '').str.split('##')
    df.PHENOTYPE = df.PHENOTYPE.astype(str).transform(parse_phenotype)
    df.PPI = df.PPI.astype(str).transform(parse_ppi)
    records =  df.to_dict('records')
    db.insert_records(str(job['_id']), records, db_conn)

# def save_records(records, job, db_conn):
#     for item in records:
#         item['job_id'] = str(job['_id'])
#         item['SIFT_object'] = parse_score_field(item['SIFT'])
#         item['PolyPhen_object'] = parse_score_field(item['PolyPhen'])
#         item['AF'] = parse_number_field(item['AF'])
#         item['GO_CLASSES'] = parse_go_functions(item['GO_CLASSES'], cache['go'])
#         item['PHENOTYPE'] = parse_phenotype(item['PHENOTYPE'], cache['hp'])
#         item['PPI'] = parse_ppi(item['PPI'])
#         db.insert_record(item, db_conn)


# def parse_go_functions(value, cache):
#     if not value.strip() or '-' in value:
#         return []

#     golist = []
#     for go_class in value.split('##'):
#         entry = {"class" : go_class}
#         if go_class in cache:
#             entry["display"] = cache[go_class]["label"][0]

#         golist.append(entry)
        
#     return golist

# def parse_phenotype(value, cache):
#     if not value.strip() or '-' == value:
#         return []

#     hplist = []
#     for item in value.split('__'):
#         for hp_class in item.split('--')[1].split('##'):
#             entry = {"class" : hp_class}
#             if hp_class in cache:
#                 entry["display"] = cache[hp_class]["label"][0]

#             hplist.append(entry)
        
#     return hplist

def parse_score_field(score):
    if score:
        parts =  score.strip().split('(')
        return {'term': parts[0], 'score': float(parts[1][:-1])}
    return None
    
def parse_score_field(score):
    if not score.strip() or '-' in score:
        return None
    
    parts =  score.strip().split('(')
    return {'term': parts[0], 'score': float(parts[1][:-1])}

def parse_phenotype(value):
    if not value.strip() or '-' == value:
        return []

    hplist = []
    for item in value.split('__'):
        for hp_class in item.split('--')[1].split('##'):
            hplist.append(hp_class)
            
    return hplist

def parse_ppi(value):
    if not value.strip() or '-' == value:
        return {}

    ppi = {}
    for protein in value.split('__'):
        protein_parts = protein.split('--')
        ppi[protein_parts[0]] = protein_parts[1].split('##')

    return ppi

def resolve_go(entries):
    go = set()
    for go_class in entries.tolist():
        if '-' == go:
            continue
        
        for item in go_class.split('##'):
            go.add(item)
    
    if len(go) < 1:
        return {}

    go_iris = []
    for go_class in go:
        go_iris.append(OBO_PREFIX + go_class.replace(':', '_'))

    result = find_entity_by_iris(go_iris, GO_VS)
    if len(result) > 1:
        return {x['identifier']: x for x in result}
    
    return {}


def resolve_hp(entries):
    hp = set()
    for protein in entries.tolist():
        if '-' == protein:
            continue
        
        for item in protein.split('__'):
            for hp_class in item.split('--')[1].split('##'):
                hp.add(hp_class)

    if len(hp) < 1:
        return {}

    hp_iris = []
    for hp_class in hp:
        hp_iris.append(OBO_PREFIX + hp_class.replace(':', '_'))
    

    result = find_entity_by_iris(hp_iris, HPO_VS)
    if len(result) > 1:
        return {x['identifier']: x for x in result}

    return {}

def get_mode():
    if 'linux' in platform:
        return 'Z'
    else:
        return 'rw'
class ValidationError(Exception):
    """Base class for validation exceptions"""
    pass

class VariantAnalyzer:

    def submit_job(self, job, file=None, filename=None):
        print(job, file, filename)
        os.makedirs(os.path.join(settings.DATA_DIR, settings.INPUT_DIR), exist_ok=True)
        if file:
            filename = self.create_incremented_name(str(file))
            filepath = os.path.join(settings.DATA_DIR, settings.INPUT_DIR, filename)
            self.write_file(file, filepath)
            job['filepath'] = filepath
            job['filename'] = filename
            name_part=filename

        elif 'content' in job:
            filename = str(uuid.uuid4()) + ".vcf"
            filepath = os.path.join(settings.DATA_DIR, settings.INPUT_DIR,  filename)
            self.write_text(job['content'], filepath)
            job['filepath'] = filepath
            job['filename'] = filename
            name_part = 'pasted data'
        
        job['submitted_at'] = datetime.now()
        job['status'] = QUEUED
        
        if 'name' not in job or not job['name']:
            job['name'] = f'Analysis of {name_part} in Home Sapiens'

        saved_obj = db.insert(job)
        executor = multiprocessing.Process(target=execute, args=(saved_obj.inserted_id,))
        executor.start()
        return saved_obj.inserted_id

    def get(self, id):
        obj = db.get(id)
        obj['_id']=str(obj['_id'])
        obj['submitted_at']=str(obj['submitted_at'])
        if 'modified_at' in obj:
            obj['modified_at']=str(obj['modified_at'])

        obj['filepath'] = None
        if 'output_filepath' in obj:
            obj['output_filepath'] = None
        return obj

    def find_records(self, job_id, filter, limit=10, offset=None, orderby=None):
        if 'limit' in filter:
            del filter['limit']
        if 'offset' in filter:
            del filter['offset']
        if 'orderby' in filter:
            del filter['orderby']
        if 'ontology_filter' in filter:
            if 'HP:' in filter['ontology_filter']:
                filter['PHENOTYPE'] = filter['ontology_filter']
            elif 'GO:' in filter['ontology_filter']:
                filter['GO_CLASSES'] = filter['ontology_filter']

            del filter['ontology_filter']

        if 'ClinSig' in filter:
            filter['CLIN_SIG'] = filter['ClinSig']
            del filter['ClinSig']

        clone = filter.copy()
        for key in clone:
            if ',' in clone[key]:
                filter[key] = filter[key].split(",")

            if not clone[key].strip():
               del filter[key]
        result = db.find_records(job_id, filter, limit, offset, orderby)
        for obj in result['data']:
            obj['_id']=str(obj['_id'])
        return result

    def export_records(self, job_id, filter):
        result = self.find_records(job_id, filter, limit=None)
        df = pd.DataFrame(result['data'])

        #clear memory
        del result

        df.drop('_id', axis='columns', inplace=True)
        df.drop('SIFT_object', axis='columns', inplace=True)
        df.drop('PolyPhen_object', axis='columns', inplace=True)
        return df.to_csv(sep="\t", index=False)


    def delete(self, id):
        job = db.get(id)
        if os.path.exists(job['filepath']):
            os.remove(job['filepath'])
        if 'output_filepath' in job and os.path.exists(job['output_filepath']):
            os.remove(job['output_filepath'])

        db.delete_records(id)
        return db.delete(id)

    def write_file(self, file, filepath):
        with open(filepath, 'wb+') as out_file:
            for chunk in file.chunks():
                out_file.write(chunk)

    def write_text(self, content, filepath):
        with open(filepath, 'w+') as out_file:
            out_file.write(content)

    def get_name_and_extension(self, filename):
        return os.path.splitext(filename)

    def create_incremented_name(self, filename) -> str:
        index = db.next_seq_number('output_filename')
        name, extension = self.get_name_and_extension(filename)
        while True:
            filename = '{}.{:06d}{}'.format(name, index, extension)
            if not os.path.lexists(os.path.join(settings.DATA_DIR, settings.INPUT_DIR, filename)):
                break

        return filename

    


