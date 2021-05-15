from django.urls import path 

from products.views import *

urlpatterns = [
    path('', ProductView.as_view()),
]