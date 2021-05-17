import json

from django.http import JsonResponse
from django.views import View
from reviews.models import *
from products.models import *
from users.models import *
from orders.models import *
# Create your views here.
class ReviewImageView(View):
    def post(self,request):
        data = json.loads(request.body)
        #CreateData
        ReviewImage.objects.create(
            review_image_url = data['review_image_url'],
        )
        return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)   

# class ReviewView(View):
#     def post(self,request):
#         data = json.loads(request.body)
#          = Product.productorder_set.all()    

# # 2. 해당상품의 구매자인지 확인 (무조건)
        
#         Review.objects.create(
#             product      = product,          # ForeignKey
#             user         = email,                # ForeignKey
#             rating       = data['rating'], # 1~5
#             text         = data['text'],
#         )
#         return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)

    # def get (self,request):
    #     product_id = request.GET.get('id', None)
    #     product = Product.objects.get(id=product_id)
    #     reviews = product.review_set.all()

    #     results = []
    #     for review in reviews:
    #         review_info = {
    #             'user_name' : review.user.name,
    #             'created_at' : review.created_at,
    #             'product_size' : product.size,
    #             'text' : review.text,
    #             'review_image' : [review_images.review_image_url for review_images in review.reiewimage_set.all()],
    #             'rating' : review
    #         }
    #         results.append(review_info)
    #     return JsonResponse({'RESULTS': results}, status=201)

