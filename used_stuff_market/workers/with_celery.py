from celery import Celery

from used_stuff_market.workers.settings import WorkersSettings

app = Celery("used_stuff_market", broker=str(WorkersSettings().URL))
app.autodiscover_tasks(packages=["used_stuff_market.catalog"])
