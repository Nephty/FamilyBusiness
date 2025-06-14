from celery import shared_task
from django.utils.timezone import now
from .models import FutureTransaction

@shared_task
def execute_future_transaction():
    for future_trx in FutureTransaction.objects.filter(active=True, execution_date__lte=now()):
        future_trx.create_transaction()

        next_date = future_trx.get_next_execution_date()

        if next_date:
            future_trx.execution_date = next_date
        else:
            future_trx.active = False

        future_trx.save()