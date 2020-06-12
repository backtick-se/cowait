import styled from 'styled-components'

type Props = {
  flexDirection?: string | null,
  alignItems?: string | null,
  justifyContent?: string | null
  background?: string | null
  flex?: string | null
}

export const FlexBox = styled.div<Props>`
  display: flex;
  flex-direction: ${p => p.flexDirection || 'row'};
  align-items: ${p => p.alignItems || ''};
  justify-content: ${p => p.justifyContent || ''};
  background: ${p => p.background || ''};
  flex: ${p => p.flex || ''};
`;