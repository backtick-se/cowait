Module cowait.tasks.schedule.schedule
=====================================

Functions
---------

    
`scheduled_task_id(name: str, date: datetime.datetime)`
:   

Classes
-------

`ScheduleTask(**inputs)`
:   ScheduleTask runs another task on a specified cron-style schedule.
    
    Inputs:
        schedule (str): Cron-style scheduling string, e.g. '0 8 * * *' for every day at 8am.
        target (str): Task to run.
        kwargs: All other inputs will be forwarded to the target task.
    
    Returns:
        Nothing. Runs forever.
    
    Creates a new instance of the task. Pass inputs as keyword arguments.

    ### Ancestors (in MRO)

    * cowait.tasks.task.Task

    ### Methods

    `execute(self, name: str, image: str, inputs: dict)`
    :

    `reschedule(self, schedule)`
    :

    `run(self, schedule: str, target: str, **inputs)`
    :