// ============================================
// SETUP
// ============================================

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let currentKey = null;
let gameState = null;

// ============================================
// INPUT HANDLING
// ============================================

// Listen for WASD key presses
document.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    
    // Only respond to WASD keys
    if (['w', 'a', 's', 'd'].includes(key)) {
        currentKey = key;
        document.getElementById('lastKey').textContent = key.toUpperCase();
        
        // Write the key press to client_request.json
        saveClientRequest(key);
        
        // Prevent default browser behavior (like scrolling)
        event.preventDefault();
    }
});

// Clear input when key is released
document.addEventListener('keyup', (event) => {
    const key = event.key.toLowerCase();
    if (['w', 'a', 's', 'd'].includes(key)) {
        currentKey = null;
        saveClientRequest(null);
    }
});

// ============================================
// JSON FILE COMMUNICATION
// ============================================

// Save key press to client_request.json
async function saveClientRequest(key) {
    try {
        const response = await fetch('client_request.json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ key: key })
        });
    } catch (error) {
        console.error('Error writing client_request.json:', error);
    }
}

// Read game state from session_state.json
async function loadGameState() {
    try {
        const response = await fetch('session_state.json?t=' + Date.now());
        if (response.ok) {
            gameState = await response.json();
            
            // Update status display
            if (gameState.player) {
                document.getElementById('position').textContent = 
                    `(${gameState.player.x.toFixed(0)}, ${gameState.player.y.toFixed(0)})`;
            }
            document.getElementById('frame').textContent = gameState.frame || 0;
        }
    } catch (error) {
        console.error('Error reading session_state.json:', error);
    }
}

// ============================================
// RENDERING
// ============================================

function render() {
    // Clear the canvas
    ctx.fillStyle = '#7f8c8d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw the player if we have game state
    if (gameState && gameState.player) {
        const player = gameState.player;
        
        // Draw the circle
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw a white outline
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.stroke();
    } else {
        // Show loading message
        ctx.fillStyle = 'white';
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Waiting for game server...', canvas.width / 2, canvas.height / 2);
    }
}

// ============================================
// GAME LOOP
// ============================================

// Update and render at 60 FPS
async function gameLoop() {
    await loadGameState();
    render();
    requestAnimationFrame(gameLoop);
}

// Start the game loop
console.log('Game client started!');
gameLoop();
