import React from 'react'

function Task({ id, status, image }) {
    return <p>{id}: {status}</p>
}

export default Task