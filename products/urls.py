from django.urls import path 

from products.views import MenuNameView

urlpatterns = [
    path('/menuname', MenuNameView.as_view()),
]