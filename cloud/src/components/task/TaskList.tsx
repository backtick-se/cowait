import React from 'react'
import { useSelector } from  'react-redux'

import TaskItem from './TaskItem'
import { RootState } from '../../store'

type Props = {
    render?: React.FC<any>
}

export const TaskList: React.FC<Props> = ({ render }) => {
    const taskIds = useSelector((state: RootState) => state.tasks.order)
    return <ul>
        { taskIds.map(id => <TaskItem id={id} key={id} render={render} />) }
    </ul>
}

export default TaskList