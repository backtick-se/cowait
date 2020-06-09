import React from 'react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { githubGist } from 'react-syntax-highlighter/dist/esm/styles/hljs'

const style = {
    padding: 0,
}

type Props = {
    language: string
}

export const Code: React.FC<Props> = ({ children, language }) => {
    return <SyntaxHighlighter style={githubGist} customStyle={style} language={language}>
        {children}
    </SyntaxHighlighter>
}