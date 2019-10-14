import React from 'react'
import styled from 'styled-components'

const StatusIcons = {
    'wait': 'fa fa-clock',
    'work': 'fa fa-cog fa-spin',
    'done': 'fa fa-check',
    'fail': 'fa fa-times',
    'stop': 'fa fa-stop',
}

const StatusLabels = {
    'wait': 'Wait',
    'work': 'Work',
    'done': 'Done',
    'fail': 'Fail',
    'stop': 'Stop',
}

const TaskStatusLabel = styled.label`
    display: inline-block;
    color: ${p => p.theme.colors.status[p.status]};
    border: 1px solid ${p => p.theme.colors.status[p.status]};
    padding: 0.3rem;
    font-size: 1rem;
    border-radius: 0.3rem;
    
    .fa {
        margin-right: 0.3rem;
    }
`

function TaskStatus({ status }) {
    return <TaskStatusLabel status={status}>
        <i className={StatusIcons[status]} />
        <span>{StatusLabels[status]}</span>
    </TaskStatusLabel>
}

export default TaskStatus