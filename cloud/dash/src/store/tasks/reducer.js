
const DefaultState = {
    order: [ ],
    items: { },
    logs: { },
}

export function tasks(state, action) {
    if (typeof(state) == 'undefined') {
        return DefaultState
    }

    switch(action.type) {
    case 'init': {
        const { task } = action
        return {
            ...state,
            order: [ ...state.order, task.id ],
            items: {
                ...state.items,
                [task.id]: task,
            },
        }
    }

    case 'status': {
        const { id, status } = action
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    status,
                },
            },
        }
    }

    case 'log': {
        const { id, data } = action
        return {
            ...state,
            logs: {
                ...state.logs,
                [id]: (state.logs[id] || '') + data,
            },
        }
    }

    case 'return': {
        const { id, result } = action
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    result,
                },
            },
        }
    }

    case 'fail': {
        const { id, error } = action
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    error,
                },
            },
        }
    }
        
    default:
        return state
    }
}

export default tasks