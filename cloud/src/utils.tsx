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

export function getToken(): string | null {
    return localStorage.getItem('token')
}

export function getWsUrl(): string {
    // allow override with env
    if (process.env.REACT_APP_AGENT_URL) {
        return process.env.REACT_APP_AGENT_URL.replace('http', 'ws').replace('?token', 'ws?token')
    }

    // grab token
    const token = getToken()

    // figure out websocket uri from current location
    let wsProto = window.window.location.protocol === 'https:' ? 'wss' : 'ws'
    return `${wsProto}://${window.location.host}/ws?token=${token}`
}

/**
 * Converts a CSS hex color value to RGBA.
 * @param {string} hex - Expanded hexadecimal CSS color value.
 * @param {number} alpha - Alpha as a decimal.
 * @returns {string} RGBA CSS color value.
 */
export function hex2Rgba(hex: string, alpha: number): string {
    const fullHex = hex.length < 6 ? hex + hex[hex.length - 1].repeat(6 - hex.length) : hex

    const r = parseInt(fullHex.substring(1, 3), 16)
    const g = parseInt(fullHex.substring(3, 5), 16)
    const b = parseInt(fullHex.substring(5, 7), 16)
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

/**
 * Loads a value from local storage by key.
 * @param {string} key - Key the value is stored by
 * @returns {any} Stored value
 */
export const loadFromLocalStorage = (key: string): any => {
    try {
        const serialized = localStorage.getItem(key);
        if (serialized === null) {
            return undefined;
        }
        return JSON.parse(serialized);
    } catch (err) {
        return undefined;
    }
};

/**
 * Saves a value to local storage by key.
 * @param {string} key - Key to store the value by
 * @param {any} value - Key to store the value by
 */
export const saveToLocalStorage = (key: string, value: any): void => {
    try {
        const serialized = JSON.stringify(value);
        localStorage.setItem(key, serialized);
    } catch {
        // ignore write errors
    }
}; 