import React from 'react'
import styled from 'styled-components'
import { connect } from  'react-redux'
import Task from './task/Task'

const TaskListContainer = styled.ul`
`

function TaskList({ task_ids }) {
    return <TaskListContainer>
        {task_ids.map(task_id => <Task id={task_id} key={task_id} />)}
    </TaskListContainer>
}

const mapStateToProps = state => ({
    task_ids: state.tasks.order,
})
export default connect(mapStateToProps)(TaskList)