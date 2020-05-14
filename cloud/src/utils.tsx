import query from 'query-string'

export function updateToken() {
    const queries = query.parse(window.location.search)
    let token = queries.token

    if (token) {
        if (token instanceof Array) {
            localStorage.setItem('token', token[0])
        } else {
            localStorage.setItem('token', token)
        }
    }
}

export function getToken() {
    return localStorage.getItem('token')
}

export function getWsUrl() {
    // allow override with env
    if (process.env.REACT_APP_AGENT_URL) {
        return process.env.REACT_APP_AGENT_URL.replace('http','ws').replace('?token', 'ws?token')
    }

    // grab token
    const token = getToken()

    // figure out websocket uri from current location
    let wsProto = window.window.location.protocol === 'https:' ? 'wss' : 'ws'
    return `${wsProto}://${window.location.host}/ws?token=${token}`
}
