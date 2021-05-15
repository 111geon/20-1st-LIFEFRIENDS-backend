import json
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View
from products.models import *
from users.models    import *
from reviews.models  import *
# Create your views here.
class ProductView(View):
    def get(self,request):
        product_id = request.GET.get('product_id', None)
        product    = Product.objects.get(id=product_id)
        producList = []
        reviews  = product.review_set.all()
        reviewsLIst = []
        for review in reviews:
            Review_info = {
                'user'         : review.user,
                'review_image' : review.review_image.review_image_url,
                'rating'       : review.rating,
                'text'         : review.text,
                'date'         : review.crated_at,
            }
            reviewsLIst.append(Review_info)
        SpecificProduct_info = {
            'menu'             : product.category.menu.name,
            'category'         : product.category.name,
            'name'             : product.name,
            'cost'             : product.cost,
            'clicks'           : product.clicks,
            'description'      : product.description_iamge_url,
            'reviews'          : reviewsLIst
        }
        producList.append(SpecificProduct_info)
        return JsonResponse({'results':producList}, status=200)