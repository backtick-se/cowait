import React from 'react'
import { Bubble, Code } from '../ui'

type Props = {
    result?: object
}

export const TaskResult: React.FC<Props> = ({ result }) => {
    if (!result) {
        return null
    }
    return <Bubble shadow="none">
        <h4>Result</h4>
        <Code language="json">{JSON.stringify(result, null, 4)}</Code>
    </Bubble>
}

export default TaskResult