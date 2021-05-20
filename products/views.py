from django.http     import JsonResponse
from django.views    import View
from products.models import Menu

class MenuView(View):
    def get(self,request):
        try:
            menus = [{
                    'id'        : menu.id,
                    'menu'      : menu.name,
                    'categories': [{
                            'id'      : category.id, 
                            'category': category.name
                    } for category in menu.category_set.all()] + [{
                            'id'      : theme.id, 
                            'category': theme.name
                    } for theme in menu.theme_set.all() 
                    if theme.name != menu.name]
            } for menu in Menu.objects.all()]
                    
            return JsonResponse({'results':menus}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)