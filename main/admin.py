from django.contrib import admin

# Register your models here.

from .models import *

#привяска картинки

class PImageInLine(admin.TabularInline):
    model = PImage
    max_num = 5
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PImageInLine, ]

admin.site.register(Category)
