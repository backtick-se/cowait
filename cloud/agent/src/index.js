import _ from 'lodash'
import http from 'http'
import express from 'express'
import socketio from 'socket.io'
import WebSocket from 'ws'
import { Metastore } from './metastore'

const PORT = 1337
const WS_PORT = 1338

const app = express()
const server = http.Server(app)
const io = socketio(server)

const metastore = new Metastore([ 'task' ])

function handle_update({ id, type, ...msg }) {
    switch(type) {
    case 'init':
        metastore.set('task', id, msg.task) 
        break

    case 'status':
        metastore.update('task', id, task => _.set(task, 'status', msg.status))
        break

    case 'return':
        metastore.update('task', id, task => _.set(task, 'result', msg.result))
        break

    case 'fail':
        metastore.update('task', id, task => _.set(task, 'error', msg.error))
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

io.on('connection', client => { 
    console.log('new client')
    const tasks = metastore.getAll('task')
    for(const task of tasks) {
        client.emit('msg', {
            id: task.id,
            type: 'init',
            task,
        })
    }

    client.on('disconnect', () => { 
        console.log('disconnect')
    });
});


const wss = new WebSocket.Server({ port: PORT })

wss.on('connection', function connection(ws) {
    ws.on('message', msg => {
        console.log("recv: %s", msg.toString());
        const event = JSON.parse(msg.toString())

        try {
            handle_update(event)
        }
        catch(e) {
            console.log('caught error:', e)
        }

        io.sockets.emit('msg', event)
    })
});


// websocket listen
server.listen(WS_PORT, () => {
    console.log('listening for websockets')
});

console.log('im on hostname', process.env.HOSTNAME)