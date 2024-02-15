from booyah.jobs.jobs_manager import jobs_manager

app = jobs_manager.manager.instance()

@app.task
def basic_task():
    print("Basic celery task executed...")
