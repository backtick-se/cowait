import styled from 'styled-components'
import { darken, desaturate } from 'polished'


export const StyledButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  background: ${p => p.theme.colors.button.background};
  color: ${p => p.theme.colors.button.color};;
  padding: 0.25em 0.5em;
  border: none;
  border-radius: 0.3em;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 500;

  &:active, &:focus, &:visited {
    outline: none;
  }

  &:hover {
    background: ${p => darken(0.1, p.theme.colors.button.background)};
  }

  > svg {
    margin-right: 0.5em;
  }

  &:disabled {
    cursor: not-allowed;
    background: ${p => desaturate(1, p.theme.colors.button.background)};
  }
`
