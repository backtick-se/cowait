
import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'

const LogOutput = styled.pre`
    font-family: monospace;
    padding: 0.5rem;
    background-color: black;
    color: white;
`

function TaskLog({ log }) {
    return <div>
        <h4>Log</h4>
        <LogOutput>{log}</LogOutput>
    </div>
}

const mapStateToProps = (state, props) => ({
    log: state.tasks.logs[props.id],
})
export default connect(mapStateToProps)(TaskLog)