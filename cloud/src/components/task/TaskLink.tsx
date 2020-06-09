import React from 'react'
import { useSelector } from 'react-redux'
import { Link } from '../ui'
import { LinkWrapper } from './styled/Link'
import TaskStatus from './TaskStatus'
import { RootState } from '../../store'

type Props = {
    id: string
}

export const TaskLink: React.FC<Props> = ({ id }) => {
    const { status } = useSelector((state: RootState) => state.tasks.items[id])
    return <LinkWrapper>
        <Link to={`/task/${id}`}>{id}</Link>
        <TaskStatus status={status} />
    </LinkWrapper>
}

export default TaskLink