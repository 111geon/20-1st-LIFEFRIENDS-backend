from django.http     import JsonResponse
from django.views    import View
from products.models import *
# Create your views here.
class MetadataView(View):
    def get(self,request):
        menus    = Menu.objects.all()
        MenuList = []
        
        for menu in menus:
            themes    = menu.theme_set.all()
            ThemeList = []
            for theme in themes:
                if theme.name != menu.name: # 메뉴이름과 테마이름이 다를때만 넣어라(메뉴,테마이름이 같은 NEW, 선물추천을 걸러줄라고 넣은것)
                    theme_info = {
                        'categoryId'  : theme.id,
                        'categoryName': theme.name,
                    }
                    ThemeList.append(theme_info)
            categories   = menu.category_set.all()
            CategoryList = []
            for category in categories:
                category_info = {
                    'categoryId'   : category.id,
                    'categoryName' : category.name,
                }
                CategoryList.append(category_info)
            menu_info = {
                'menuId'           : menu.id,
                'menuName'         : menu.name,
                'categoryList'     : CategoryList+ThemeList
            }
            MenuList.append(menu_info)
            themes = menu.theme_set.all()
            ThemeList = []
        
        return JsonResponse({'results':MenuList}, status=200)