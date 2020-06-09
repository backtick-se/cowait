import React from 'react'
import { ErrorOutput } from './styled/Error'
import { ContentBlock } from '../ui'

type Props = {
    error: string | null
}

export const TaskError: React.FC<Props> = ({ error = null }) => {
    if (!error) {
        return null
    }
    console.log(error);
    return <ContentBlock>
        <h4>Error</h4>
        <ErrorOutput>{error}</ErrorOutput>
    </ContentBlock>
}

export default TaskError