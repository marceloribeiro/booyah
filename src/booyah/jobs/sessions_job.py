from datetime import timedelta
from booyah.jobs.jobs_manager import jobs_manager

app = jobs_manager.manager.instance()

app.conf.beat_schedule.update({
    'delete_expired_sessions': {
        'task': 'booyah.jobs.sessions_job.delete_expired_sessions',
        'schedule': timedelta(days=2)
    },
})

@app.task
def delete_expired_sessions():
    from booyah.session.session_manager import session_manager
    print("Deleting expired sessions...")
    session_manager.clear_expired()
    print('Expired sessions deleted!')
