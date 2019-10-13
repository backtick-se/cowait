import _ from 'lodash'
import zmq from 'zeromq'
import http from 'http'
import express from 'express'
import socketio from 'socket.io'
import { Metastore } from './metastore'

const ZMQ_PORT = 1337
const WS_PORT = 1338

let clients = [ ]

var app = express()
var server = http.Server(app)
var io = socketio(server)

const metastore = new Metastore([ 'task' ])

function handle_update({ id, type, ...msg }) {
    switch(type) {
    case 'init':
        metastore.set('task', id, msg.task) 

    case 'status':
        metastore.update('task', id, task => _.set(task, 'status', msg.status))

    case 'return':
        metastore.update('task', id, task => _.set(task, 'result', msg.result))
        break

    case 'fail':
        metastore.update('task', id, task => _.set(task, 'error', msg.error))
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
    clients.push(client)
    console.log('new client')
    client.emit('msg', {
        'type': 'hello',
    })

    client.on('event', data => { 
        console.log('event', data)
    });
    client.on('disconnect', () => { 
        console.log('disconnect')
    });
});

console.log('listening for nodes')
let sock = zmq.socket("pull");

sock.on("message", function(msg) {
    console.log("recv: %s", msg.toString());
    const event = JSON.parse(msg.toString())

    handle_update(event)
    io.sockets.emit('msg', event)
});

sock.bindSync(`tcp://*:${ZMQ_PORT}`);

server.listen(WS_PORT, () => {
    console.log('listening for websockets')
});

console.log('im on hostname', process.env.HOSTNAME)