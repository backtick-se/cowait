import React from 'react'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'
import TaskSubTasks from './TaskSubTasks'
import { TaskHeader, TaskHeaderLink, TaskImage, TaskWrapper, ParentWrapper } from './styled/Task'
import { Task as TaskInterface } from '../../store/tasks/types'

type TaskProps = TaskInterface & {
    maxLogHeight?: number
}

export type TaskComponent = React.FC<TaskProps>

export const Task: TaskComponent = ({ id, status, image, parent, result, error, sub_tasks, inputs, maxLogHeight }) => {
    return <TaskWrapper>
        <TaskHeader>
            <h2>
                <TaskHeaderLink to={`/task/${id}`}>{id}</TaskHeaderLink> 
                <TaskStatus status={status} />
            </h2>
            <TaskImage>{image}</TaskImage>
            {parent && <ParentWrapper>
                <TaskLink id={parent}/>
            </ParentWrapper>}
        </TaskHeader>

        <TaskError error={error} />
        <TaskInputs inputs={inputs} />
        <TaskSubTasks sub_tasks={sub_tasks} />
        <TaskLog id={id} maxHeight={maxLogHeight} />
        <TaskResult result={result} />
    </TaskWrapper>
}

export default Task