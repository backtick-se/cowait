import React from 'react'
import styled from 'styled-components'

const StatusIcons = {
    'wait': 'fa fa-clock',
    'work': 'fa fa-spinner fa-spin',
    'done': 'fa fa-check',
}

const StatusColors = {
    'wait': '#999999',
    'work': '#ffad13',
    'done': 'green',
    'fail': 'red',
}

const StatusLabels = {
    'wait': 'Wait',
    'work': 'Work',
    'done': 'Done',
    'fail': 'Fail',
}

const TaskStatusLabel = styled.label`
    display: inline-block;
    color: ${p => StatusColors[p.status]};
    border: 1px solid ${p => StatusColors[p.status]};
    padding: 0.3rem;
    font-size: 1rem;
    border-radius: 0.3rem;
`

function TaskStatus({ status }) {
    return <TaskStatusLabel status={status}>
        <i class={StatusIcons[status]} />
        <span>{StatusLabels[status]}</span>
    </TaskStatusLabel>
}

export default TaskStatus