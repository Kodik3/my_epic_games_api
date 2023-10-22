# python.
from typing import Any
# Django.
from  django.db.models import query
# rest_framework.
from rest_framework.validators import ValidationError
from rest_framework.response import Response


class ErrorMixin:
    def error(self, message: str, code: int) -> None:
        raise ValidationError({'error': message}, code=code)


class ObjectMixin:
    def object_get(self, queryset: query.QuerySet, obj_id: str) -> Any:
        object: Any = queryset.filter(pk=int(obj_id)).first()
        if object is None:
            raise ValidationError(f'Object {obj_id} not found', code=404)
        return object
    
    
class ResponseMixin:
    STATUSES: tuple = (
        'Success',
        'Warning',
        'Error'
    )
    def json_response(self, data: Any, status:str = 'Success') -> Response:
        if status not in self.STATUSES:
            raise ValidationError('FATAL ERROR')
        return Response(data={'status':status, 'results':data})