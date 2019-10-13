import React from 'react'
import styled from 'styled-components'

const TaskResultBox = styled.div`
    padding: 0.5rem 0;
    h4 {
        font-size: 1.1rem;
    }
    pre {
        font-family: monospace;
    }
`

function TaskResult({ result }) {
    if (!result) {
        return null
    }
    return <TaskResultBox>
        <h4>Result</h4>
        <pre>{JSON.stringify(result, null, 4)}</pre>
    </TaskResultBox>
}

export default TaskResult