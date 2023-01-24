from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data and type(data) == ReturnList:
            data = {
                'status': 'ok',
                'data': data
            }
        elif data == [] or data and data.get('status') not in ['ok', 'err']:
            data = {
                'status': 'ok',
                'data': data
            }
        return super(CustomJSONRenderer, self).render(
            data, accepted_media_type, renderer_context)
