import React from 'react'
import { Bubble } from '../ui'
import TaskLink from './TaskLink'

type Props = {
    sub_tasks: string[]
}

export const TaskSubTasks: React.FC<Props> = ({ sub_tasks }) => {
    if (sub_tasks.length) {
        return null
    }

    return <Bubble shadow="none">
        <h4>Children</h4>
        { sub_tasks.map((id: string) => <TaskLink id={id} />) }
    </Bubble>
}

export default TaskSubTasks