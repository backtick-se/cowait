var zmq = require("zeromq")
var http = require("http")
var socketio = require("socket.io")

let clients = [ ]
function handler (req, res) {
    res.end('hello sir')
}

const ZMQ_PORT = 1337
const WS_PORT = 1338

var app = http.createServer(handler)
var io = socketio(app)


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
    console.log("work: %s", msg.toString());
    io.sockets.emit('msg', JSON.parse(msg.toString()))
});

sock.bindSync(`tcp://*:${ZMQ_PORT}`);

app.listen(WS_PORT, () => {
    console.log('listening for websockets')
});

console.log('im on hostname', process.env.HOSTNAME)