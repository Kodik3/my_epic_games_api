from celery import shared_task


@shared_task
def do_test():
    return 5 + 10