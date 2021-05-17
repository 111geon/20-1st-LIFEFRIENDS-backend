import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Sum, Avg

from products.models  import Menu, Category, Theme, Product, ProductSize
from orders.models    import ProductOrder, Order, Status
from reviews.models   import Review

class CategoryView(View):
    def get(self, request):
        menu     = request.GET.get('menu', None)
        category = request.GET.get('category', None)
        theme    = request.GET.get('theme', None)

        if menu:
            menu       = Menu.objects.get(name=menu)
            categories = Theme.objects.filter(menu=menu) if menu.id<7 else Category.objects.filter(menu=menu)
            results    = self.makeResults(categories)
        elif theme:
            themes     = Theme.objects.filter(name=theme)
            results    = self.makeResults(themes)
        elif category:
            categories = Category.objects.filter(name=category)
            results    = self.makeResults(categories)
        else:
            categories = Category.objects.all()
            results    = self.makeResults(categories)
        total_num = len(results)

        sort     = request.GET.get('sort', None)
        sort_std = {
                None           : ['clicks', True],
                'POPULAR'      : ['clicks', True],
                'TOTALSALE'    : ['sold', True],
                'LOWPRICE'     : ['cost', False],
                'RECENT'       : ['created_at', True],
                'REVIEW'       : ['reviewCount', True],
                'SATISFACTION' : ['rating', True]
                }
        results = sorted(
                results,
                key = lambda product: product[sort_std[sort][0]],
                reverse = sort_std[sort][1]
                )
                
        size = request.GET.get('size', '10')
        size = int(size)
        page = request.GET.get('page', '1')
        page = int(page)

        results = results[(page-1)*size:page*size]
        return JsonResponse({'MESSAGE': results, 'TOTAL_NUM': total_num}, status=200)


    def makeResults(self, categories):
        results = []
        
        products = []
        for category in categories:
            try:
                products += list(Product.objects.filter(theme=category))
            except ValueError:
                products += list(Product.objects.filter(category=category))

        for product in products:
            images     = product.productimage_set.all()
            image_urls = [image.url[1:-1] if image.url[0]!='h' else image.url for image in images]

            sold            = 0
            review_count    = 0
            rating          = 0
            product_sizes   = product.productsize_set.all()
            for product_size in product_sizes:
                product_orders = product_size.productorder_set.filter(
                        ~Q(status_id=1) &
                        ~Q(status_id=5)
                        )
                sold += product_orders.aggregate(Sum('quantity'))['quantity__sum'] if product_orders.exists() else 0

                product_reviews  = product_size.review_set.all()
                review_count    += len(product_reviews)
                rating          += product_reviews.aggregate(Sum('rating'))['rating__sum'] if product_reviews.exists() else 0
            rating = rating / review_count if review_count else 0

            results.append(
                {
                    'id'          : product.id,
                    'name'        : product.name,
                    'cost'        : int(product.cost),
                    'created_at'  : product.created_at,
                    'clicks'      : product.clicks,
                    'imgUrl'      : image_urls[0],
                    'imgAlt'      : product.name,
                    'reviewCount' : review_count,
                    'rating'      : rating,
                    'sold'        : sold,
                }
            )
        return results


