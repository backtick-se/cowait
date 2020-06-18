import styled from 'styled-components'


export const Navbar = styled.nav`
  background: ${p => p.theme.colors.background.secondary};
  color: ${p => p.theme.colors.text.primary};
  padding: 1rem;
  display: flex;
  font-size: 0.8rem;
  justify-content: space-between;
  align-items: center;
  z-index: 100;

  a {
    font-family: ${p => p.theme.fonts.header};

    &:focus,
    &:visited,
    &:active {
      color: inherit;
    }
  
    &:hover {
      color: ${p => p.theme.colors.menu.hover};
    }
  }
`
