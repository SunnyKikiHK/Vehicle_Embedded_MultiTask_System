import { useState } from 'react'

function ResponsePanel({ responses, streamingContent, onClear }) {
  const [activeTab, setActiveTab] = useState('response')  // 'response' | 'raw'
  const [expandedRaw, setExpandedRaw] = useState({})  // Track expanded raw responses
  const hasStreamingContent = Object.keys(streamingContent).length > 0

  const toggleRawExpand = (index) => {
    setExpandedRaw(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 className="panel-title" style={{ marginBottom: 0 }}>
          Responses
          {responses.length > 0 && (
            <span style={{
              marginLeft: '0.5rem',
              background: '#334155',
              padding: '0.125rem 0.5rem',
              borderRadius: '9999px',
              fontSize: '0.75rem'
            }}>
              {responses.length}
            </span>
          )}
        </h2>
        {(responses.length > 0 || hasStreamingContent) && (
          <button
            onClick={onClear}
            style={{
              padding: '0.25rem 0.75rem',
              fontSize: '0.75rem',
              background: 'transparent',
              border: '1px solid #475569',
              borderRadius: '0.375rem',
              color: '#94a3b8',
              cursor: 'pointer',
            }}
          >
            Clear
          </button>
        )}
      </div>

      {/* Tabs for Response and Raw Response */}
      <div style={{
        display: 'flex',
        gap: '0.5rem',
        marginBottom: '1rem',
        borderBottom: '1px solid #334155',
        paddingBottom: '0.5rem'
      }}>
        <button
          onClick={() => setActiveTab('response')}
          style={{
            padding: '0.5rem 1rem',
            fontSize: '0.875rem',
            background: activeTab === 'response' ? '#3b82f6' : 'transparent',
            border: 'none',
            borderRadius: '0.375rem',
            color: activeTab === 'response' ? 'white' : '#94a3b8',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          Actual Response
        </button>
        <button
          onClick={() => setActiveTab('raw')}
          style={{
            padding: '0.5rem 1rem',
            fontSize: '0.875rem',
            background: activeTab === 'raw' ? '#3b82f6' : 'transparent',
            border: 'none',
            borderRadius: '0.375rem',
            color: activeTab === 'raw' ? 'white' : '#94a3b8',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          Full Response Object
        </button>
      </div>

      <div className="response-container">
        {/* Streaming content section - shown for both tabs */}
        {hasStreamingContent && (
          <div style={{ marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>Streaming Responses:</h3>
            {Object.entries(streamingContent).map(([query, content]) => (
              <div key={query} className="response-item" style={{ borderColor: '#3b82f6' }}>
                <div className="response-header">
                  <span className="response-query">Q: {query}</span>
                  <span className="response-status" style={{ color: '#3b82f6' }}>streaming...</span>
                </div>
                <div className="response-content" style={{ color: '#60a5fa' }}>
                  {content}
                  <span style={{ animation: 'blink 1s infinite' }}>|</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab: Actual Response */}
        {activeTab === 'response' && (
          <>
            {responses.length === 0 && !hasStreamingContent ? (
              <p className="response-placeholder">
                No responses yet. Connect to the server and send a query.
              </p>
            ) : (
              responses.map((response, index) => {
                const actualResponse = extractActualResponse(response)
                return (
                  <div key={response.timestamp || index} className="response-item">
                    <div className="response-header">
                      <span className="response-query">
                        Q: {response.query || response.data?.query || 'N/A'}
                      </span>
                      <span className={`response-status ${response.status === 'success' ? 'success' : 'error'}`}>
                        {response.status || response.data?.status || 'unknown'}
                      </span>
                    </div>
                    <div className="response-content" style={{ whiteSpace: 'pre-wrap', fontSize: '1rem', lineHeight: '1.5' }}>
                      {actualResponse || 'No response content'}
                    </div>
                  </div>
                )
              })
            )}
          </>
        )}

        {/* Tab: Full Response Object */}
        {activeTab === 'raw' && (
          <>
            {responses.length === 0 && !hasStreamingContent ? (
              <p className="response-placeholder">
                No responses yet. Connect to the server and send a query.
              </p>
            ) : (
              responses.map((response, index) => (
                <div key={response.timestamp || index} className="response-item" style={{ borderColor: '#8b5cf6' }}>
                  <div className="response-header">
                    <span className="response-query">
                      Q: {response.query || response.data?.query || 'N/A'}
                    </span>
                    <span className={`response-status ${response.status === 'success' ? 'success' : 'error'}`}>
                      {response.status || response.data?.status || 'unknown'}
                    </span>
                  </div>

                  <button
                    onClick={() => toggleRawExpand(index)}
                    style={{
                      marginTop: '0.5rem',
                      padding: '0.25rem 0.75rem',
                      fontSize: '0.75rem',
                      background: '#8b5cf6',
                      border: 'none',
                      borderRadius: '0.25rem',
                      color: 'white',
                      cursor: 'pointer',
                    }}
                  >
                    {expandedRaw[index] ? 'Collapse' : 'Expand'} Raw Object
                  </button>

                  {expandedRaw[index] && (
                    <div className="response-content" style={{ marginTop: '0.5rem' }}>
                      <pre style={{
                        background: '#1e293b',
                        padding: '0.75rem',
                        borderRadius: '0.375rem',
                        overflow: 'auto',
                        maxHeight: '400px',
                        fontSize: '0.75rem',
                        lineHeight: '1.4'
                      }}>
                        {JSON.stringify(response, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              ))
            )}
          </>
        )}
      </div>
    </div>
  )
}

function extractActualResponse(response) {
  // Try to extract the actual text response from various possible locations
  const result = response.result || response.data?.result

  if (!result) return null

  // Case 1: result is a simple string
  if (typeof result === 'string') return result

  // Case 2: result.response is the actual text
  if (result.response && typeof result.response === 'string') return result.response

  // Case 3: result is an object but no clear response field
  return null
}

export default ResponsePanel
