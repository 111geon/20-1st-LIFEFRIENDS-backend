from django.urls import path 

from products.views import *

urlpatterns = [
    path('/metadatas', MetadataView.as_view()),
]