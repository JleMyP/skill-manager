from rest_framework import renderers

__all__ = ['JsonUnicodeRenderer']


class JsonUnicodeRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
