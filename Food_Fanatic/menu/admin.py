from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Review)