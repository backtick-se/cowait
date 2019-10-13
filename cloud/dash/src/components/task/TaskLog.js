
import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'

const TaskLogBox = styled.div`
    padding: 0.5rem 0;
    h4 {
        font-size: 1.1rem;
        font-weight: bold;
    }
    pre {
        font-family: 'Nanum Gothic Coding';
        padding: 0.5rem;
        background-color: black;
        color: white;
    }
`

function TaskLog({ log }) {
    return <TaskLogBox>
        <h4>Log</h4>
        <pre>{log}</pre>
    </TaskLogBox>
}

const mapStateToProps = (state, props) => ({
    log: state.tasks.logs[props.id],
})
export default connect(mapStateToProps)(TaskLog)