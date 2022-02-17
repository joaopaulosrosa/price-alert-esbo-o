from datetime import datetime
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import create_update_assets, test_g
from base.models import AssetPriceHistory

def start():
    scheduler = BackgroundScheduler()


    # scheduler.add_job(test_i,'interval', seconds=20)

    # scheduler.add_job(update_assets,'interval', hours=6)
    scheduler.start()

    scheduler.add_job(test_g, coalesce=True)
