import React from 'react'
import { ContentBlock } from '../ui'
import TaskLink from './TaskLink'

type Props = {
    sub_tasks: string[]
}

export const TaskSubTasks: React.FC<Props> = ({ sub_tasks }) => {
    if (!sub_tasks.length) {
        return null
    }

    return <ContentBlock>
        <h4>Children</h4>
        { sub_tasks.map((id, idx) => <TaskLink id={id} key={idx}/>) }
    </ContentBlock>
}

export default TaskSubTasks