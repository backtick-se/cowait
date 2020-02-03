import React from 'react'
import PropTypes from 'prop-types'
import { connect } from  'react-redux'
import Task from './task/Task'
import TaskItem from './task/TaskItem'

function TaskList({ tasks, render }) {
    return <ul>
        {tasks.map(id => <TaskItem id={id} key={id} render={render} />)}
    </ul>
}

TaskList.defaultProps = {
    tasks: [ ],
    render: Task,
}

TaskList.propTypes = {
    tasks: PropTypes.array.isRequired,
    render: PropTypes.elementType,
}

const mapStateToProps = state => ({
    tasks: state.tasks.order,
})
export default connect(mapStateToProps)(TaskList)