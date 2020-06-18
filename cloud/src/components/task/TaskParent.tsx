import React from 'react'
import { ContentBlock } from '../ui'
import TaskLink from './TaskLink'


export const TaskParent: React.FC<{ parent?: string | null }> = ({ parent }) => {
    if (!parent) return null
    
    return <ContentBlock>
        <h4>Parent</h4>
        <TaskLink id={parent} />
    </ContentBlock>
}

export default TaskParent