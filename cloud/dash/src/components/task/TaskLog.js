
import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import { Bubble } from '../ui'

const LogOutput = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
    padding: 0.5rem;
    background-color: #222;
    border-radius: 0.3rem;
    color: white;
    overflow-x: auto;

    line-height: 1.25em;
`

function TaskLog({ log }) {
    if (!log) {
        return null
    }
    return <Bubble shadow="none">
        <h4>Output Log</h4>
        <LogOutput>{log}</LogOutput>
    </Bubble>
}

const mapStateToProps = (state, props) => ({
    log: state.tasks.logs[props.id],
})
export default connect(mapStateToProps)(TaskLog)