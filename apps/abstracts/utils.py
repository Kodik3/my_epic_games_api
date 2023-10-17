# Django.
from django.http import Http404
from django.core.mail import EmailMessage
from django.conf import settings


def get_object_or_404(model, object_id: int, error_msg=None):
    try:
        return model.objects.get(id=object_id)
    except model.DoesNotExist:
        if error_msg is None:
            raise Http404
        raise Http404(f"{error_msg}")
    
def send_email(subject: str, body: str, to_emails: list[str]) -> None:
    email = EmailMessage(subject, body, settings.EMAIL_FROM, to_emails)
    email.send()
    