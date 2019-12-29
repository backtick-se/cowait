import express from 'express'
import expressWs from 'express-ws'
import { Metastore } from './metastore'
import { TaskAgent } from './TaskAgent'
import { Subscriptions, MetastoreFeed } from './components'

const PORT = process.env.PORT || 1337

const app = express()
expressWs(app)

// create metastore
const metastore = new Metastore([ 'task' ])
app.get('/meta/:kind', (req, res) => { res.json(metastore.getAll(req.params.kind)) })
app.get('/meta/:kind/:id', (req, res) => { res.json(metastore.get(req.params.kind, req.params.id)) })

// create task agent
const agent = new TaskAgent()
agent.attach(Subscriptions)
agent.attach(MetastoreFeed, metastore)
app.ws('/', agent.handle)

// logs
agent.on('subscribe', () => { console.log('added subscriber') })
agent.on('close', () => { console.log('removed subscriber') })
agent.on('connect', conn => {
    conn.send({
        type: 'test',
        msg: 'hello world',
    })
})

// create express app
app.listen(PORT, () => {
    console.log('im on hostname', process.env.HOSTNAME)
})