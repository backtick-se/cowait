import React from 'react'
import { Bubble, CodeBlock } from '../ui'

function TaskInputs({ inputs }) {
    if (!inputs) {
        return null
    }
    return <Bubble>
        <h4>Inputs</h4>
        <CodeBlock>{JSON.stringify(inputs, null, 4)}</CodeBlock>
    </Bubble>
}

export default TaskInputs