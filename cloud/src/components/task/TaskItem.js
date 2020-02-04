import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import Task from './Task'

function TaskItem({ id, task, render, ...props }) {
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

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(TaskItem)