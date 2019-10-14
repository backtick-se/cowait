import React from 'react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { githubGist } from 'react-syntax-highlighter/dist/esm/styles/hljs'

const style = {
    padding: 0,
}

export function Code({ children, language }) {
    return <SyntaxHighlighter style={githubGist} customStyle={style} language={language}>
        {children}
    </SyntaxHighlighter>
}

Code.defaultProps = {

}