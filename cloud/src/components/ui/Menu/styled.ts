import styled from 'styled-components'
import { Link } from 'react-router-dom'

export const Menu = styled.div`
  display: flex;
  flex-direction: column;
  width: 4rem;
  background: ${p => p.theme.colors.background.secondary};
`

export const MenuItem = styled(Link)`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;  

  &:focus,
  &:visited,
  &:active {
    color: ${p => p.theme.colors.menu.primary};
  }
      
  &:hover {
    color: ${p => p.theme.colors.menu.hover};
  }
`

export const Logo = styled.div`
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
`