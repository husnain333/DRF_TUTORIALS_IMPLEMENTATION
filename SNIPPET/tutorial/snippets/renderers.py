from rest_framework.renderers import BaseRenderer

class UppercaseRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'upper'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return ''
        return str(data).upper().encode(self.charset)
