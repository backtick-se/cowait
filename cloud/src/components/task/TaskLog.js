
import React, { useEffect, useRef } from 'react'
import { useSelector } from 'react-redux'
import { Bubble } from '../ui'
import { LogOutput, LogContainer } from './styled/Log'


export function TaskLog({ id, maxHeight }) {
    const logRef = useRef(null)
    const log = useSelector(state => state.tasks.logs[id])

    // scroll to bottom of the log whenever it changes
    const scrollToBottom = () => {
        if (!logRef.current) {
            return
        }
        logRef.current.scrollTop = logRef.current.scrollHeight
    }

    useEffect(scrollToBottom, [log])

    // no output if log is empty
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

export default TaskLog