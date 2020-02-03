import React from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'
import { ErrorBubble } from '../ui'


const ErrorOutput = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
    line-height: 1.5em;
`

const ErrorBubblePadded = styled(ErrorBubble)`
    margin: 0 1rem;
`

function TaskError({ error }) {
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