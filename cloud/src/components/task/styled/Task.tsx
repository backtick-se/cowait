import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Bubble } from '../../ui'


export const TaskHeader = styled.div`
    padding: 1rem;

    h2 {
        padding-bottom: 0.5rem;
    }
`

export const TaskHeaderLink = styled(Link)`
    color: #222;
    text-decoration: none;
    cursor: pointer;
    margin-right: 0.5em;

    &:hover {
        text-decoration: none;
    }
`

export const TaskImage = styled.label`
    display: block;
    color: #777;
    font-family: ${p => p.theme.fonts.monospace};
`

export const TaskWrapper = styled(Bubble)`
    margin-bottom: 2rem;
    padding: 0.5rem;
`

export const ParentWrapper = styled.div`
    padding: 0.5rem 0;
    font-size: 1.1rem;
`