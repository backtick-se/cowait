import query from 'query-string'

export function updateToken() {
    const queries = query.parse(window.location.search)
    let token = queries.token
    localStorage.setItem('token', token)
}

export function getToken() {
    return localStorage.getItem('token')
}

export function getWsUrl() {
    // grab token
    const token = getToken()

    // figure out websocket uri from current location
    let wsProto = window.window.location.protocol === 'https:' ? 'wss' : 'ws'
    return `${wsProto}://${window.location.host}/ws?token=${token}`
}
