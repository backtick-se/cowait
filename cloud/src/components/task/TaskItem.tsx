import React from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'
import Task from './Task'

type Props = {
    id: string,
    render?: React.FC,
    maxLogHeight?: number
}

export const TaskItem: React.FC<Props> = ({ id, render = Task, ...props }) => {
    const task = useSelector((state: RootState) => state.tasks.items[id])
    if (!task) {
        return null
    }

    const RenderElement = render
    return <RenderElement {...task} {...props} />
}

export default TaskItem