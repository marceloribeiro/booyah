**Jobs/Tasks**
Our web framework comes equipped with a powerful and flexible jobs/tasks feature designed to efficiently handle background processes, scheduled tasks, and other asynchronous operations. This capability allows developers to offload time-consuming tasks, ensuring that critical user interactions remain responsive and seamless.
Currently we have only support for Celery task queue.

To create a job with custom tasks you can call the job generator:

```sh
$ booyah g job example basic_task basic_task2 basic_task3 
```

In the previous generator call example, it will create a file app/jobs/example_job.py with the tasks (basic_task, basic_task2, basic_task3)

To handle the tasks you need to run the following commands in your project folder:

```sh
$ booyah w
```

and to scheduled tasks, like clean expired sessions (automatically scheduled)

```sh
$ booyah ws
```

to add a scheduled task you may follow this example:

app/jobs/example_job.py
> from datetime import timedelta
> from booyah.jobs.jobs_manager import jobs_manager
> 
> app = jobs_manager.manager.instance() # a Celery instance
> app.conf.beat_schedule.update({
>     'basic_task': {
>         'task': 'your_project_folder.app.jobs.example_job.basic_task',
>         'schedule': timedelta(minutes=2)
>     },
> })
> 
> @app.task
> def basic_task():
>     print("Basic celery task executed...")

You can change some settings in your project config/application.yml
> environment:
>   jobs:
>     broker: 'amqp://guest:guest@localhost:5672/'

You can call to execute the task in a controller by using the Celery task call:

> from project_name.app.jobs.example_job import basic_task
> from project_name.app.controllers.application_controller import ApplicationController
> 
> class UsersController(ApplicationController):
>     
>     def index(self):
>         basic_task.apply_async()
>         ...
