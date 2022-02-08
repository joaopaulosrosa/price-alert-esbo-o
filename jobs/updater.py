from datetime import datetime
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_assets

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_assets,'interval', seconds=30)
    scheduler.start()
