import React from 'react'
import styled from 'styled-components'
import { Bubble, CodeBlock } from '../ui'

const ErrorBubble = styled(Bubble)`
    color: white;
    background-color: ${p => p.theme.colors.status.fail};
`

function TaskError({ error }) {
    if (!error) {
        return null
    }
    return <ErrorBubble>
        <h4>Error</h4>
        <CodeBlock>{error}</CodeBlock>
    </ErrorBubble>
}

export default TaskError