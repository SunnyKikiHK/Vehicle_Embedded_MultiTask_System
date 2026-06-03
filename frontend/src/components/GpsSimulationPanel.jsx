import { useState, useCallback, useEffect, useRef } from 'react'

function GpsSimulationPanel({ socket, connectionStatus, ttlSeconds }) {
  const [isActive, setIsActive] = useState(false)
  const [latitude, setLatitude] = useState('23.078519')
  const [longitude, setLongitude] = useState('112.50055')
  const [statusMessage, setStatusMessage] = useState('')
  const [ttlRemaining, setTtlRemaining] = useState(null)
  const expiryTimestampRef = useRef(null)
  const intervalRef = useRef(null)

  useEffect(() => {
    if (isActive && expiryTimestampRef.current) {
      intervalRef.current = setInterval(() => {
        const remaining = Math.ceil((expiryTimestampRef.current - Date.now()) / 1000)
        if (remaining <= 0) {
          setTtlRemaining(0)
          clearInterval(intervalRef.current)
          intervalRef.current = null
          handleDeactivate()
        } else {
          setTtlRemaining(remaining)
        }
      }, 1000)

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
      }
    } else {
      setTtlRemaining(null)
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [isActive])

  const handleDeactivate = useCallback(() => {
    setIsActive(false)
    setTtlRemaining(null)
    expiryTimestampRef.current = null
    setStatusMessage('GPS inactive (session expired)')

    if (socket && connectionStatus === 'connected') {
      socket.emit('gps_update', {
        active: false
      })
    }
  }, [socket, connectionStatus])

  const handleSetActive = useCallback(() => {
    if (!latitude || !longitude) {
      setStatusMessage('Please enter both latitude and longitude')
      return
    }

    if (ttlSeconds == null) {
      setStatusMessage('GPS TTL not configured (server may not support expiry)')
    }

    const lat = parseFloat(latitude)
    const lng = parseFloat(longitude)

    if (isNaN(lat) || isNaN(lng)) {
      setStatusMessage('Invalid coordinates')
      return
    }

    if (lat < -90 || lat > 90) {
      setStatusMessage('Latitude must be between -90 and 90')
      return
    }

    if (lng < -180 || lng > 180) {
      setStatusMessage('Longitude must be between -180 and 180')
      return
    }

    expiryTimestampRef.current = Date.now() + ttlSeconds * 1000
    setIsActive(true)
    setTtlRemaining(ttlSeconds)
    setStatusMessage(`GPS active: ${lat.toFixed(6)}, ${lng.toFixed(6)}`)

    if (socket && connectionStatus === 'connected') {
      socket.emit('gps_update', {
        latitude: lat,
        longitude: lng,
        active: true
      })
    }
  }, [latitude, longitude, socket, connectionStatus, ttlSeconds])

  const handleSetInactive = useCallback(() => {
    setIsActive(false)
    setTtlRemaining(null)
    expiryTimestampRef.current = null
    setStatusMessage('GPS inactive')

    if (socket && connectionStatus === 'connected') {
      socket.emit('gps_update', {
        active: false
      })
    }
  }, [socket, connectionStatus])

  const handleClearCoordinates = useCallback(() => {
    setLatitude('')
    setLongitude('')
    setStatusMessage('')
    if (isActive) {
      handleSetInactive()
    }
    setIsActive(false)
    setTtlRemaining(null)
    expiryTimestampRef.current = null
  }, [isActive, handleSetInactive])

  const isConnected = connectionStatus === 'connected'

  return (
    <div className="panel gps-panel" style={{ marginTop: '1.5rem' }}>
      <h2 className="panel-title">GPS Simulation</h2>

      <p className="panel-hint">
        Simulate vehicle GPS by entering coordinates manually
      </p>

      <div className="form-group">
        <label htmlFor="latitude">Latitude</label>
        <input
          id="latitude"
          type="number"
          step="any"
          placeholder="e.g., 39.9042"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
          disabled={!isConnected}
        />
      </div>

      <div className="form-group">
        <label htmlFor="longitude">Longitude</label>
        <input
          id="longitude"
          type="number"
          step="any"
          placeholder="e.g., 116.4074"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
          disabled={!isConnected}
        />
      </div>

      <div className="button-row">
        <button
          onClick={handleSetActive}
          disabled={!isConnected || !latitude || !longitude}
          className="btn btn-primary"
        >
          Set GPS
        </button>
        <button
          onClick={handleSetInactive}
          disabled={!isConnected || !isActive}
          className="btn btn-secondary"
        >
          Clear
        </button>
        <button
          onClick={handleClearCoordinates}
          disabled={!isConnected}
          className="btn btn-outline"
        >
          Reset
        </button>
      </div>

      <div className="gps-status-container">
        <div className={`gps-status ${isActive ? 'active' : 'inactive'}`}>
          <span className="status-dot"></span>
          <span>GPS {isActive ? 'Active' : 'Inactive'}</span>
          {ttlRemaining !== null && ttlSeconds != null && (
            <span style={{ marginLeft: '0.5rem', opacity: 0.75 }}>
              ({ttlRemaining}s / {ttlSeconds}s)
            </span>
          )}
        </div>

        {statusMessage && (
          <div className={`status-message ${isActive ? 'success' : ''}`}>
            {statusMessage}
          </div>
        )}
      </div>
    </div>
  )
}

export default GpsSimulationPanel
