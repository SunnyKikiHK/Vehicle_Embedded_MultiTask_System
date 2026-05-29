function LogsPanel({ logs, onClear }) {
  return (
    <div className="panel logs-section">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 className="panel-title" style={{ marginBottom: 0 }}>
          Activity Logs
          {logs.length > 0 && (
            <span style={{
              marginLeft: '0.5rem',
              background: '#334155',
              padding: '0.125rem 0.5rem',
              borderRadius: '9999px',
              fontSize: '0.75rem'
            }}>
              {logs.length}
            </span>
          )}
        </h2>
        {logs.length > 0 && (
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

      <div className="logs-container">
        {logs.length === 0 ? (
          <p style={{ color: '#64748b', fontStyle: 'italic', textAlign: 'center' }}>
            No logs yet
          </p>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`log-entry log-${log.type}`}>
              <span className="timestamp">[{log.timestamp}]</span>
              <span>{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default LogsPanel
