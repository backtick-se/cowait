import React from 'react'
import { Bubble, Code } from '../ui'

type Props = {
    inputs: object | null
}

export const TaskInputs: React.FC<Props> = ({ inputs }) => {
    if (!inputs) {
        return null
    }
    return <Bubble shadow="none">
        <h4>Inputs</h4>
        <Code language="json">{JSON.stringify(inputs, null, 4)}</Code>
    </Bubble>
}

export default TaskInputs