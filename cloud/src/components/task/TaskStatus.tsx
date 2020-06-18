import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { IconName } from '@fortawesome/fontawesome-svg-core';
import { TaskStatusLabel } from './styled/Status'


export const statusIcons: { [status: string]: string } = {
    'wait': 'clock',
    'work': 'cog',
    'done': 'check',
    'fail': 'times',
    'stop': 'stop',
}

export const statusLabels: { [status: string]: string } = {
    'wait': 'Waiting',
    'work': 'Running',
    'done': 'Done',
    'fail': 'Failed',
    'stop': 'Stopped',
}

type Props = {
    status: string,
}

export const TaskStatus: React.FC<Props> = ({ status }) => {
    return <TaskStatusLabel status={status}>
        <FontAwesomeIcon icon={statusIcons[status || 'wait'] as IconName} spin={status === ('work' || 'wait')}/>
        <span>{statusLabels[status]}</span>
    </TaskStatusLabel>
}

export default TaskStatus