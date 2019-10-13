import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'

const TaskBox = styled.div`
    padding: 1rem 0;
`

function Task({ task: { id, status, image, parent, result, error, children } }) {
    return <TaskBox>
        <h2>{id} <TaskStatus status={status} /></h2>
        {parent && <TaskLink id={parent}>Parent: {parent}</TaskLink>}
        <p>Image: {image}</p>
        <p>Children: {JSON.stringify(children)}</p>
        <TaskError error={error} />
        <TaskResult result={result} />
        <TaskLog id={id} />
        {children.map(child => <TaskLink id={child} />)}
    </TaskBox>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(Task)