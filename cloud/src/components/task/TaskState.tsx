import React from 'react'
import { ContentBlock, Code } from '../ui'

type Props = {
    state?: object
}

export const TaskState: React.FC<Props> = ({ state }) => {
    if (!state) {
        return null
    }
    return <ContentBlock>
        <h4>State</h4>
        <Code language="json">{JSON.stringify(state, null, 4)}</Code>
    </ContentBlock>
}

export default TaskState
