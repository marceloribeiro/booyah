from booyah.jobs.jobs_manager import jobs_manager

def on_starting(server):
    print('gunicorn.conf.py#on_starting initializing jobs...')
    setattr(server, 'celery_app', jobs_manager.manager.instance)
    print('jobs initialized!')