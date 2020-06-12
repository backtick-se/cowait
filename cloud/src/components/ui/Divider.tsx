import styled from 'styled-components'


const Divider = styled.hr`
  border: none;
  border-bottom: 0.5px solid ${p => p.theme.colors.border};
  height: 0.5px;
  margin: 1rem 0;
`

export default Divider;