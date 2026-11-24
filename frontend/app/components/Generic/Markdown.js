import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Table } from 'react-bootstrap'

// One place that decides how markdown content looks on the whole site.
// Plain elements (h1-h6, p, lists, links) are styled by Bootstrap + styles/_typography.scss.
// Elements that need a Bootstrap class are mapped to Bootstrap components here.
// Extra styling: styles/_markdown.scss (.markdown-content).
const components = {
  table: ({ node, ...props }) => <Table striped hover responsive size='sm' {...props} />,
  img: ({ node, ...props }) => <img className='img-fluid' {...props} />,
  blockquote: ({ node, ...props }) => <blockquote className='blockquote' {...props} />
}

const Markdown = ({ children, className = '' }) => (
  <div className={`markdown-content ${className}`.trim()}>
    <ReactMarkdown components={components}>{children || ''}</ReactMarkdown>
  </div>
)

export default Markdown
