import React from 'react'
import styled from 'styled-components'

const TaskInputBox = styled.div`
    padding: 0.5rem 0;
    h4 {
        font-size: 1.1rem;
        font-weight: bold;
    }
    pre {
        font-family: ${p => p.theme.fonts.monospace};
    }
`

function TaskInputs({ inputs }) {
    if (!inputs) {
        return null
    }
    return <TaskInputBox>
        <h4>Inputs</h4>
        <pre>{JSON.stringify(inputs, null, 4)}</pre>
    </TaskInputBox>
}

export default TaskInputs