import React from 'react'
import { ContentBlock, Code } from '../ui'

type Props = {
    result?: object
}

export const TaskResult: React.FC<Props> = ({ result }) => {
    if (!result) {
        return null
    }
    return <ContentBlock>
        <h4>Result</h4>
        <Code language="json">{JSON.stringify(result, null, 4)}</Code>
    </ContentBlock>
}

export default TaskResult