import React from 'react'
import styled from 'styled-components'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useSelector } from  'react-redux'
import { RootState } from '../../store'
import { SOCKET_CONNECTED } from '../../store/socket/reducer'

const LoadingContainer = styled.div`
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    position: relative;
    z-index: 9999;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(2px);

    display: flex;
    flex-direction: row;
    align-items: center;
`

const LoadingIcon = styled.div`
    width: 100%;
    text-align: center;
    color: #fff;

    i {
        font-size: 5rem;
    }

    label {
        display: block;
        margin-top: 1rem;
    }
`

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