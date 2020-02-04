import React from 'react'
import styled from 'styled-components'
import { connect } from 'react-redux'
import socket from '../store/socket'

const LoadingContainer = styled.div`
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    position: absolute;
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


function SocketOverlay({ children, status }) {
    if (status === socket.actions.SOCKET_CONNECTED) {
        return children
    }

    return <React.Fragment>
        {children}
        <LoadingContainer>
            <LoadingIcon>
                <i className="fa fas fa-asterisk fa-spin" />
                <label>connecting</label>
            </LoadingIcon>
        </LoadingContainer>
    </React.Fragment> 
}

const mapStateToProps = state => ({
    ...state.socket,
})
export default connect(mapStateToProps)(SocketOverlay)