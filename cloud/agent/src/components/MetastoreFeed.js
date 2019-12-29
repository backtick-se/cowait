import _ from 'lodash'

export class MetastoreFeed {
    constructor(agent, metastore) {
        // broadcast metastore to new subscribers
        agent.on('subscribe', (msg, conn) => {
            const tasks = metastore.getAll('task')
            _.each(tasks, task => {
                conn.send({
                    id: task.id,
                    type: 'init',
                    task,
                })
            })
        })

        //
        // update metastore with task information
        //

        agent.on('init', ({ id, task }) => {
            metastore.set('task', id, task) 
        })

        agent.on('status', ({ id, status }) => {
            metastore.update('task', id, task => _.set(task, 'status', status))
        })

        agent.on('return', ({ id, result }) => {
            metastore.update('task', id, task => _.set(task, 'result', result))
        })

        agent.on('fail', ({ id, error }) => {
            metastore.update('task', id, task => _.set(task, 'error', error))
        })

        agent.on('log', ({ id, data }) => {
            metastore.update('task', id, task => {
                const log = (task.log || '') + data
                return _.set(task, 'log', log)
            })
        })

        agent.on('return', ({ kind, data }) => {
            metastore.set(kind, data)
        })
    }
}

export default MetastoreFeed