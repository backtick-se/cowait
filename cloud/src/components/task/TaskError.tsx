import React from 'react'
import { ErrorOutput, ErrorBubblePadded } from './styled/Error'

type Props = {
    error: string | null
}

export const TaskError: React.FC<Props> = ({ error = null }) => {
    if (!error) {
        return null
    }
    return <ErrorBubblePadded>
        <h4>Error</h4>
        <ErrorOutput>{error}</ErrorOutput>
    </ErrorBubblePadded>
}

export default TaskError