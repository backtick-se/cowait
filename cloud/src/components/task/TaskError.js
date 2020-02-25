import React from 'react'
import PropTypes from 'prop-types'
import { ErrorOutput, ErrorBubblePadded } from './styled/Error'


export function TaskError({ error }) {
    if (!error) {
        return null
    }
    return <ErrorBubblePadded>
        <h4>Error</h4>
        <ErrorOutput>{error}</ErrorOutput>
    </ErrorBubblePadded>
}

TaskError.propTypes = {
    error: PropTypes.string,
}

TaskError.defaultProps = {
    error: null,
}

export default TaskError