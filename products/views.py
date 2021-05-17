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
        product_id = request.GET.get('id', None)
        product    = Product.objects.get(id=product_id)
        producList = []
        reviews  = product.review_set.all()
        reviewsLIst = []
        for review in reviews:
            Review_info = {
                'user'         : review.user.name,
                'review_image' : [review_images.review_image_url for review_images in review.reviewimage_set.all()],
                'rating'       : review.rating,
                'text'         : review.text,
                'date'         : review.created_at,
            }
            reviewsLIst.append(Review_info)
        SpecificProduct_info = {
            'images'           : [product_images.url for product_images in product.productimage_set.all()],
            'menu'             : product.category.menu.name,
            'category'         : product.category.name,
            'name'             : product.name,
            'cost'             : product.cost,
            'clicks'           : product.clicks,
            'description'      : product.description_iamge_url,
            'reviews'          : reviewsLIst,
            'size'             : [product_size.name for product_size in product.size_set.all()]
        }
        producList.append(SpecificProduct_info)
        return JsonResponse({'results':producList}, status=200)