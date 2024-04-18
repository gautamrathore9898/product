from django.contrib import admin

# Register your models here.


from application.models import Category, Product

class ProductDisplay(admin.ModelAdmin):
    list_display = ['id', 'category_id', 'title', 'description', 'price', 'status']

admin.site.register(Product, ProductDisplay)
admin.site.register(Category)   