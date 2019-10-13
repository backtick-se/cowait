import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import TaskLog from './TaskLog'

const TaskBox = styled.div`
    padding: 1rem 0;
`

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

const TaskErrorBox = styled.div`
    padding: 0.5rem;
    color: white;
    background-color: red;

    h4 {
        font-size: 1.1rem;
    }
`

const TaskResultBox = styled.div`
    padding: 0.5rem 0;
    h4 {
        font-size: 1.1rem;
    }
    pre {
        font-family: monospace;
    }
`

function TaskError({ error }) {
    if (!error) {
        return null
    }
    return <TaskErrorBox>
        <h4>Error</h4>
        <pre>{error}</pre>
    </TaskErrorBox>
}

function TaskResult({ result }) {
    if (!result) {
        return null
    }
    return <TaskResultBox>
        <h4>Result</h4>
        <pre>{JSON.stringify(result, null, 4)}</pre>
    </TaskResultBox>
}

function Task({ task: { id, status, image, parent, result, error } }) {
    return <TaskBox>
        <h2>{id} <TaskStatus status={status} /></h2>
        {parent && <p>Parent: {parent}</p>}
        <p>Image: {image}</p>
        <TaskError error={error} />
        <TaskResult result={result} />
        <TaskLog id={id} />
    </TaskBox>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(Task)