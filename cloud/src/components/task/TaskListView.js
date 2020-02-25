import React from 'react'
import TaskList from './TaskList'
import { View } from '../ui'


export function TaskListView() {
    return <View title="tasks">
        <TaskList />
    </View>
}

export default TaskListView