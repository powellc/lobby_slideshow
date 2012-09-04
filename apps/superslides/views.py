from django.views.generic import ListView
from superslides.models import Slide
from django import http
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        data=[]
        for slide in context['slide_list']:
            try:
                data.append(
                  { 'image':slide.image['slideshow'].url,
                    'title':slide.caption,})
            except:
                pass
        return json.dumps(data)

class UpdateSlidesView(JSONResponseMixin, ListView):
    model = Slide
    pass

