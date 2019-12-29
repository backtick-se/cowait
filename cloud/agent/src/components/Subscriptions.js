import _ from 'lodash'

export class Subscriptions {
    constructor(agent) {
        this.subscribers = [ ]

        agent.on('subscribe', (msg, conn) => this.subscribe(conn))
        agent.on('close', this.unsubscribe)

        agent.on('event', event => {
            agent.send(event, this.subscribers)
        })
    }

    subscribe = conn => {
        this.subscribers.push(conn)
        conn.send({ type: 'subscribed' })
    }

    unsubscribe = conn => {
        this.subscribers = _.filter(this.subscribers, sub => sub.ws !== conn.ws)
        //conn.send({ type: 'unsubscribed' })
    }
}

export default Subscriptions