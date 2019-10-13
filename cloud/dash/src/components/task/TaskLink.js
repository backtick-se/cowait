import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import TaskStatus from './TaskStatus'

const StyledLink = styled(Link)`
    display: block;
    padding: 0.5rem 0;
    text-decoration: none;
`

function TaskLink({ task: { id, status } }) {
    return <StyledLink to={`/task/${id}`}>{id} <TaskStatus status={status} /></StyledLink>
}

const mapStateToProps = (state, props) => ({
    task: state.tasks.items[props.id],
})
export default connect(mapStateToProps)(TaskLink)