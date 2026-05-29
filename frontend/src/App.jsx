import { useState, useEffect, useCallback, useRef } from 'react'
import { io } from 'socket.io-client'
import ConnectionPanel from './components/ConnectionPanel'
import QueryPanel from './components/QueryPanel'
import ResponsePanel from './components/ResponsePanel'
import LogsPanel from './components/LogsPanel'
import GpsSimulationPanel from './components/GpsSimulationPanel'

function App() {
  const [socket, setSocket] = useState(null)
  const [connectionStatus, setConnectionStatus] = useState('disconnected')
  const [sessionInfo, setSessionInfo] = useState(null)
  const [responses, setResponses] = useState([])
  const [logs, setLogs] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [streamingContent, setStreamingContent] = useState({})  // query -> accumulated content
  const socketRef = useRef(null)

  const addLog = useCallback((message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString()
    setLogs(prev => [...prev, { timestamp, message, type }])
  }, [])

  const connect = useCallback((serverUrl, vehicleId, userId) => {
    if (socketRef.current) {
      socketRef.current.disconnect()
    }

    addLog(`Connecting to ${serverUrl}...`, 'info')
    setConnectionStatus('connecting')

    // Note: path should NOT be specified here. Socket.IO will use default /socket.io/ path
    // The namespace /vehicle is handled by the server
    const newSocket = io(serverUrl, {
      auth: { vehicle_id: vehicleId, user_id: userId },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    })

    newSocket.on('connect', () => {
      addLog('Connected to server', 'success')
      setConnectionStatus('connected')
    })

    newSocket.on('disconnect', (reason) => {
      addLog(`Disconnected: ${reason}`, 'warning')
      setConnectionStatus('disconnected')
      setSessionInfo(null)
    })

    newSocket.on('connect_error', (error) => {
      addLog(`Connection error: ${error.message}`, 'error')
      setConnectionStatus('disconnected')
    })

    newSocket.on('connected', (data) => {
      addLog(`Session established: ${JSON.stringify(data)}`, 'success')
      setSessionInfo(data)
    })

    newSocket.on('processing', (data) => {
      addLog(`Processing: ${JSON.stringify(data)}`, 'warning')
      setIsProcessing(true)
    })

    newSocket.on('stream_response', (data) => {
      addLog(`Streaming chunk received: "${data.chunk}"`, 'info')
      // Accumulate streaming content by query
      setStreamingContent(prev => ({
        ...prev,
        [data.query]: (prev[data.query] || '') + data.chunk
      }))
    })

    newSocket.on('response', (data) => {
      addLog(`Response received`, 'success')
      setIsProcessing(false)
      // Clear streaming content for this query
      const query = data.query
      setStreamingContent(prev => {
        const newContent = { ...prev }
        delete newContent[query]
        return newContent
      })
      setResponses(prev => [{
        ...data,
        timestamp: new Date().toISOString()
      }, ...prev])
    })

    newSocket.on('error', (data) => {
      addLog(`Error: ${data.message}`, 'error')
      setIsProcessing(false)
      setResponses(prev => [{
        ...data,
        status: 'error',
        timestamp: new Date().toISOString()
      }, ...prev])
    })

    socketRef.current = newSocket
    setSocket(newSocket)
  }, [addLog])

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect()
      socketRef.current = null
      setSocket(null)
      setSessionInfo(null)
      setConnectionStatus('disconnected')
      addLog('Disconnected', 'info')
    }
  }, [addLog])

  const sendQuery = useCallback((query, metadata = {}) => {
    if (socketRef.current && connectionStatus === 'connected') {
      addLog(`Sending query: ${query.substring(0, 50)}...`, 'info')
      socketRef.current.emit('voice_query', { query, ...metadata })
    } else {
      addLog('Cannot send query: not connected', 'error')
    }
  }, [connectionStatus, addLog])

  const sendHeartbeat = useCallback(() => {
    if (socketRef.current && connectionStatus === 'connected') {
      addLog('Sending heartbeat...', 'info')
      socketRef.current.emit('heartbeat', {}, (response) => {
        if (response && response.status === 'ok') {
          addLog('Heartbeat acknowledged', 'success')
        } else {
          addLog(`Heartbeat failed: ${JSON.stringify(response)}`, 'warning')
        }
      })
    } else {
      addLog('Cannot send heartbeat: not connected', 'error')
    }
  }, [connectionStatus, addLog])

  const clearLogs = useCallback(() => {
    setLogs([])
  }, [])

  const clearResponses = useCallback(() => {
    setResponses([])
  }, [])

  useEffect(() => {
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect()
      }
    }
  }, [])

  return (
    <div className="app">
      <header className="header">
        <h1>Vehicle Task System - Client</h1>
        <p>Socket.IO client for testing the vehicle voice assistant backend</p>
      </header>

      <div className="main-grid">
        <div className="sidebar">
          <ConnectionPanel
            connectionStatus={connectionStatus}
            sessionInfo={sessionInfo}
            onConnect={connect}
            onDisconnect={disconnect}
            onHeartbeat={sendHeartbeat}
          />
          <GpsSimulationPanel
            socket={socket}
            connectionStatus={connectionStatus}
            sessionInfo={sessionInfo}
          />
          <QueryPanel
            onSendQuery={sendQuery}
            isConnected={connectionStatus === 'connected'}
            isProcessing={isProcessing}
          />
        </div>
        <div className="content">
          <ResponsePanel
            responses={responses}
            streamingContent={streamingContent}
            onClear={clearResponses}
          />
          <LogsPanel
            logs={logs}
            onClear={clearLogs}
          />
        </div>
      </div>
    </div>
  )
}

export default App
