import { useState } from 'react'

const SAMPLE_QUERIES = [
  '帮我导航到最近的加油站',
  '播放周杰伦的晴天',
  '今天天气怎么样',
  '帮我打开空调',
  '附近有什么餐厅',
]

function QueryPanel({ onSendQuery, isConnected, isProcessing }) {
  const [query, setQuery] = useState('')
  const [streamingEnabled, setStreamingEnabled] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && isConnected) {
      onSendQuery(query.trim(), { stream: streamingEnabled })
      setQuery('')
    }
  }

  const handleSampleClick = (sampleQuery) => {
    if (isConnected) {
      onSendQuery(sampleQuery, { stream: streamingEnabled })
    }
  }

  return (
    <div className="panel" style={{ marginTop: '1.5rem' }}>
      <h2 className="panel-title">Send Query</h2>

      <form onSubmit={handleSubmit}>
        <textarea
          className="query-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your voice query (e.g., 帮我导航到最近的加油站)"
          disabled={!isConnected || isProcessing}
        />
        
        <div style={{ marginTop: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.875rem' }}>
            <input
              type="checkbox"
              checked={streamingEnabled}
              onChange={(e) => setStreamingEnabled(e.target.checked)}
              disabled={!isConnected || isProcessing}
              style={{ width: '16px', height: '16px' }}
            />
            Enable Streaming Response
          </label>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          style={{ marginTop: '0.75rem' }}
          disabled={!isConnected || !query.trim() || isProcessing}
        >
          {isProcessing ? 'Processing...' : 'Send Query'}
        </button>
      </form>

      <div style={{ marginTop: '1rem' }}>
        <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
          Sample Queries:
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {SAMPLE_QUERIES.map((sample, index) => (
            <button
              key={index}
              onClick={() => handleSampleClick(sample)}
              disabled={!isConnected || isProcessing}
              style={{
                padding: '0.375rem 0.75rem',
                fontSize: '0.75rem',
                background: '#334155',
                border: '1px solid #475569',
                borderRadius: '0.375rem',
                color: '#f1f5f9',
                cursor: isConnected ? 'pointer' : 'not-allowed',
                opacity: isConnected ? 1 : 0.5,
              }}
            >
              {sample}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default QueryPanel
