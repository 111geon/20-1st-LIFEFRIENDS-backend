from django.urls import path 

from products.views import MenuView

urlpatterns = [
    path('/menu', MenuView.as_view()),
]