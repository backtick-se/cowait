import React from 'react'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'
import TaskChildren from './TaskChildren'
import { TaskHeader, TaskHeaderLink, TaskImage, TaskWrapper, ParentWrapper } from './styled/Task'


export function Task({ id, status, image, parent, result, error, children, inputs, maxLogHeight }) {
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
        <TaskChildren children={children} />
        <TaskLog id={id} maxHeight={maxLogHeight} />
        <TaskResult result={result} />
    </TaskWrapper>
}

export default Task