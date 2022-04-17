from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from .parsing import *
from django.core.files.storage import DefaultStorage, default_storage
from django.core.files.base import ContentFile
from cvmining_proj import settings
import os

# Create your views here.

class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file = request.FILES.get('file')
        content_type = file.content_type
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        #CV_text = read_file(file_path)
        #contact_info = phone_email_doc(CV_text)
        response = find_contact_info(file_path)
        return Response(response)


