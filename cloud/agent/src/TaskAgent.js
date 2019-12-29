import _ from 'lodash'
import EventEmitter from 'events'
import Connection from './Connection'

const AllConnections = conn => true

export class TaskAgent extends EventEmitter {
    constructor() {
        super()
        this.connections = [ ]
        this.components = [ ]
    }

    attach = (Component, ...args) => {
        this.components.push(new Component(this, ...args))
    }

    handle = ws => {
        let conn = new Connection(ws)
        this.connections.push(conn)
    
        conn.on('message', event => {
            const { type, ...msg } = event
            this.emit('event', event, conn)
            this.emit(type, msg, conn)
        })

        conn.on('close', () => {
            this.connections = _.filter(this.connections, c => c.ws !== conn.ws)
            this.emit('close', conn)
        })

        this.emit('connect', conn)
    }

    send = (msg, predicate = AllConnections) => {
        // send to matching connections if predicate is a function
        if (_.isFunction(predicate)) {
            _.each(this.connections, conn => {
                if (predicate(conn)) {
                    conn.send(msg)
                }
            })
            return
        }

        // send to each connection if predicate is an array
        if (_.isArray(predicate)) {
            _.each(predicate, conn => conn.send(msg))
            return
        }

        throw new Error('Expected predicate to be a function or an array')
    }
}

export default TaskAgent