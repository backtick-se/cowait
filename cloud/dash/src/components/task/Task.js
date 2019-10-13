import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'

const TaskBox = styled.div`
    padding: 1rem 0;
`

const TaskChildrenBox = styled.div`
    padding: 0.5rem 0;
    h4 {
        font-size: 1.1rem;
        font-weight: bold;
    }
`

function TaskChildren({ children }) {
    return <TaskChildrenBox>
        <h4>Children</h4>
        {children.map(child => <TaskLink key={child} id={child} />)}
    </TaskChildrenBox>
}

function Task({ task: { id, status, image, parent, result, error, children, inputs } }) {
    return <TaskBox>
        <h2>{id} <TaskStatus status={status} /></h2>
        <p>Image: {image}</p>
        {parent && <TaskLink id={parent}>Parent: {parent}</TaskLink>}
        <TaskInputs inputs={inputs} />
        <TaskError error={error} />
        <TaskChildren children={children} />
        <TaskLog id={id} />
        <TaskResult result={result} />
    </TaskBox>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(Task)