from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils.timezone import now

def setup_periodic_tasks():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    try:
        task = PeriodicTask.objects.get(name="Execute Future Transactions")
    except PeriodicTask.DoesNotExist:
        PeriodicTask.objects.create(
            interval=schedule,
            name="Execute Future Transactions",
            task="wallet.tasks.execute_future_transaction",
            start_time=now(),
            enabled=True,
        )