
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
        if (!task.parent) {
            return {
                ...state,
                order: [ task.id, ...state.order ],
                items: {
                    ...state.items,
                    [task.id]: {
                        ...task,
                        children: [ ],
                    },
                },
                logs: {
                    ...state.logs,
                    [task.id]: task.log || '',
                },
            }
        }
        else {
            const parent = state.items[task.parent]
            return {
                ...state,
                items: {
                    ...state.items,
                    [task.id]: {
                        ...task,
                        children: [ ],
                    },
                    [task.parent]: {
                        ...parent,
                        children: [ ...parent.children, task.id ],
                    },
                },
                logs: {
                    ...state.logs,
                    [task.id]: task.log || '',
                },
            }
        }
    }

    case 'status': {
        const { id, status } = action
        const item = state.items[id]
        if (!item) {
            console.log('unknown task', id)
            return state
        }
        if (item.status === 'fail' || item.status === 'done') {
            console.log('cant change status on', id, 'its already', item.status)
            return state
        }
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