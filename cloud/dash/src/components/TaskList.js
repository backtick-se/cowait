import _ from 'lodash'
import React from 'react'
import { connect } from  'react-redux'
import Task from './Task'

function TaskList({ tasks }) {
    return <div>
        <h2>tasks</h2>
        <ul>
            {_.map(tasks, task => <Task {...task} />)}
        </ul>
    </div>
}

const mapStateToProps = state => ({
    tasks: state.tasks.items,
})
export default connect(mapStateToProps)(TaskList)