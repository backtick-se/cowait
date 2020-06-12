import styled from 'styled-components'
import { hex2Rgba } from '../../../utils'
import { SocketStatus } from '../../../store/socket/types'
import { SOCKET_CONNECTED } from '../../../store/socket/reducer'
import { Theme } from '../../../theme/types'

const statusColor = ({ status, theme }: { status?: SocketStatus, theme: Theme}) =>
  status === SOCKET_CONNECTED ?
    theme.colors.status['done'] :
    theme.colors.status['stop']

export const Status = styled.div<{ status?: SocketStatus | null }>`
  padding: 0.25rem 0.5rem;
  background: red;
  border-radius: 0.3rem;
  color: ${statusColor};
  border-radius: ${p => p.theme.borderRadius};
  background: ${p => hex2Rgba(statusColor(p), 0.2)};

  svg {
    margin-left: 0.5rem;
  }

  margin-left: 0.5rem;
`