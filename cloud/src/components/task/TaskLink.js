import React from 'react'
import { useSelector } from 'react-redux'
import { Link } from '../ui'
import { LinkWrapper } from './styled/Link'
import TaskStatus from './TaskStatus'


export function TaskLink({ id }) {
    const { status } = useSelector(state => state.tasks.items[id])
    return <LinkWrapper>
        <Link to={`/task/${id}`}>{id}</Link>
        <TaskStatus status={status} />
    </LinkWrapper>
}

export default TaskLink