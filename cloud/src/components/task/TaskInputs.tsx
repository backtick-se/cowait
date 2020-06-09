import React from 'react'
import { Code, ContentBlock } from '../ui'


type Props = {
    inputs: object | null
}

export const TaskInputs: React.FC<Props> = ({ inputs }) => {
    if (!inputs) {
        return null
    }
    return <ContentBlock>
        <h4>Inputs</h4>
        <Code language="json">{JSON.stringify(inputs, null, 4)}</Code>
    </ContentBlock>
}

export default TaskInputs