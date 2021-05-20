import json

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q, Count, Sum, Avg
from django.db.models.functions import Coalesce

from products.models  import Menu, Product

class ProductListView(View):
    def get(self, request):
        MAX_THEME_MENU_ID = 7
        try:
            menu     = request.GET.get('menu', None)
            category = request.GET.get('category', None)
            theme    = request.GET.get('theme', None)
            size     = int(request.GET.get('size', '200'))
            page     = int(request.GET.get('page', '1'))

            list_criteria = {}
            if menu:
                if Menu.objects.get(name=menu).id < MAX_THEME_MENU_ID:
                    list_criteria['theme__menu__name'] = menu
                else:
                    list_criteria['category__menu__name'] = menu
            elif category:
                list_criteria['category__name'] = category
            elif theme:
                list_criteria['theme__name'] = theme

            sort_criteria = {
                    None           : '-clicks',
                    'POPULAR'      : '-clicks',
                    'TOTALSALE'    : '-sold',
                    'LOWPRICE'     : 'cost',
                    'RECENT'       : '-created_at',
                    'REVIEW'       : '-review_count',
                    'SATISFACTION' : '-rating'
            }
            sort = request.GET.get('sort', None)
            sort = None if sort not in sort_criteria else sort

            offset   = (page-1) * size
            limit    = page * size

            products = Product.objects\
                    .filter(**list_criteria)\
                    .annotate(
                            review_count=Count('productsize__review'),
                            rating=Coalesce(Avg('productsize__review__rating'), 0.0),
                            sold=Coalesce(Sum('productsize__productorder__quantity',
                                filter=Q(productsize__productorder__status__id__range=(2,4))), 0)
                            )\
                    .order_by(sort_criteria[sort])[offset:limit]

            results = [
                    {
                        'id'          : product.id,
                        'name'        : product.name,
                        'cost'        : int(product.cost),
                        'created_at'  : product.created_at,
                        'clicks'      : product.clicks,
                        'imgUrl'      : product.productimage_set.first().url,
                        'imgAlt'      : product.name,
                        'reviewCount' : product.review_count,
                        'rating'      : product.rating,
                        'sold'        : product.sold
                    } for product in products
            ]

            total_num = Product.objects.filter(**list_criteria).count()
                   
            return JsonResponse({'MESSAGE': results, 'TOTAL_NUM': total_num}, status=200)
        except Menu.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_KEYWORD'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID_KEYWORD'}, status=400)
