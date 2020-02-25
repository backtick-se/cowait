import React from 'react'
import { Bubble } from '../ui'
import TaskLink from './TaskLink'


export function TaskChildren({ children }) {
    if (!React.Children.count(children)) {
        return null
    }
    return <Bubble shadow="none">
        <h4>Children</h4>
        {children.map(child => <TaskLink key={child} id={child} />)}
    </Bubble>
}

export default TaskChildren