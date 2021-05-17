from django.urls import path 

from reviews.views import *

urlpatterns = [
    # path('', ReviewView.as_view()),
    path('/reviewimage', ReviewImageView.as_view()),
]
