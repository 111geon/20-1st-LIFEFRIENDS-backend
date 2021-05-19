import json
from json import JSONDecodeError


from django.http import JsonResponse
from django.views import View

from reviews.models import ReviewImage
from products.models import Product
from orders.models  import ProductOrder
from reviews.models import Review, ReviewImage
from users.validations import Validation

class ReviewView(View):
    @Validation.validate_login
    def post(self,request,product_id):
        try:
            data = json.loads(request.body)
            product  = Product.objects.get(id=product_id) 
            size     = product.size_set.get(name=data['product_size'])   

            if not Product.objects.filter(id=product_id).exists():    
                return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
            if not product.size_set.filter(name=data['product_size']).exists():    
                return JsonResponse({'MESSAGE':'INVALID_SIZE'}, status=400)   

            DELIVERED = 4 # status_id = 4(배송완료) 
            if not ProductOrder.objects.filter(order__user=request.account, status_id=DELIVERED):
                return JsonResponse({'MESSAGE':'NO_PURCHASE_HISTORY'}, status=400)  

            review_info = Review.objects.create(
                product_size = size.name,
                user_name    = request.account.name,
                rating       = data['rating'],
                text         = data['text'],
            )

            review_image = ReviewImage.objects.create(
                review_image_url = data['review_image_url'],
                review_id        = review_info.id,
            )

            return JsonResponse({'REVIEW':review_info, 'REVIEW_IMAGE': review_image}, status=400)

        except KeyError: 
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)

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