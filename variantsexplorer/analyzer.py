import logging
import os
import uuid
import threading
import subprocess
import json
import pandas as pd

from datetime import datetime
from django.conf import settings
import variantsexplorer.db as db

logger = logging.getLogger(__name__) 


MIME_TYPE_JSON = "application/json"
QUEUED = 'Queued'
DONE = 'Done'
FAILED = 'Failed'

def execute(id):
    os.makedirs(os.path.join(settings.BASE_DIR, settings.OUTPUT_DIR), exist_ok=True)
    job = db.get(id)
    print(job, id)
    cwd = os.getcwd()
    print(job['filepath'].rsplit("/", 1))
    rel_input_filepath = os.path.join(settings.VEP_CONTAINER_BASE_DIR, settings.INPUT_DIR, job['filepath'].rsplit("/", 1)[1])
    out_filepath = os.path.join(settings.OUTPUT_DIR, job['filepath'].rsplit("/", 1)[1])
    rel_out_filepath = os.path.join(settings.VEP_CONTAINER_BASE_DIR, out_filepath)
    assembly = job['assembly']
    CMD = f'docker run -t -i -v {cwd}/vep_data:/opt/vep/.vep ensemblorg/ensembl-vep ./vep -input_file {rel_input_filepath} -output_file {rel_out_filepath} --buffer_size 500 \
        --species homo_sapiens --assembly {assembly} --symbol --transcript_version --cache --tab --no_stats --polyphen b --sift b '
    print(cwd, rel_input_filepath, out_filepath, CMD)

    process = subprocess.Popen(CMD, stdout=subprocess.PIPE, text=True, shell=True)
    error = ''
    for line in process.stdout:
       error += line
    
    if error:
        job['error'] = error
        job['status'] = FAILED
    else:
        job['output_filepath'] = os.path.join(settings.BASE_DIR, out_filepath)
        job['status'] = DONE
        df = pd.read_csv(job['output_filepath'], sep='\t', skiprows=45)
        print(df.head())
        job['output_data'] = df.to_dict('records')
        # with open(job['output_filepath'] , 'r') as output_file:
        #     for line in output_file.readlines():
        #         entry = json.loads(line)
        #         job['output_data'].append(entry)

    job['modified_at'] = datetime.now()
    print(error, "|", job)
    db.update(id, job)


class ValidationError(Exception):
    """Base class for validation exceptions"""
    pass

class VariantAnalyzer:

    def submit_job(self, job, file=None, filename=None):
        print(job, file, filename)
        os.makedirs(os.path.join(settings.BASE_DIR, settings.INPUT_DIR), exist_ok=True)
        if file:
            filepath = os.path.join(settings.BASE_DIR, settings.INPUT_DIR,  self.create_incremented_name(str(file)))
            self.write_file(file, filepath)
            job['filepath'] = filepath
            name_part=filename

        elif 'content' in job:
            filepath = os.path.join(settings.BASE_DIR, settings.INPUT_DIR,  str(uuid.uuid4()) + ".vcf")
            self.write_text(job['content'], filepath)
            job['filepath'] = filepath
            name_part = 'pasted data'
        
        job['submitted_at'] = datetime.now()
        job['status'] = QUEUED
        
        if 'name' not in job or not job['name']:
            job['name'] = f'Analysis of {name_part} in Home Sapiens'

        saved_obj = db.insert(job)
        executor = threading.Thread(target=execute, args=(saved_obj.inserted_id,))
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

    def delete(self, id):
        job = db.get(id)
        if os.path.exists(job['filepath']):
            os.remove(job['filepath'])
        if 'output_filepath' in job and os.path.exists(job['output_filepath']):
            os.remove(job['output_filepath'])
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
        index = 1
        name, extension = self.get_name_and_extension(filename)
        while True:
            filename = '{}.{:06d}{}'.format(name, index, extension)
            index += 1
            if not os.path.lexists(os.path.join(settings.BASE_DIR, settings.INPUT_DIR, filename)):
                break

        return filename

    


