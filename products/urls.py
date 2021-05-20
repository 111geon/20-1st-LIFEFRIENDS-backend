from django.urls import path

from products.views import ProductListView, SearchView, MenuView, ProductView

urlpatterns = [
    path('/categories', ProductListView.as_view()),
    path('/search', SearchView.as_view()),
    path('/menu', MenuView.as_view()),
    path('/<str:product_id>', ProductView.as_view()),
]