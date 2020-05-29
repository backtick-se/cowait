
import React, { useEffect, useRef } from 'react'
import { useSelector } from 'react-redux'
import { ContentBlock } from '../ui'
import { LogOutput, LogContainer } from './styled/Log'
import { RootState } from '../../store'

type Props = {
    id: string,
    maxHeight?: number
}

export const TaskLog: React.FC<Props> = ({ id, maxHeight }) => {
    const logRef = useRef<HTMLInputElement>(null)
    const log = useSelector((state: RootState) => state.tasks.logs[id])

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

    return <ContentBlock>
        <h4>Output Log</h4>
        <LogContainer ref={logRef} maxHeight={maxHeight}>
            <LogOutput>{log}</LogOutput>
        </LogContainer>
    </ContentBlock>
}

export default TaskLog