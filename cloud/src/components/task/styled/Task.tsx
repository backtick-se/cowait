import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Bubble, FlexBox } from '../../ui'

export const TaskHeader = styled.div`
    padding-bottom: 1rem;
    border-bottom: 0.5px solid ${p => p.theme.colors.border};
    margin-bottom: 1.5rem;
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
`

export const TaskWrapper = styled(Bubble)`
    margin-bottom: 2rem;
    padding: 1rem 1.5rem;
`

export const ParentWrapper = styled(FlexBox)`
    padding-top: 0.5rem;
    align-items: center;

    > svg {
        margin-right: 0.5rem;
    }
`

export const TaskTitleContainer = styled.div`
    display: flex;
    align-items: center;
    font-size: 1.5rem;
`