import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Bubble } from '../ui'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'
import TaskChildren from './TaskChildren'

const TaskHeader = styled.div`
    padding: 1rem;

    h2 {
        padding-bottom: 0.5rem;
    }
`

const TaskHeaderLink = styled(Link)`
    color: #222;
    text-decoration: none;
    cursor: pointer
    margin-right: 0.5em;

    &:hover {
        text-decoration: none;
    }
`

const TaskImage = styled.label`
    display: block;
    color: #777;
    font-family: ${p => p.theme.fonts.monospace};
`

const TaskWrapper = styled(Bubble)`
    margin-bottom: 2rem;
    padding 0.5rem;
`

const ParentWrapper = styled.div`
    padding: 0.5rem 0;
    font-size: 1.1rem;
`

function Task({ id, status, image, parent, result, error, children, inputs }) {
    return <TaskWrapper>
        <TaskHeader>
            <h2>
                <TaskHeaderLink to={`/task/${id}`}>{id}</TaskHeaderLink> 
                <TaskStatus status={status} />
            </h2>
            <TaskImage>{image}</TaskImage>
            {parent && <ParentWrapper>
                <TaskLink id={parent}/>
            </ParentWrapper>}
        </TaskHeader>

        <TaskError error={error} />
        <TaskInputs inputs={inputs} />
        <TaskChildren children={children} />
        <TaskLog id={id} />
        <TaskResult result={result} />
    </TaskWrapper>
}

export default Task