import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Bubble, FlexBox } from '../../ui'

export const TaskHeader = styled.div`
    font-size: 1.5rem;
    margin-bottom: 1rem;
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
    margin-bottom: 1rem;
    padding: 1rem 1.5rem;
`

export const TaskCreatedAt = styled.span`
    color: ${p => p.theme.colors.text.secondary};
    font-size: 0.7em;
    flex: 1;
    text-align: right;
`

export const TaskTitle = styled.div`
    display: flex;
    align-items: center;
`

export const TaskTitleWrapper = styled(FlexBox)`
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    flex: 1;
`

export const TaskActions = styled(FlexBox)`

`
