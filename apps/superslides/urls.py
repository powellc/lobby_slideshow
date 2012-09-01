from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from superslides.views import UpdateSlidesView
from superslides.models import Slide

urlpatterns = patterns('',
    url(r'^$', view=ListView.as_view(model=Slide), name="superslides_index"),
    url(r'^update-slides/$', view=UpdateSlidesView.as_view(), name="superslides_update"),
)
