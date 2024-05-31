from django.contrib import admin
from .models import Image, Category


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_date', 'age_limit')
    filter_horizontal = ('categories',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
