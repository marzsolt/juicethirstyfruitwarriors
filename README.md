"# juicethirstyfruitwarriors" 
# Short description
My team would like to create a real-time platformer arena game (with multiplayer and AI players options). We plan to create different player-types, with different attacking abilities (e.g. one could become a deadly ball for a short time; another could throw himself into a direction with force set by the mouse, causing damage at impact...). Who survives the others, wins.


# Architecture sketch
There are two main components: server and client side. Only one server should run to which all clients connect.

## Client side
Responsible for all the GUI, input-detection. Minimal game-logic, only to send relevant messages to the server.
### Client - Main
Main tasks:
- Startup and control client side (NetworkClient, Screen)
- Main "event-loop"
### NetworkClient
Main tasks:
- Connect to server
- Send/receive messages
- Singleton (but each client will have one!)
### Screen
Main tasks:
- Root of all graphics :)
- Switch from menu to game (maybe to gameover and others later) 
- Singleton(?)
### Player (and derivations: ApplePlayer, OrangePlayer...)
Main tasks:
- If client's player: report inputs in every frame (Client calls its report func) -> character-specified
- Draw player (maybe with animations)
- Store copy of graphics-related (character-specific) data (like cooldown of attack, life...). 

## Server side
Responsible for all game-logic. Manages the whole game, updates players based on their inputs.
### Server - Main
Main tasks:
- Startup and control server side (NetworkServer, Game)
### NetworkServer
Main tasks:
- Connect to clients
- Send/receive messages
- Singleton
### Game
Main tasks:
- Stores players (in a list)
- Control gameflow
- Manage other game-related classes
### Player (and derivations: ApplePlayer, OrangePlayer...)
Main tasks:
- Store player-related data (health, cooldowns...)
- Define player-logic like how to attack, move...
### World
Main tasks:
- Generate itself on call
- Store world-related data (ground level)
- Provide easy access to its data, like: goundLevelAtX(x) function
