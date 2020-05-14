import React from 'react'
import { TaskStatusLabel } from './styled/Status'

export const statusIcons: { [status: string]: string } = {
    'wait': 'fa fa-clock',
    'work': 'fa fa-cog fa-spin',
    'done': 'fa fa-check',
    'fail': 'fa fa-times',
    'stop': 'fa fa-stop',
}

export const statusLabels: { [status: string]: string } = {
    'wait': 'Wait',
    'work': 'Running',
    'done': 'Done',
    'fail': 'Fail',
    'stop': 'Stop',
}

type Props = {
    status: string
}

export const TaskStatus: React.FC<Props> = ({ status }) => {
    return <TaskStatusLabel status={status}>
        <i className={statusIcons[status]} />
        <span>{statusLabels[status]}</span>
    </TaskStatusLabel>
}

export default TaskStatus