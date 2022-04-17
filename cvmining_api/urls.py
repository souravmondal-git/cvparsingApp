from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet


router = DefaultRouter()
#router.register(r'upload', UploadViewSet, basename="upload")
router.register(r'', UploadViewSet, basename="")

urlpatterns = [

    path('',include(router.urls)),

]
