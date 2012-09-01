from django.contrib import admin
from superslides.forms import SlideAdminForm

from superslides.models import Slide

class SlideAdmin(admin.ModelAdmin):
    list_display= ('name', 'caption', 'published',)
    list_filter= ('published',)
    form = SlideAdminForm

admin.site.register(Slide, SlideAdmin)
