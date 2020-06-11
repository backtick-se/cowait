import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Bubble, FlexBox } from '../../ui'

export const TaskHeader = styled.div`
    padding-bottom: 1rem;
    border-bottom: 0.5px solid ${p => p.theme.colors.border};
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
`

export const TaskHeaderLink = styled(Link)`
    font-family: ${p => p.theme.fonts.header};
    font-weight: 500;
    margin-right: 0.5em;
    
    &:hover {
        text-decoration: underline;
    }
`

export const TaskImage = styled.label`
    display: block;
    color: ${p => p.theme.colors.text.secondary};
    font-family: ${p => p.theme.fonts.monospace};
    font-size: 0.7em;
`

export const TaskWrapper = styled(Bubble)`
    margin-bottom: 2rem;
    padding: 1rem 1.5rem;
`

export const ParentWrapper = styled(FlexBox)`
    padding-top: 0.5rem;
    align-items: center;
    font-size: 0.7em;

    > svg {
        font-size: 0.9em;
        margin-right: 0.5em;
    }
`

export const TaskCreatedAt = styled.span`
    color: ${p => p.theme.colors.text.secondary};
    font-size: 0.7em;
`

export const TaskTitle = styled.div`
    display: flex;
    align-items: center;
`

export const TaskTitleWrapper = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
`
