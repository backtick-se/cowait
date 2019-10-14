import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'
import TaskChildren from './TaskChildren'

const TaskHeader = styled.div`
    margin-bottom: 1rem;
`

function Task({ task: { id, status, image, parent, result, error, children, inputs } }) {
    return <React.Fragment>
        <TaskHeader>
            <h2>{id} <TaskStatus status={status} /></h2>
            <p>{image}</p>
            {parent && <TaskLink id={parent}>Parent: {parent}</TaskLink>}
        </TaskHeader>

        <TaskError error={error} />
        <TaskInputs inputs={inputs} />
        <TaskChildren children={children} />
        <TaskLog id={id} />
        <TaskResult result={result} />
    </React.Fragment>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(Task)