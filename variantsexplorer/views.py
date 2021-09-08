import logging
import json
from variantsexplorer.aberowl import executeDlQuery
from variantsexplorer.phenome_lookup import find_entity_by_iris, find_entity_by_startswith

from variantsexplorer.analyzer import ValidationError, VariantAnalyzer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from variantsexplorer import db
from django.http import HttpResponse
from variantsexplorer.options import FIELD_OPTIONS
from django.conf import settings

logger = logging.getLogger(__name__) 

class JobView(APIView):
    """
    Upload variant data
    """
    service = VariantAnalyzer()
    def post(self, request, *args, **kwargs):
        try:
            job = json.loads(request.data['job'])
            file_attached = False
            if 'file' in request.data:
                file_attached = True

            filename = None
            if 'filename' in request.data:
                filename = request.data['filename']

            url = None
            if 'url' in job:
                url = job['url']

            content = None
            if 'content' in job:
                content = job['content']

            if not content and not url and not file_attached:
                raise ValidationError('atleast of one of input data field is required')

            if file_attached:
                self.service.submit_job(job, file=request.data['file'], filename=filename)
            else:
                self.service.submit_job(job)
            return Response(status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("message")

    """
    List jobs by given criteria
    """
    def get(self, request, format=None):
        try:
            # disease = request.GET.get('disease', None)
            # ranktype = request.GET.get('ranktype', None)
            result = db.find()
            return Response(result)
        except Exception as e:
            logger.exception("message")


class JobInstanceView(APIView):
    """
    List jobs by given criteria
    """
    service = VariantAnalyzer()
    def get(self, request, jobid, format=None):
        try:
            result = self.service.get(jobid)
            return Response(result)
        except Exception as e:
            logger.exception("message")

    """
    Delete job by id
    """
    def delete(self, request, jobid, format=None):
        try:
            self.service.delete(jobid)
            return Response()
        except Exception as e:
            logger.exception("message")
    

class RecordsView(APIView):
    """
    List variant records by given criteria
    """

    service = VariantAnalyzer()
    def get(self, request, jobid, format=None):
        try:
            limit = request.GET.get('limit', None)
            offset = request.GET.get('offset', None)
            orderby = request.GET.get('orderby', None)
            query_params = request.GET.dict().copy()
            result = self.service.find_records(jobid, query_params, int(limit), int(offset), orderby)
            return Response(result)
        except Exception as e:
            logger.exception("message")


class InMemoryRecordsView(APIView):
    """
    List variant records by given criteria
    """

    service = VariantAnalyzer()
    def get(self, request, format=None):
        try:
            file_url = request.GET.get('file', None)
            limit = request.GET.get('limit', None)
            offset = request.GET.get('offset', None)
            orderby = request.GET.get('orderby', None)
            query_params = request.GET.dict().copy()

            if not file_url:
                raise RuntimeException("'file' property is required")

            result = self.service.find_inmemory_records(file_url, query_params, int(limit), int(offset), orderby)
            return Response(result)
        except Exception as e:
            logger.exception("message")

class FieldConfigView(APIView):
    """
    Fields configuration
    """
    def get(self, request, format=None):
        try:
            return Response(FIELD_OPTIONS)
        except Exception as e:
            logger.exception("message")

class FindEntityByLabelStartsWith(APIView):
    """
    List lookup entities by given criteria
    """

    def get(self, request, format=None):
        try:
            term = request.GET.get('term', None)
            valueset = request.GET.getlist('valueset')
            result = find_entity_by_startswith(term, valueset) 
            return Response(result)
        except Exception as e:
            logger.exception("message")
            

class FindEntityByIris(APIView):
    """
    List lookup entities by given criteria
    """

    def post(self, request, format=None):
        try:
            entity_iris = request.data['iri']

            valueset = None
            if 'valueset' in request.data:
                valueset = request.data['valueset']

            if not entity_iris:
                raise RuntimeException("'iri' property is required")

            result = find_entity_by_iris(entity_iris, valueset) 
            return Response(result)
        except Exception as e:
            logger.exception("message")
    

class AberowlDLQuery(APIView):
    """
    List lookup entities by given criteria
    """

    def get(self, request, format=None):
        try:
            query = request.GET.get('query')
            type = request.GET.get('type')
            ontology = request.GET.get('ontology')
            result = executeDlQuery(query, type, ontology)
            return Response(result)
        except Exception as e:
            logger.exception("message")

class ExportFilteredData(APIView):
    """
    Get latest
    """
    service = VariantAnalyzer()
    def get(self, request, jobid, format=None):
        try:
            query_params = request.GET.dict().copy()
            result = self.service.export_records(jobid, query_params)
            response = HttpResponse(result, content_type="text/tab-separated-values")
            response['Content-Disposition'] = 'inline; filename=ve_filtered.tsv'
            return response
        except Exception as e:
            logger.exception("message")