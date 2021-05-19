from django.urls import path 

from products.views import ProductView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/purchase/<int:product_id>', ProductView.as_view()),
]