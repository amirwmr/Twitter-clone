import json
from rest_framework.renderers import JSONRenderer

class PostJSONRenderer(JSONRenderer):
    charset = "UTF-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        ...