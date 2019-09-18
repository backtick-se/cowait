import zmq
import json
from pipeline.engine import TaskDefinition
        

class ParentTask(object):
    """ Serves as the base class for all tasks with children """

    def __init__(self):
        self.tasks = [ ]

    def run(self, context, inputs):
        port = 1337
        mq = zmq.Context()

        # server socket
        daemon = mq.socket(zmq.PULL)
        daemon.bind(f'tcp://*:{port}')

        # create tasks
        self.schedule(context, inputs)

        # pass data to parent
        results = { }
        while True:
            msg = daemon.recv_json()
            context.send(msg) # pass to parent

            if msg['type'] == 'return':
                results[msg['id']] = msg['result']
                if len(results) == len(self.tasks):
                    # everything returned
                    break

        return results
        

    def spawn(self, context, **kwargs):
        taskdef = TaskDefinition(**kwargs)
        task = context.cluster.spawn(taskdef)
        self.tasks.append(task)
        return task

        
    def schedule(self, context, inputs):
        for duration in inputs['durations']:
            self.spawn(
                context,
                name='lazy-child',
                image='johanhenriksson/pipeline-task:lazy',
                inputs={
                    'duration': duration,
                },
            )