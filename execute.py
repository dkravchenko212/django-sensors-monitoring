from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

scheduler=BackgroundScheduler()
scheduler.configure(timezone=utc)

import scheduled_jobs

scheduler.add_job(scheduled_jobs.update_data_from_sensors, 'interval', seconds=30)
scheduler.start()