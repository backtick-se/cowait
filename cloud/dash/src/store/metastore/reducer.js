
const DefaultState = {

}

export function metastore(state, action) {
    if (typeof(state) == 'undefined') {
        return DefaultState
    }

    switch(action.type) {
    default:
        return state
    }
}

export default metastore