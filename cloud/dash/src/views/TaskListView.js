import React from 'react'
import TaskList from '../components/TaskList'
import { View } from '../components/ui'

function TaskListView({ }) {
    return <View title="tasks">
        <TaskList />
    </View>
}

export default TaskListView