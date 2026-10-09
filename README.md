# Remote Desktop using TCP/IP

A lightweight Python proof-of-concept for remote screen sharing and input control over a local network. This project captures the server machine's screen and sends it to a target client via UDP, while receiving mouse and keyboard commands from the client through raw socket packets.

> Note: This repository currently contains the server-side implementation. It is intended for learning, experimentation, and local-network testing rather than production use.

## Overview

This application demonstrates:

- screen capture using `mss`
- JPEG compression of screenshots
- UDP streaming of the captured frames
- remote mouse movement and keyboard input via `pynput`
- raw packet interception for command delivery

The server runs on the machine being controlled, while the client (not included in this repository) would need to receive the stream and send input commands back to the server.

## Project structure

```text
Remote-desktop-using-TCP-IP-main/
├── README.md
├── Server_Side.py
├── Client_Side.py
└── (optional improvements: authentication, encryption, TCP control channel)
```

## Features

- Real-time screen capture
- Low-bandwidth JPEG streaming via UDP
- Mouse repositioning from remote commands
- Keyboard key presses and releases
- Local-network communication setup

## Requirements

- Python 3.8 or newer
- Windows/Linux/macOS support depending on socket and input library compatibility
- Administrative permissions may be required for raw socket access
- Network access between the controlling client and target server

## Dependencies

Install the required Python packages:

```bash
pip install mss pillow pynput
```

## Configuration

Before running the server, update the target client IP address in `Server_Side.py`:

```python
CLIENT_IP = '192.168.1.10'  # Change this to client's IP
```

Set this to the actual IP address of the machine receiving the screen stream.

## How it works

1. The server captures the current screen using `mss`.
2. Each captured frame is converted to JPEG and compressed.
3. The JPEG data is sent to the configured client using UDP.
4. The server listens for raw incoming packets.
5. Commands prefixed with `M` or `K` are interpreted as:
   - `M` + X/Y coordinates => move mouse pointer
   - `K` + key => press and release a key

## Running the server

From the project directory:

```bash
python Server_Side.py
```

This will start both threads:

- one for screen capture and transmission
- one for listening for remote input packets

## Running the client

From the project directory:

```bash
python Client_Side.py
```

Before running the client, set the server IP address:

```python
SERVER_IP = "192.168.1.10"  # Change this to the server machine's IP
```

The client does the following:

- listens for the incoming UDP screen stream on port 9999
- renders it in a Tkinter window
- forwards mouse movement and keyboard input to the server
- uses the command packet format expected by the server: `M` + X/Y coordinates or `K` + key

> Note: The current server implementation is a proof-of-concept and uses raw socket packet interception on the server side. The client therefore uses a simple UDP control channel for compatibility and experimentation. If you want the server to accept command traffic over a standard socket, update the server to listen on the same command port instead of a raw packet socket.

## Important limitations

This is a basic demonstration project and has several limitations:

- It is not optimized for high performance or production environments.
- Raw socket usage is OS- and privilege-sensitive.
- UDP does not guarantee reliability or delivery ordering.
- The client implementation is not included in this repository.
- No authentication, encryption, or security controls are present.
- Using this over untrusted networks can expose the host machine to unauthorized control.

## Security notice

This project should only be used on trusted local networks or private lab environments. Because it allows remote mouse and keyboard input, it can be abused if exposed to the outside world. Do not deploy it in production without:

- authentication
- encrypted communication
- access restrictions
- robust input validation
- a proper client/server protocol

## License

This project does not currently include a license file. If you plan to share or reuse it publicly, consider adding an appropriate open-source license.

## Notes

This code is intended as a educational sample for understanding low-level networked desktop control. For a more secure and maintainable implementation, consider upgrading to a controlled protocol with:

- TCP for reliable command exchange
- authentication and session tokens
- user consent prompts
- encrypted transport (TLS/SSH/VPN)
- client/server separation with a real protocol
