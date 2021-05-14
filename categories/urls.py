from django.urls import path

from categories.views import CategoryView

urlpatterns = [
    path('/<str:category>', CategoryView.as_view()),
]

