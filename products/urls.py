from django.urls import path

from products.views import ProductListView, SearchView

urlpatterns = [
    path('/categories', ProductListView.as_view()),
    path('/search', SearchView.as_view())

]
