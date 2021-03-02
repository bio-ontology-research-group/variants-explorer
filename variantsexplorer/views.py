import logging
import json

from variantsexplorer.analyzer import ValidationError, VariantAnalyzer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from variantsexplorer import db

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
    

    


