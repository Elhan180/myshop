from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Показывать 1 пустую строку по умолчанию

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'price', 'stock', 'available']
    list_filter = ['available', 'category']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
