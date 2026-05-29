# Vehicle Task System - Frontend Test Client

A React-based test client for the Vehicle Voice Assistant backend, built with Socket.IO for real-time communication.

## Features

- **Connection Management** - Connect/disconnect to the backend server with custom credentials
- **Query Testing** - Send voice queries and view responses in real-time
- **Sample Queries** - Quick-start buttons for common vehicle commands
- **Activity Logs** - Monitor all Socket.IO events and message flow
- **Dark Theme UI** - Modern, easy-on-the-eyes interface

## Prerequisites

- Node.js 18+ installed
- Backend server running at `http://localhost:8000`

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at `http://localhost:3000`.

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # React entry point
│   ├── index.css            # Global styles
│   └── components/
│       ├── ConnectionPanel.jsx   # Server connection form
│       ├── QueryPanel.jsx        # Query input & samples
│       ├── ResponsePanel.jsx     # Response display
│       └── LogsPanel.jsx         # Activity logs
├── index.html
├── package.json
└── vite.config.js
```

## Usage

### 1. Connect to Server

Fill in the connection details:
- **Server URL**: `http://localhost:8000` (default)
- **Vehicle ID**: Any identifier for the vehicle
- **User ID**: Any identifier for the user

Click **Connect** to establish the Socket.IO connection.

### 2. Send Queries

Once connected, enter a voice query in the text area or use one of the sample query buttons:

| Sample Query | Description |
|--------------|-------------|
| 帮我导航到最近的加油站 | Navigate to nearest gas station |
| 播放周杰伦的晴天 | Play a specific song |
| 今天天气怎么样 | Check weather |
| 帮我打开空调 | Control air conditioning |
| 附近有什么餐厅 | Search for nearby restaurants |

### 3. View Responses

Responses are displayed in the Responses panel with:
- Query text
- Status indicator (success/error)
- Full JSON response from the backend

### 4. Monitor Logs

The Activity Logs panel shows all Socket.IO events in real-time for debugging.

## Socket.IO Events

### Events Emitted

| Event | Payload | Description |
|-------|---------|--------------|
| `voice_query` | `{ query: string, metadata?: object }` | Send a voice command |

### Events Received

| Event | Payload | Description |
|-------|---------|--------------|
| `connected` | `{ status, session_id, user_id }` | Connection established |
| `processing` | `{ status }` | Query is being processed |
| `response` | `{ status, query, result }` | Query result returned |
| `error` | `{ status, message }` | Error occurred |

## Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

## Configuration

The frontend connects to `http://localhost:8000` by default. To change this, modify the `serverUrl` field in the Connection Panel or update the default value in `src/components/ConnectionPanel.jsx`.

## API Reference

The frontend communicates with the backend's Socket.IO namespace at `/vehicle`. See the backend's `run.py` for the complete server-side implementation.
