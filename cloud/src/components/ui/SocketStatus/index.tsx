import React from 'react'
import { useSelector } from 'react-redux'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { RootState } from '../../../store'
import { Status } from './styled'
import { SocketStatus } from '../../../store/socket/types'
import { SOCKET_CONNECTED } from '../../../store/socket/reducer'


const statusIcon = (socketStatus: SocketStatus) =>
  socketStatus === SOCKET_CONNECTED ?
    <FontAwesomeIcon icon="check" /> :
    <FontAwesomeIcon icon="spinner" spin />

const statusText = (socketStatus: SocketStatus) =>
  socketStatus === SOCKET_CONNECTED ?
    'Connected' :
    'Connecting'

const SocketStatusLabel: React.FC = ({ children }) => {
  const status = useSelector((state: RootState) => state.socket.status)
 
  return <Status status={status}>
    {statusText(status)}
    {statusIcon(status)}
  </Status>
}

  export default SocketStatusLabel
