import styled from 'styled-components'


export const LoadingContainer = styled.div`
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

export const LoadingIcon = styled.div`
    width: 100%;
    text-align: center;
    color: ${p => p.theme.colors.text.primary}

    i {
        font-size: 5rem;
    }

    label {
        display: block;
        margin-top: 1rem;
    }
`
