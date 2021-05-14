import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Menu, Category, Theme, Product

class CategoryView(View):
    def get(self, request, category):
        is_menu     = True if Menu.objects.filter(name=category).exists() else False
        is_theme    = True if Theme.objects.filter(name=category).exists() else False
        is_category = True if Category.objects.filter(name=category).exists() else False
        is_all      = True if category=="all" else False

        if is_menu:
            menu = Menu.objects.get(name=category)
            is_theme = True if menu.id < 7 else False
            categories = Theme.objects.filter(menu=menu) if is_theme else Category.objects.filter(menu=menu)
            results = self.makeResults(categories, is_theme)
        elif is_theme:
            themes = Theme.objects.filter(name=category)
            results = self.makeResults(themes, is_theme)
        elif is_category:
            categories = Category.objects.filter(name=category)
            results = self.makeResults(categories, is_theme)
        elif is_all:
            categories = Category.objects.all()
            results = self.makeResults(categories, is_theme)
        else:
            return JsonResponse({'MESSAGE': "INVALID_PATH"}, status=404)

        results = sorted(results, key = lambda product: product['clicks'])
        return JsonResponse({'MESSAGE': results}, status=200)


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
                        'sold'        : 0,
                    }
                )
        return results

