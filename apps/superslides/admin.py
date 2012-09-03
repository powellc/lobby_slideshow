from django.contrib import admin

from superslides.models import Slide

class SlideAdmin(admin.ModelAdmin):
    list_display= ('name', 'caption', 'published',)
    list_filter= ('published',)

admin.site.register(Slide, SlideAdmin)
