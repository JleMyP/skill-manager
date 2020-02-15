from rest_framework.schemas.openapi import AutoSchema

__all__ = ['AutoSchemaCustomCreated']


class AutoSchemaCustomCreated(AutoSchema):
    def _get_responses(self, path, method):
        responses = super()._get_responses(path, method)
        if method == 'POST':
            responses['201'] = responses.pop('200')
        return responses
