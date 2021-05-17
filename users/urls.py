from django.urls import path

from users.views  import SignupView, LoginView, CouponView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/coupon/<str:coupon>', CouponView.as_view()),
]

