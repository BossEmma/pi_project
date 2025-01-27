from .tasks import process_payment_task
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler= BackgroundScheduler()
    scheduler.add_job(process_payment_task, 'interval', seconds=10)
    scheduler.start()