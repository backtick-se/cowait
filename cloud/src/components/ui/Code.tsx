import React from 'react'
import styled from 'styled-components'
import RSH from 'react-syntax-highlighter'
import { atelierSulphurpoolDark } from 'react-syntax-highlighter/dist/esm/styles/hljs'

const SyntaxHighlighter = styled(RSH)`
    background: transparent !important;
`

type Props = {
    language: string
}

export const Code: React.FC<Props> = ({ children, language }) => {
    return <SyntaxHighlighter style={atelierSulphurpoolDark} language={language}>
        {children}
    </SyntaxHighlighter>
}