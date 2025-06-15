import logging
import time

from django.db import transaction, OperationalError
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

            safe_create_transaction(trx)

            next_date = trx.get_next_execution_date()

            if next_date:
                trx.execution_date = next_date
            else:
                trx.active = False

            trx.save()

def safe_create_transaction(trx, retries=3):
    for i in range(retries):
        try:
            trx.create_transaction()
            return
        except OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(1)
            else:
                raise

    print("Failed to create transaction after retries")