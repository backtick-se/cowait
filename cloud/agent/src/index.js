const io = require('socket.io')();
var zmq = require("zeromq");

let clients = [ ]

io.on('connection', client => { 
    clients.push(client)
    console.log('new client')
    client.send({
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
    io.sockets.send(msg)
});

sock.bindSync("tcp://*:1337");

setInterval(function() {
    console.log("heartbeat");
    io.sockets.send({ type: "heartbeat" });
}, 5000);

console.log('listening for websockets')
io.listen(1338);


