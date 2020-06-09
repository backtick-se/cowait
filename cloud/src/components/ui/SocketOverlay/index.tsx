import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useSelector } from  'react-redux'
import { RootState } from '../../../store'
import { SOCKET_CONNECTED } from '../../../store/socket/reducer'
import { LoadingContainer, LoadingIcon } from './styled'


const SocketOverlay: React.FC = ({ children }) =>  {
    const status = useSelector((state: RootState) => state.socket.status)

    if (status === SOCKET_CONNECTED) {
        return <>{children}</>
    }

    return <React.Fragment>
        <>{children}</>
        <LoadingContainer>
            <LoadingIcon>
                <FontAwesomeIcon icon="spinner" spin />
                <label>connecting</label>
            </LoadingIcon>
        </LoadingContainer>
    </React.Fragment> 
}

export default SocketOverlay
