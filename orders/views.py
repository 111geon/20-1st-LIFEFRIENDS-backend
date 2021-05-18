import json

from django.http       import JsonResponse
from django.views      import View

from orders.models     import ProductOrder
from users.validations import Validation

class CartView(View):
    @Validation.validate_login
    def post(self, request):
        

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

