"""
Simple ECS (Entity-Component-System) Game Server
Uses ESPER library to manage a moving circle
Reads player inputs from client_request.json
Writes game state to session_state.json
"""

import esper
import json
import time
import os

# ============================================
# COMPONENTS (Data containers)
# ============================================

class Position:
    """Stores the x, y coordinates of an entity"""
    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y

class Velocity:
    """Stores movement speed"""
    def __init__(self, speed=5):
        self.speed = speed

class Appearance:
    """Stores visual properties"""
    def __init__(self, color="blue", radius=30):
        self.color = color
        self.radius = radius

# ============================================
# PROCESSORS (Logic systems)
# ============================================

class MovementProcessor(esper.Processor):
    """Handles movement based on input"""
    
    def __init__(self):
        super().__init__()
        self.current_input = None
    
    def process(self, **kwargs):
        # Process all entities that have both Position and Velocity components
        for ent, (pos, vel) in esper.get_components(Position, Velocity):
            if self.current_input:
                # Move based on WASD input
                if self.current_input == 'w':
                    pos.y -= vel.speed  # Move up (y decreases)
                elif self.current_input == 's':
                    pos.y += vel.speed  # Move down (y increases)
                elif self.current_input == 'a':
                    pos.x -= vel.speed  # Move left
                elif self.current_input == 'd':
                    pos.x += vel.speed  # Move right
                
                # Keep the circle on screen (800x600)
                pos.x = max(50, min(750, pos.x))
                pos.y = max(50, min(550, pos.y))

# ============================================
# MAIN GAME LOOP
# ============================================

def main():
    print("=== ECS Game Server Starting ===")
    
    # Create and add the movement processor
    movement_processor = MovementProcessor()
    esper.add_processor(movement_processor)
    
    # Create the player entity with components
    player = esper.create_entity()
    esper.add_component(player, Position(x=400, y=300))
    esper.add_component(player, Velocity(speed=10))
    esper.add_component(player, Appearance(color="dodgerblue", radius=30))
    
    print(f"Created player entity (ID: {player})")
    print("Game loop running... Press Ctrl+C to stop")
    
    # Initialize JSON files if they don't exist
    if not os.path.exists('client_request.json'):
        with open('client_request.json', 'w') as f:
            json.dump({"key": None}, f)
    
    # Main game loop
    frame_count = 0
    try:
        while True:
            frame_count += 1
            
            # 1. READ: Get input from client_request.json
            try:
                with open('client_request.json', 'r') as file:
                    client_data = json.load(file)
                    movement_processor.current_input = client_data.get('key')
            except (FileNotFoundError, json.JSONDecodeError):
                movement_processor.current_input = None
            
            # 2. PROCESS: Run all processors (handles movement logic)
            esper.process()
            
            # 3. WRITE: Export game state to session_state.json
            # Get the player's current components
            pos = esper.component_for_entity(player, Position)
            appear = esper.component_for_entity(player, Appearance)
            
            game_state = {
                "player": {
                    "x": pos.x,
                    "y": pos.y,
                    "color": appear.color,
                    "radius": appear.radius
                },
                "frame": frame_count
            }
            
            with open('session_state.json', 'w') as file:
                json.dump(game_state, file, indent=2)
            
            # Print status every 60 frames (roughly every second)
            if frame_count % 60 == 0:
                print(f"Frame {frame_count}: Player at ({pos.x:.1f}, {pos.y:.1f})")
            
            # Run at approximately 60 FPS
            time.sleep(1/60)
    
    except KeyboardInterrupt:
        print("\n=== Game Server Stopped ===")

if __name__ == "__main__":
    main()
