import React from 'react'
import styled from 'styled-components'
import { ErrorBubble } from './components/ui'

const ErrorContainer = styled.div`
    padding: 2em;
`

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props)
        this.state = { 
            hasError: false,
            error: null,
        }
    }

    static getDerivedStateFromError(error) {
        return { 
            hasError: true,
            error,
        }
    }

    componentDidCatch(error, errorInfo) {
    }

    render() {
        const { hasError, error } = this.state
        if (hasError) {
            return <ErrorContainer>
                <ErrorBubble>
                    <h4>Error</h4>
                    <pre>
                        {error.toString()}
                    </pre>
                </ErrorBubble>
            </ErrorContainer>
        }

        return this.props.children
    }
}

export default ErrorBoundary