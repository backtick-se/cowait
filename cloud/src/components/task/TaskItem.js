import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import Task from './Task'


export function TaskItem({ id, render, ...props }) {
    const task = useSelector(state => state.tasks.items[id])
    if (!task) {
        return <p>loading</p>
    }

    const RenderElement = render
    return <RenderElement {...task} {...props} />
}

TaskItem.defaultProps = {
    render: Task,
}

TaskItem.propTypes = {
    render: PropTypes.elementType.isRequired,
}

export default TaskItem