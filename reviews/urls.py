from django.urls import path 

from reviews.views import ReviewImageView, ReviewView

urlpatterns = [
    # path('/reviewimage', ReviewImageView.as_view()),
    path('<int:product_id>', ReviewView.as_view()),
]
