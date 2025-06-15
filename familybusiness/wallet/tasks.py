import logging

from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from .models import FutureTransaction

logger = logging.getLogger(__name__)

def execute_future_transaction():
    logger.info("Running scheduled future transaction")
    now_time = now()

    transactions = FutureTransaction.objects.filter(active=True, execution_date__lte=now_time)

    for trx in transactions:
        with transaction.atomic():
            trx = FutureTransaction.objects.select_for_update().get(id=trx.id)

            if not trx.active or trx.execution_date > timezone.now():
                continue


            trx.create_transaction()

            next_date = trx.get_next_execution_date()

            if next_date:
                trx.execution_date = next_date
            else:
                trx.active = False

            trx.save()