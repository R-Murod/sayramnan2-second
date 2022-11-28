from django.contrib import admin
from main.models import *


# Register your models here.


class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category',)
    search_fields = ('title', 'category',)


admin.site.register(Size, SizeAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'is_new', 'is_popular',)
    list_display_links = ('id', 'title', 'category',)
    search_fields = ('title', 'category',)
    list_editable = ('is_new', 'is_popular',)
    list_filter = ('is_popular', 'price',)


admin.site.register(Product, ProductAdmin)


class AdminModelSingle(admin.ModelAdmin):
    pass


admin.site.register(Category, AdminModelSingle)
admin.site.register(CategoryBrand, AdminModelSingle)
admin.site.register(Cart, AdminModelSingle)
admin.site.register(CartItem, AdminModelSingle)
admin.site.register(WishItem, AdminModelSingle)
admin.site.register(CompareItem, AdminModelSingle)
admin.site.register(Subscriber, AdminModelSingle)
