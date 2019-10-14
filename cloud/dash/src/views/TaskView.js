import React from 'react'
import { useParams } from 'react-router-dom'
import Task from '../components/task/Task'
import { View, Header } from '../components/ui'

function TaskView({ }) {
    let { taskId } = useParams();

    return <View title={taskId}>
        <Task id={taskId} />
    </View>
}

export default TaskView