import _ from 'lodash'
import express from 'express'
import expressWs from 'express-ws'
import EventEmitter from 'events'
import { Metastore } from './metastore'

const PORT = 1337

const app = express()
expressWs(app)

const metastore = new Metastore([ 'task' ])
let subscribers = [ ]
let tasks = [ ]

function handle_update({ id, type, ...msg }, conn) {
    switch(type) {
    case 'subscribe':
        subscribers.push(conn)
        conn.send({
            type: 'subscribed',
            channels: ['events'],
        })
        console.log('added subscriber')
        break

    case 'init':
        metastore.set('task', id, msg.task) 
        tasks[id] = conn
        break

    case 'status':
        metastore.update('task', id, task => _.set(task, 'status', msg.status))
        break

    case 'return':
        metastore.update('task', id, task => _.set(task, 'result', msg.result))
        delete tasks[id]
        break

    case 'fail':
        metastore.update('task', id, task => _.set(task, 'error', msg.error))
        delete tasks[id]
        break

    case 'log':
        metastore.update('task', id, task => {
            const log = (task.log || '') + msg.data
            return _.set(task, 'log', log)
        })
        break

    case 'object':
        // other metadata
        metastore.set(msg.kind, msg.data)
        break
    }
}

app.get('/meta/:kind', async (req, res) => {
    res.json(metastore.getAll(req.params.kind))
})

app.get('/meta/:kind/:id', async (req, res) => {
    res.json(metastore.get(req.params.kind, req.params.id))
})

class Connection extends EventEmitter {
    constructor(ws) {
        super()
        this.ws = ws
    }

    send = msg => {
        this.ws.send(JSON.stringify(msg))
    }
}

app.ws('/', (ws, req) => {
    let conn = new Connection(ws)
    console.log('new client')

    const tasks = metastore.getAll('task')
    for(const task of tasks) {
        conn.send({
            id: task.id,
            type: 'init',
            task,
        })
    }

    ws.on('message', msg => {
        const event = JSON.parse(msg.toString())
        console.log(event)

        try {
            handle_update(event, conn)
        }
        catch(e) {
            console.log('caught error:', e)
        }

        _.each(subscribers, sub => sub.send(event))
    })

    ws.on('close', () => {
        console.log('remove subscriber')
        subscribers = _.filter(subscribers, sub => sub.ws !== ws)
    })
})

app.listen(PORT, () => {
    console.log('im on hostname', process.env.HOSTNAME)
})