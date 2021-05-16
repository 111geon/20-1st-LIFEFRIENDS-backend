import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Sum, Avg

from products.models  import Menu, Category, Theme, Product
from orders.models    import ProductOrder, Order, Status

class CategoryView(View):
    def get(self, request, category):
        is_menu     = True if Menu.objects.filter(name=category).exists() else False
        is_theme    = True if Theme.objects.filter(name=category).exists() else False
        is_category = True if Category.objects.filter(name=category).exists() else False
        is_all      = True if category=="all" else False

        if is_menu:
            menu       = Menu.objects.get(name=category)
            is_theme   = True if menu.id < 7 else False
            categories = Theme.objects.filter(menu=menu) if is_theme else Category.objects.filter(menu=menu)
            results    = self.makeResults(categories, is_theme)
        elif is_theme:
            themes     = Theme.objects.filter(name=category)
            results    = self.makeResults(themes, is_theme)
        elif is_category:
            categories = Category.objects.filter(name=category)
            results    = self.makeResults(categories, is_theme)
        elif is_all:
            categories = Category.objects.all()
            results    = self.makeResults(categories, is_theme)
        else:
            return JsonResponse({'MESSAGE': "INVALID_PATH"}, status=404)
        total_num = len(results)

        sort = request.GET.get('sort', None)
        if not sort or sort == "POPULAR":
            results = sorted(
                    results, 
                    key= lambda product: product['clicks'], 
                    reverse = True
                    )
        elif sort == "TOTALSALE":
            results = sorted(
                    results, 
                    key= lambda product: product['clicks'], 
                    reverse = True
                    )
        elif sort == "LOWPRICE":
            results = sorted(
                    results,
                    key= lambda product: product['cost']
                    )
        elif sort == "RECENT":
            results = sorted(
                    results,
                    key= lambda product: product['created_at'],
                    reverse = True
                    )
        elif sort == "REVIEW":
            pass
        elif sort == "SATISFACTION":
            pass
        else:
            pass

        size = request.GET.get('size', '40')
        size = int(size)

        page = request.GET.get('page', '1')
        page = int(page)

        results = results[(page-1)*size:page*size]

        return JsonResponse({'MESSAGE': results, 'TOTAL_NUM': total_num}, status=200)


    def makeResults(self, categories, is_theme):
        results = []
        for category in categories:
            if is_theme:
                products = Product.objects.filter(theme=category)
            else:
                products = Product.objects.filter(category=category)
            for product in products:
                images     = product.productimage_set.all()
                image_urls = [image.url[1:-1] if image.url[0]!='h' else image.url for image in images]

                product_orders = ProductOrder.objects.filter(Q(product=product) & Q(1<status_id<5))
                sold           = product_orders.aggregate(Sum('quantity'))['quantity__sum'] if product_orders.exists() else 0
                results.append(
                    {
                        'id'          : product.id,
                        'name'        : product.name,
                        'cost'        : int(product.cost),
                        'created_at'  : product.created_at,
                        'clicks'      : product.clicks,
                        'imgUrl'      : image_urls[0],
                        'imgAlt'      : product.name,
                        'reviewCount' : 0,
                        'rating'      : 0,
                        'sold'        : sold,
                    }
                )
        return results

