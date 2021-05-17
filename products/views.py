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
                    key= lambda product: product['sold'], 
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
            results = sorted(
                    results,
                    key= lambda product: product['reviewCount'],
                    reverse = True
                    )
        elif sort == "SATISFACTION":
            results = sorted(
                    results,
                    key= lambda product: product['rating'],
                    reverse = True
                    )

        size = request.GET.get('size', '40')
        size = int(size)

        page = request.GET.get('page', '1')
        page = int(page)

        results = results[(page-1)*size:page*size]

        return JsonResponse({'MESSAGE': results, 'TOTAL_NUM': total_num}, status=200)


    def makeResults(self, categories):
        results = []
        for category in categories:
            if isinstance(category, Theme):
                products = Product.objects.filter(theme=category)
            else:
                products = Product.objects.filter(category=category)
            for product in products:
                images     = product.productimage_set.all()
                image_urls = [image.url[1:-1] if image.url[0]!='h' else image.url for image in images]

                product_sizes   = ProductSize.objects.filter(product=product)
                product_orders  = ProductOrder.objects.none()
                product_reviews = Review.objects.none()
                for product_size in product_sizes:
                    product_orders |= ProductOrder.objects.filter(
                            Q(product_size=product_size) & 
                            ~Q(status=Status.objects.get(id=1))
                            ).exclude(status=Status.objects.get(id=5)
                            )
                    product_reviews |= product_size.review_set.all()
                sold = product_orders.aggregate(Sum('quantity'))['quantity__sum'] if product_orders.exists() else 0
                review_count = product_reviews.count() if product_reviews.exists() else 0
                rating       = product_reviews.aggregate(Avg('rating'))['rating__avg'] if product_reviews.exists() else 0

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


