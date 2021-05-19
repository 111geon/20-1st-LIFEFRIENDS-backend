import json
from json import decoder
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from users.validations import Validation

class ProductView(View):
#     @Validation.validate_login
#     def post(self,request):
#         user = request.account
#         data = json.load(request.body)
        
#         if data['product_name'] not in product.name:
#             return JsonResponse({'MESSAGE':'NOT_FOUND_PRODUCT'}, status=400)         
        
#         product_size = product.size_set.get(name=data['product_size']
#         quantity = data['quantity']

# # 수량
# # 가격
# # 장바구니 담긴개수
# # 몇개가 담겼습니다 ~ 

    def get(self,request):
        product_id = request.GET.get('id', None)
        if not product_id:     
            return JsonResponse({'MESSAGE':'NOT_FOUND_ID'}, status=400)   
        if int(product_id) > Product.objects.count():
            return JsonResponse({'MESSAGE':'NOT_FOUND_PRODUCT'}, status=400)   
        
        product    = Product.objects.get(id=product_id)
        productdetail = {
            'images'           : [product_images.url for product_images in product.productimage_set.all()],
            'menu'             : product.category.menu.name,
            'category'         : product.category.name,
            'name'             : product.name,
            'cost'             : product.cost,
            'clicks'           : product.clicks,
            'description'      : product.description_iamge_url,
            'size'             : [product_size.name for product_size in product.size_set.all()]
        }
        return JsonResponse({'productdetail':productdetail}, status=200)

