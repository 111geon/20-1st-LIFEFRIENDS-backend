import json
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View
from products.models import *
from users.models    import *
# Create your views here.
class ProductView(View):
    def get(self,request):
        product_id = request.GET.get('id', None)
        product    = Product.objects.get(id=product_id)
        producList = []
        SpecificProduct_info = {
            'images'           : [product_images.url for product_images in product.productimage_set.all()],
            'menu'             : product.category.menu.name,
            'category'         : product.category.name,
            'name'             : product.name,
            'cost'             : product.cost,
            'clicks'           : product.clicks,
            'description'      : product.description_iamge_url,
            'size'             : [product_size.name for product_size in product.size_set.all()]
        }
        producList.append(SpecificProduct_info)
        return JsonResponse({'results':producList}, status=200)