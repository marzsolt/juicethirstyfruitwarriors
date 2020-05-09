"# juicethirstyfruitwarriors"

# Short description
My team created a real-time platformer arena game (with multiplayer and AI players options). There are different player-types, with different attacking abilities (one can become a deadly ball for a short time; another can throw himself, causing damage at impact). Who survives the others, wins.

# Architecture sketch
There are two main components: server and client side. Only one server should run to which all clients connect. There is also a utils and a tests (unittests) modul. 

## Client side
Responsible for all the GUI and input-detection. Minimal game-logic, only to send relevant messages to the server (the different player-types send different kind of data).
### main
Main tasks:
- Startup client side (NetworkClient, Screen)
- Main "event-loop", base "clock signal"
### Network communication
Main tasks:
- Connect to server
- Provide interface to send/receive messages
### Screen
Main tasks:
- Root of all graphics :)
- Handle menu and screens of the game in general (drawing, switching)
### Player
Main tasks:
- If client's player: report inputs in every frame -> character-specified
- Draw player (with animations)
- Store copy of graphics-related (character-specific) data (like cooldown of attack, hp...). 
- Singleton PlayerManager class is an extra layer to handle players

## Server side
Responsible for all game-logic. Manages the whole game, updates players based on their inputs.
### main
Main tasks:
- Startup server side
- Base "clock signal"
### Network communication
Main tasks:
- Accept clients
- Provide interface to send/receive messages
### Game
Main tasks:
- Control gameflow
- Manage game-related classes (Terrain, Players)
### Player 
Main tasks:
- Store player-related data (health, cooldowns...)
- Define player-logic like how to attack, move...
- Process client side's requests
- its AI-derivations: AI...
### PlayerAI 
Main tasks:
- Define general and character-specific AI behaviour
