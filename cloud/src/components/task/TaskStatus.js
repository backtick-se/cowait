import React from 'react'
import { TaskStatusLabel } from './styled/Status'

export const StatusIcons = {
    'wait': 'fa fa-clock',
    'work': 'fa fa-cog fa-spin',
    'done': 'fa fa-check',
    'fail': 'fa fa-times',
    'stop': 'fa fa-stop',
}

export const StatusLabels = {
    'wait': 'Wait',
    'work': 'Running',
    'done': 'Done',
    'fail': 'Fail',
    'stop': 'Stop',
}


export function TaskStatus({ status }) {
    return <TaskStatusLabel status={status}>
        <i className={StatusIcons[status]} />
        <span>{StatusLabels[status]}</span>
    </TaskStatusLabel>
}

export default TaskStatus