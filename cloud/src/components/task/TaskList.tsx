import React from 'react'
import { useSelector } from  'react-redux'
import styled from 'styled-components'

import { FlexBox } from '../ui/FlexBox'
import TaskItem from './TaskItem'
import { RootState } from '../../store'
import { Task } from '../../store/tasks/types'
import { TaskListEmptyItem } from './styled/List'


const TaskListWrapper = styled(FlexBox)`
    flex-direction: column;
    flex: 1;

    h2 {
        margin-bottom: 1rem;
    }
`

type Props = {
    render?: React.FC<any>
    title?: string | null,
    predicate?: (task: Task) => boolean
}

export const TaskList: React.FC<Props> = ({ render, title, predicate }) => {
    const order = useSelector((state: RootState) => state.tasks.order)
    const tasks = useSelector((state: RootState) => state.tasks.items)
    const taskIds = order
        .map(taskId => tasks[taskId])
        .filter(task => predicate ? predicate(task) : true)
        .map(task => task.id)

    return <TaskListWrapper>
        {title ? <h2>{title}</h2> : ''}
        <ul>
            { !taskIds.length && <TaskListEmptyItem>Empty list</TaskListEmptyItem>}
            { taskIds.map(id => <TaskItem id={id} key={id} render={render} />) }
        </ul>
    </TaskListWrapper>
}

export default TaskList