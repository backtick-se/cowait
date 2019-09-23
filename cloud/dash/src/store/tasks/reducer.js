
const DefaultState = {
    order: [ ],
    items: { },
}

export function tasks(state, action) {
    if (typeof(state) == 'undefined') {
        return DefaultState
    }

    switch(action.type) {
    case 'init':
        const { task } = action
        return {
            ...state,
            order: [ ...state.order, task.id ],
            items: {
                ...state.items,
                [task.id]: task,
            },
        }

    case 'status':
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
        
    default:
        return state
    }
}

export default tasks