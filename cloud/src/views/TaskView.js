import React from 'react'
import { useParams } from 'react-router-dom'
import { View } from '../components/ui'
import TaskItem from '../components/task/TaskItem'

function TaskView() {
    let { taskId } = useParams()

    return <View title={taskId}>
        <TaskItem id={taskId} maxLogHeight={40} />
    </View>
}

export default TaskView