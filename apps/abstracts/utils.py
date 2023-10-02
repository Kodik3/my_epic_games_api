from typing import Any
# Django.
from django.http import Http404
# models.
from games.models import Game, UserGame

def get_object_or_404(model, object_id: int, error_msg=None):
    try:
        return model.objects.get(id=object_id)
    except model.DoesNotExist:
        if error_msg is None:
            raise Http404
        raise Http404(f"{error_msg}")
    