import { EventEmitter } from 'tsee'

const DefaultConnectInterval = 1000


export class PipeClient extends EventEmitter {
    uri: string
    ws?: WebSocket
    reconnectInterval: number
    _reconnectTimeout: number

    constructor(uri: string) {
        super()
        this.uri = uri
        this.reconnectInterval = DefaultConnectInterval
        this._reconnectTimeout = 0
    }

    connect = () => {
        this.close()
        this.emit('connecting')

        let ws = new WebSocket(this.uri)
        ws.onopen = () => {
            this.ws = ws
            this.reconnectInterval = DefaultConnectInterval
            this.emit('connect')
            this.send({
                type: 'subscribe',
            })
        }
        ws.onmessage = msg => {
            const event = JSON.parse(msg.data)
            this.emit('message', event)
        }
        ws.onclose = event => {
            if (event.wasClean) {
                this.emit('close')
            } else {
                this.emit('error', {
                    code: event.code,
                    reason: event.reason,
                })
            }
            
            this.reconnect()
        }
    }

    reconnect = () => {
        clearTimeout(this._reconnectTimeout)
        this._reconnectTimeout = setTimeout(() => this.connect(), this.reconnectInterval)
    }

    close = () => {
        if (this.ws) {
            this.ws.close()
        }
        this.ws = undefined
    }

    send = (msg: object) => {
        if (!this.ws) {
            throw new Error('Not connected')
        }
        this.ws.send(JSON.stringify(msg))
    }
}

export default PipeClient