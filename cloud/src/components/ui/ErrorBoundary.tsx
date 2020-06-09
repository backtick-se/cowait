import React, { ErrorInfo } from 'react'
import styled from 'styled-components'
import { ErrorBubble } from '.'

const ErrorContainer = styled.div`
    padding: 2em;
`
type State = {
    hasError: boolean,
    error: Error | null
}

type Props = {}

class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props)
        this.state = { 
            hasError: false,
            error: null,
        }
    }

    static getDerivedStateFromError(error: Error) {
        return { 
            hasError: true,
            error,
        }
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    }

    render() {
        const { hasError, error } = this.state
        if (hasError) {
            return <ErrorContainer>
                <ErrorBubble>
                    <h4>Error</h4>
                    <pre>
                        {error!.toString()}
                    </pre>
                </ErrorBubble>
            </ErrorContainer>
        }

        return this.props.children
    }
}

export default ErrorBoundary