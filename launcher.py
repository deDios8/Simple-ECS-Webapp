"""
Unified Launcher - Runs both the game server and web server together
This script uses THREADING to run both servers at the same time
"""

import threading
import time

# Import the server modules
import game_server
import web_server

def run_game_server():
    """Run the game logic server in a separate thread"""
    print("🎮 Starting game server thread...")
    game_server.main()

def run_web_server():
    """Run the HTTP web server in a separate thread"""
    print("🌐 Starting web server thread...")
    web_server.run_server(port=8000)

def main():
    """Launch both servers using threads"""
    print("=" * 50)
    print("  ECS GAME - UNIFIED LAUNCHER")
    print("=" * 50)
    print()
    print("This will start:")
    print("  1. Game Server  - Handles ECS logic")
    print("  2. Web Server   - Serves HTML/CSS/JS files")
    print()
    print("Once started, open your browser to:")
    print("  👉 http://localhost:8000")
    print()
    print("Press Ctrl+C to stop both servers")
    print("=" * 50)
    print()
    
    # Give the user a moment to read the message
    time.sleep(3)
    
    # Create threads for each server
    # daemon=True means threads will stop when main program stops
    game_thread = threading.Thread(target=run_game_server, daemon=True, name="GameServer")
    web_thread = threading.Thread(target=run_web_server, daemon=True, name="WebServer")
    
    # Start both threads
    game_thread.start()
    time.sleep(0.5)  # Small delay so game server starts first
    web_thread.start()
    
    print()
    print("✅ Both servers are running!")
    print()
    
    try:
        # Keep the main thread alive
        # The servers will run in the background threads
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        print("=" * 50)
        print("🛑 Shutting down servers...")
        print("=" * 50)
        # Threads will automatically stop because daemon=True

if __name__ == "__main__":
    main()
