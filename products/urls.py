from django.urls import path

from products.views import ProductListView

urlpatterns = [
    path('/categories', ProductListView.as_view()),
]
