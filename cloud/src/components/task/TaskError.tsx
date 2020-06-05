import React from 'react'
import { ErrorOutput } from './styled/Error'
import { ErrorBubble } from '../ui'

type Props = {
    error: string | null
}

export const TaskError: React.FC<Props> = ({ error = null }) => {
    if (!error) {
        return null
    }
    return <ErrorBubble>
        <h4>Error</h4>
        <ErrorOutput>{error}</ErrorOutput>
    </ErrorBubble>
}

export default TaskError