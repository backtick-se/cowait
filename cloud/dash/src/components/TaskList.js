import _ from 'lodash'
import React from 'react'
import { connect } from  'react-redux'
import Task from './task/Task'

function TaskList({ task_ids }) {
    return <div>
        <h2>Tasks</h2>
        <ul>
            {_.map(task_ids, task_id => <Task id={task_id} key={task_id} />)}
        </ul>
    </div>
}

const mapStateToProps = state => ({
    task_ids: state.tasks.order,
})
export default connect(mapStateToProps)(TaskList)