import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import { Link } from '../ui'
import TaskStatus from './TaskStatus'

const LinkWrapper = styled.span`
    display: block;
    padding: 0.25em 0;

    ${Link} {
        margin-right: 0.5em;
        font-family: ${p => p.theme.fonts.monospace};
    }
`

function TaskLink({ task: { id, status } }) {
    return <LinkWrapper>
        <Link to={`/task/${id}`}>{id}</Link>
        <TaskStatus status={status} />
    </LinkWrapper>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(TaskLink)