# Python Chat Application

A simple real-time chat application implemented in Python using sockets, allowing multiple clients to connect and communicate through a central server.

## Features

- Multi-client support
- Real-time messaging
- Non-blocking socket communication
- Client-side logging
- Windows keyboard input support
- Clean disconnection handling

## Prerequisites

- Python 3.x
- Windows OS (for client application due to msvcrt usage)

## Project Structure

```
chat-application/
│
├── chatclient.py        # Client-side implementation
├── app/
│   ├── chatserver.py    # Server implementation
│   └── chat/
│       └── routes.py    # Server routing logic
└── client.log          # Client-side logging file
```

## Installation

1. Clone the repository or download the source code
2. Ensure Python 3.x is installed on your system
3. No additional dependencies are required as the application uses Python's standard library

## Usage

### Starting the Server

1. Open a terminal window
2. Navigate to the project directory
3. Run the server with the following command:

```bash
python app/chatserver.py <IP_ADDRESS> <PORT>
```

Example:
```bash
python app/chatserver.py 127.0.0.1 5000
```

### Starting a Client

1. Open a new terminal window
2. Navigate to the project directory
3. Run the client with the following command:

```bash
python chatclient.py <SERVER_IP> <PORT>
```

Example:
```bash
python chatclient.py 127.0.0.1 5000
```

## Features Explanation

### Server
- Supports up to 100 concurrent connections
- Broadcasts messages to all connected clients except the sender
- Handles client disconnections gracefully
- Includes timeout mechanism to prevent blocking
- Automatic cleanup of disconnected clients

### Client
- Non-blocking input/output operations
- Real-time message reception
- Logging functionality (messages logged to client.log)
- Clean exit handling (Ctrl+C)
- User-friendly input interface

## Logging

The client application logs all activity to `client.log`. The log file contains:
- Warning messages
- Debug information about sent/received messages
- User inputs
- Connection events

## Error Handling

The application includes comprehensive error handling for:
- Connection failures
- Client disconnections
- Invalid inputs
- System interrupts
- Socket timeouts

## Limitations

- Client application is Windows-specific due to the use of `msvcrt`
- No message persistence (messages are not stored)
- No user authentication
- No private messaging support
- Messages are sent as plain text (no encryption)
