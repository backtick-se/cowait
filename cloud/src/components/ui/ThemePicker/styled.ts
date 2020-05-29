import styled from 'styled-components'


export const ThemeIcon = styled.a<{ active: boolean, color: string }>`
  display: block;
  background: ${p => p.color};
  width: 1rem;
  height: 1rem;
  border-radius: 1rem;
  margin: 0 0.2em;
  border: ${p => `1px solid ${p.active ? p.theme.colors.text.primary : p.color}`};

  &:last-child {
    margin-right: 0;
  }

  &:hover {
    border-color: ${p => p.theme.colors.link.primary};
  }
`
