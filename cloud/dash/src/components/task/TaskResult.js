import React from 'react'
import { Bubble, CodeBlock } from '../ui'

function TaskResult({ result }) {
    if (!result) {
        return null
    }
    return <Bubble>
        <h4>Result</h4>
        <CodeBlock>{JSON.stringify(result, null, 4)}</CodeBlock>
    </Bubble>
}

export default TaskResult