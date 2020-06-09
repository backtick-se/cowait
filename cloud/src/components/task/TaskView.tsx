import React from 'react'
import { useParams } from 'react-router-dom'
import { View } from '../ui'
import TaskItem from './TaskItem'


export function TaskView() {
    let { taskId } = useParams()

    return <View title={taskId}>
        <TaskItem id={taskId} maxLogHeight={40} />
    </View>
}

export default TaskView