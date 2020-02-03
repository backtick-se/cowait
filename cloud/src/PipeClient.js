import EventEmitter from 'events'

export class PipeClient extends EventEmitter {
    constructor(uri) {
        super()
        this.uri = uri
        this.ws = false
    }

    connect = () => {
        this.close()

        let ws = new WebSocket(this.uri)
        ws.onopen = () => {
            this.ws = ws
            console.log(`connected to ${this.uri}`)
            this.emit('connect')
            this.send({
                type: 'subscribe',
            })
        }
        ws.onmessage = msg => {
            console.log(msg.data)
            const event = JSON.parse(msg.data)
            this.emit('message', event)
        }
        ws.onerror = err => {
            console.error(err)
            this.emit('error', err)
            setTimeout(() => this.connect(), 1000)
        }
        ws.onclose = () => {
            console.log('ws closed')
            this.emit('close')
            setTimeout(() => this.connect(), 1000)
        }
    }

    close = () => {
        if (this.ws) {
            this.ws.close()
        }
        this.ws = false
    }

    send = msg => {
        if (!this.ws) {
            throw new Error('Not connected')
        }
        this.ws.send(JSON.stringify(msg))
    }
}

export default PipeClient