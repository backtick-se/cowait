import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'

const TaskBox = styled.div`
    padding: 1rem 0;
`

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