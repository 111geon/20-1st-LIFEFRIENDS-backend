import json

from django.http import JsonResponse
from django.views import View
from reviews.models import *
from products.models import *
from users.models import *

# Create your views here.
class ReviewImageView(View):
    def post(self,request):
        data = json.loads(request.body)
        #CreateData
        ReviewImage.objects.create(
            review_image_url = data['review_image_url'],
        )
        return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)   

class ReviewView(View):
    def post(self,request):
        data = json.loads(request.body)
        Review.objects.create(
            product      = Product.objects.get(name=data['product_name']),          # ForeignKey
            user         = User.objects.get(name=data['user_name']),                # ForeignKey
            review_image = ReviewImage.objects.get(name=data['review_image_url']),  # ForeignKey
            rating       = data['rating'], # 1~5
            text         = data['text'],
        )

        return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)