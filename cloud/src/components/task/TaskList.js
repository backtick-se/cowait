import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from  'react-redux'
import Task from './Task'
import TaskItem from './TaskItem'


export function TaskList({ render }) {
    const taskIds = useSelector(state => state.tasks.order)
    return <ul>
        {taskIds.map(id => <TaskItem id={id} key={id} render={render} />)}
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

export default TaskList