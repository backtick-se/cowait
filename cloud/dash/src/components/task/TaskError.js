import React from 'react'
import styled from 'styled-components'

const TaskErrorBox = styled.div`
    padding: 0.5rem;
    color: white;
    background-color: red;

    h4 {
        font-size: 1.1rem;
    }
    pre {
        font-family: monospace;
    }
`

function TaskError({ error }) {
    if (!error) {
        return null
    }
    return <TaskErrorBox>
        <h4>Error</h4>
        <pre>{error}</pre>
    </TaskErrorBox>
}

export default TaskError