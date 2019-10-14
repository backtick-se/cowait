import React from 'react'
import { Bubble } from '../ui'
import TaskLink from './TaskLink'

function TaskChildren({ children }) {
    if (!React.Children.count(children)) {
        return null
    }
    return <Bubble>
        <h4>Children</h4>
        {children.map(child => <TaskLink key={child} id={child} />)}
    </Bubble>
}

export default TaskChildren