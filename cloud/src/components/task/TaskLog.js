
import React, { useEffect, useRef } from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import { Bubble } from '../ui'

const LogOutput = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
    color: white;
    line-height: 1.25em;
`

const LogContainer = styled.div`
    padding: 0.5rem;
    background-color: #222;
    border-radius: 0.3rem;
    overflow: auto;
    min-height: ${p => p.minHeight || 6}rem;
    max-height: ${p => p.maxHeight || 12}rem;
`

function TaskLog({ log, maxHeight }) {
    let logRef = useRef(null)

    const scrollToBottom = () => {
        if (!logRef.current) {
            return
        }
        logRef.current.scrollTop = logRef.current.scrollHeight
    }
    useEffect(scrollToBottom, [ log ])

    if (!log) {
        return null
    }

    return <Bubble shadow="none">
        <h4>Output Log</h4>
        <LogContainer ref={logRef} maxHeight={maxHeight}>
            <LogOutput>{log}</LogOutput>
        </LogContainer>
    </Bubble>
}

const mapStateToProps = (state, props) => ({
    log: state.tasks.logs[props.id],
})
export default connect(mapStateToProps)(TaskLog)