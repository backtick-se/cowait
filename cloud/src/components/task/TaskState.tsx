import React from 'react'
import { ContentBlock, Code } from '../ui'
import TaskGraph from './task-ui/TaskGraph'

type Props = {
    state: State
}

type State = {
    ui?: TaskComponent[]
    [key: string]: any
}

type TaskComponent = {
    component: string
    path: string
}

function renderComponent(def: TaskComponent, state: State) {
    switch(def.component) {
        case 'ui.cowait.io/task-graph':
            return <TaskGraph graph={state[def.path]} />
        default:
            throw new Error(`Unknown Task Component ${def.component}`)
    }
}

export const TaskState: React.FC<Props> = ({ state }) => {
    if (!state) {
        return null
    }
    const components = state.ui || []

    return <ContentBlock>
        <h4>State</h4>
        {components.map(c => renderComponent(c, state))}
    </ContentBlock>
    // <Code language="json">{JSON.stringify(state, null, 4)}</Code>
}

export default TaskState
