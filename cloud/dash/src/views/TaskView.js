import React from 'react'
import { useParams } from 'react-router-dom'
import Task from '../components/task/Task'

function TaskView({ }) {
    let { taskId } = useParams();
    return <Task id={taskId} />
}

export default TaskView