import { useState } from 'react'

function ConnectionPanel({ connectionStatus, sessionInfo, onConnect, onDisconnect, onHeartbeat }) {
  const [serverUrl, setServerUrl] = useState('http://localhost:8000/')
  const [vehicleId, setVehicleId] = useState('test-vehicle-001')
  const [userId, setUserId] = useState('test-user-001')

  const handleConnect = () => {
    onConnect(serverUrl, vehicleId, userId)
  }

  const handleHeartbeat = () => {
    if (onHeartbeat) {
      onHeartbeat()
    }
  }

  const getStatusLabel = () => {
    switch (connectionStatus) {
      case 'connected': return 'Connected'
      case 'connecting': return 'Connecting...'
      default: return 'Disconnected'
    }
  }

  return (
    <div className="panel">
      <h2 className="panel-title">
        <span className={`status-badge ${connectionStatus}`}>
          <span className="status-dot"></span>
          {getStatusLabel()}
        </span>
      </h2>

      <div className="form-group">
        <label htmlFor="serverUrl">Server URL</label>
        <input
          id="serverUrl"
          type="text"
          value={serverUrl}
          onChange={(e) => setServerUrl(e.target.value)}
          placeholder="http://localhost:8000"
          disabled={connectionStatus === 'connected'}
        />
      </div>

      <div className="form-group">
        <label htmlFor="vehicleId">Vehicle ID</label>
        <input
          id="vehicleId"
          type="text"
          value={vehicleId}
          onChange={(e) => setVehicleId(e.target.value)}
          placeholder="vehicle-001"
          disabled={connectionStatus === 'connected'}
        />
      </div>

      <div className="form-group">
        <label htmlFor="userId">User ID</label>
        <input
          id="userId"
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="user-001"
          disabled={connectionStatus === 'connected'}
        />
      </div>

      {connectionStatus === 'connected' ? (
        <button className="btn btn-danger" onClick={onDisconnect}>
          Disconnect
        </button>
      ) : (
        <button
          className="btn btn-primary"
          onClick={handleConnect}
          disabled={connectionStatus === 'connecting'}
        >
          {connectionStatus === 'connecting' ? 'Connecting...' : 'Connect'}
        </button>
      )}

      {sessionInfo && (
        <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#94a3b8' }}>
          <div><strong>Session ID:</strong> {sessionInfo.session_id}</div>
          <div><strong>User ID:</strong> {sessionInfo.user_id}</div>
        </div>
      )}

      {connectionStatus === 'connected' && (
        <button
          className="btn btn-secondary"
          onClick={handleHeartbeat}
          style={{ marginTop: '1rem', width: '100%' }}
        >
          Send Heartbeat
        </button>
      )}
    </div>
  )
}

export default ConnectionPanel
