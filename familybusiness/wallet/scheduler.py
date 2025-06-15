from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from wallet.tasks import execute_future_transaction

scheduler = BackgroundScheduler()

def start():
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        execute_future_transaction,
        trigger='interval',
        minutes=5,
        id="execute_future_transaction",
        name="Execute Future Transaction",
        replace_existing=True
    )

    register_events(scheduler)
    scheduler.start()
