from django.utils.encoding import smart_str
from rest_framework import renderers

# smart_str() replaced smart_text()

class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)