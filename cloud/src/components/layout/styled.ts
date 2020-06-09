import styled from 'styled-components'


export const HorizontalWrapper = styled.div`
  display: flex;
  height: 100vh;
`

export const ContentWrapper = styled.div`
  overflow-y: scroll;

  -ms-overflow-style: none;
  &::-webkit-scrollbar {
    display: none;
  }
`

export const VerticalWrapper = styled.div`
  flex: 200px;
  display: flex;
  flex-direction: column;
`
