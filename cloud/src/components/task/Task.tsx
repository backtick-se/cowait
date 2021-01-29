import React from 'react'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskInputs from './TaskInputs'
import TaskSubTasks from './TaskSubTasks'
import TaskState from './TaskState'
import { TaskHeader, TaskHeaderLink, TaskImage, TaskWrapper, TaskTitleWrapper, TaskCreatedAt, TaskTitle } from './styled/Task'
import { Task as TaskInterface } from '../../store/tasks/types'
import { formatDate } from '../../utils'
import TaskParent from './TaskParent'
import TaskActionBar from './TaskActionBar'


type TaskProps = TaskInterface & {
    maxLogHeight?: number
}

export type TaskComponent = React.FC<TaskProps>

export const Task: TaskComponent = (props: TaskProps) => {
    const { id, status, image, parent, result, error, state, sub_tasks, inputs, maxLogHeight, created_at } = props

    return <TaskWrapper>
        <TaskHeader>
            <TaskTitleWrapper>
                <TaskTitle>
                    <TaskHeaderLink to={`/task/${id}`}>{id}</TaskHeaderLink>
                    <TaskStatus status={status} />
                </TaskTitle>
                <TaskCreatedAt>{formatDate(created_at)}</TaskCreatedAt>
                <TaskActionBar {...props} />
            </TaskTitleWrapper>
            <TaskImage>{image}</TaskImage>
        </TaskHeader>

        <TaskParent parent={parent} />
        <TaskError error={error} />
        <TaskInputs inputs={inputs} />
        <TaskState state={state} />
        <TaskSubTasks sub_tasks={sub_tasks} />
        <TaskLog id={id} maxHeight={maxLogHeight} />
        <TaskResult result={result} />
    </TaskWrapper>
}

export default Task
