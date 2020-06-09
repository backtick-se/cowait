import styled from 'styled-components'
import { Link } from 'react-router-dom'


export const BreadcrumbWrapper = styled.div`
  display: flex;
  align-items: center;
  svg {
    font-size: 0.7rem;
  }
`

export const BreadcrumbLink = styled(Link)`
  padding-right: 0.5rem;
  padding-left: 0.5rem;
  
  &:first-child {
    padding-left: 0;
  }
`