# Simple ECS Web App Demo

A beginner-friendly demonstration of **Entity-Component-System (ECS)** architecture using Python and HTML/JavaScript, communicating through JSON files.

## 🎯 What This Demonstrates

- **Python with ESPER library**: Entity-Component-System game logic
- **JSON for communication**: Data exchange between Python and JavaScript
- **Simple game loop**: Reading input, processing logic, updating state
- **HTML/JavaScript**: Rendering and user input

## 📁 Project Structure

```
Simple-ECS-Webapp/
├── launcher.py             # 🚀 START HERE - Runs both servers
├── game_server.py          # Python ECS game logic
├── web_server.py           # HTTP server for the HTML client
├── index.html              # HTML structure
├── styles.css              # Visual styling
├── app.js                  # JavaScript game client
├── session_state.json      # Game state (Python writes, HTML reads)
├── client_request.json     # Player input (HTML writes, Python reads)
└── README.md               # This file
```

## 🚀 Getting Started

### 1. Install Dependencies

First, install the ESPER library:

```bash
pip install esper
```

### 2. Run the Launcher (Easy Way!)

Start both servers with one command:

```bash
python launcher.py
```

You should see:
```
==================================================
  ECS GAME - UNIFIED LAUNCHER
==================================================
This will start:
  1. Game Server  - Handles ECS logic
  2. Web Server   - Serves HTML/CSS/JS files

Once started, open your browser to:
  👉 http://localhost:8000
```

### 3. Open Your Browser

Open your browser to: **http://localhost:8000**

### 4. Play!

Use **W, A, S, D** keys to move the blue circle around the screen.

## 🏗️ How It Works

### The ECS Pattern (game_server.py)

1. **Components**: Data containers (Position, Velocity, Appearance)
2. **Entities**: Objects made of components (the player circle)
3. **Processors**: Systems that operate on entities (MovementProcessor)

### The Game Loop

```
┌─────────────────┐      client_request.json      ┌──────────────────┐
│                 │ ◄──────────────────────────── │                  │
│  Python Server  │                                │  HTML/JS Client  │
│   (game_server) │                                │   (index.html)   │
│                 │ ────────────────────────────► │                  │
└─────────────────┘      session_state.json       └──────────────────┘
```

1. **HTML**: User presses WASD → writes to `client_request.json`
2. **Python**: Reads `client_request.json` → processes movement with ECS → writes to `session_state.json`
3. **HTML**: Reads `session_state.json` → draws circle at new position
4. **Repeat** at 60 FPS!

## 📚 Learning Points

### For Python Learners:
- How to use the ESPER library for ECS architecture
- Reading and writing JSON files
- Creating a game loop with timing
- Separating data (Components) from logic (Processors)

### For HTML/JavaScript Learners:
- Canvas drawing basics
- Keyboard event handling
- Reading/writing JSON with fetch API
- Game loop with requestAnimationFrame

### For Architecture Learners:
- Client-server separation
- File-based communication (JSON)
- Entity-Component-System pattern
- Game loop fundamentals

## 🎓 Exercises to Try

1. **Add a second entity**: Create another circle with a different color
2. **Add boundaries**: Make the circle bounce off walls
3. **Add speed control**: Use arrow keys to change movement speed
4. **Add a score**: Track how many times the player moves
5. **Multiple components**: Add a Score component and ScoreProcessor

## ⚠️ Note

This project uses JSON files for communication, which is simple but not ideal for real games (too slow). Real games would use:
- WebSockets for real-time communication
- Direct server-client protocols
- Shared memory or message queues

But for learning the ECS pattern and JSON basics, this approach is perfect! 🎉

## 🛑 Stopping the Servers

Press `Ctrl+C` in the terminal running `launcher.py` to stop both servers.

## 🔧 Advanced: Running Servers Separately

If you want to run the servers in separate terminals (for debugging):

**Terminal 1:**
```bash
python game_server.py
```

**Terminal 2:**
```bash
python web_server.py
```

## 💡 How Threading Works

The `launcher.py` uses Python's **threading** module to run both servers simultaneously:

```python
# Create two separate threads
game_thread = threading.Thread(target=run_game_server, daemon=True)
web_thread = threading.Thread(target=run_web_server, daemon=True)

# Start both threads - they run at the same time!
game_thread.start()
web_thread.start()
```

**Why threading works well here:**
- Both servers spend most of their time **waiting** (for input, for network requests)
- They don't compete for resources
- Easy to understand for beginners
- `daemon=True` means threads automatically stop when you press Ctrl+C
