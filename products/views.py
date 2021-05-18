from django.http     import JsonResponse
from django.views    import View
from products.models import Product, Menu

class MenuNameView(View):
    def get(self,request):
        menus    = Menu.objects.all()
        menulist = []
        try:
            for menu in menus:
                themes    = menu.theme_set.all() 
                themelist = [{'categoryid' : theme.id, 'categoryname' : theme.name} for theme in themes if theme.name != menu.name]
                
                categories   = menu.category_set.all()
                categorylist = [{'categoryid': category.id, 'categoryname ' : category.name} for category in categories]
                
                menulist.append({
                    'menuid'           : menu.id,
                    'menuname'         : menu.name,
                    'categorylist'     : categorylist+themelist
                })
                
            return JsonResponse({'results':menulist}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)