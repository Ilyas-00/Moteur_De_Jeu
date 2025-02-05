# Game Engine with gRPC 

Ce projet implémente un moteur de jeu  en utilisant gRPC.

## Fonctionnalités
- Inscription et gestion des joueurs
- Attribution des rôles aléatoires
- Alternance des phases Nuit/Jour
- Actions des joueurs et gestion des votes
- Récupération de l'état du jeu

## Installation
```bash
git clone https://github.com/yourusername/game-engine-grpc.git
cd game-engine-grpc
pip install grpcio grpcio-tools
python game_engine_server.py
```

## API gRPC
- **StartGame** : Démarre une partie
- **RegisterPlayer** : Ajoute un joueur
- **AssignRoles** : Assigne les rôles
- **PlayerAction** : Envoie une action
- **GetGameState** : Récupère l'état
- **ResetGame** : Réinitialise le jeu

