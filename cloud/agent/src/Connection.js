import EventEmitter from 'events'

export class Connection extends EventEmitter {
    constructor(ws) {
        super()
        this.ws = ws

        this.ws.on('message', msg => {
            const event = JSON.parse(msg.toString())
            this.emit('message', event)
        })

        this.ws.on('close', () => {
            this.emit('close')
        })
    }

    send = msg => {
        this.ws.send(JSON.stringify(msg))
    }
}

export default Connection