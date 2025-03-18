# Moteur De Jeu - Jeu de Loups-Garous et Villageois

## Fonctionnalités

- Carte 8x8
- Deux types de joueurs : Villageois et Loups-Garous
- Possibilité de se déplacer de 1 ou 2 cases dans les 4 directions (haut, bas, gauche, droite)
- Système de tours de jeu
- Persistance des données avec SQLite

## Prérequis

- Python 3.6+
- gRPC et protobuf
- SQLite

## Installation

1. Cloner le dépôt :
```
git clone https://github.com/Ilyas-00/Moteur_De_Jeu.git
cd Moteur_De_Jeu
```

2. Installer les dépendances :
```
pip install grpcio grpcio-tools protobuf
```

3. Générer les fichiers gRPC à partir du fichier proto :
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. game.proto
```

## Utilisation

### Démarrer le serveur

```
python game_server.py
```

Le serveur démarrera et écoutera sur le port 50051.

### Utiliser le client

```
python game_client.py
```

Dans le client, vous pouvez utiliser les commandes suivantes :
- `create_game [taille_carte] [max_joueurs] [max_tours]` : Créer un nouveau jeu
- `create_player [nom] [type]` : Créer un nouveau joueur (type 0=Villageois, 1=Loup-garou)
- `join_game [game_id]` : Rejoindre un jeu existant
- `start` : Démarrer le jeu
- `status` : Afficher l'état actuel du jeu
- `move [distance] [direction]` : Déplacer votre joueur (distance 1-2, direction up/down/left/right)
- `end_turn` : Terminer votre tour
- `reset` : Réinitialiser le jeu
- `exit` ou `quit` : Quitter le client

## Exemple de flux de jeu

1. Créer un jeu : `create_game`
2. Créer un joueur : `create_player Joueur1 0`
3. Rejoindre le jeu : `join_game 1`
4. Démarrer le jeu : `start`
5. Se déplacer : `move 2 up`
6. Terminer le tour : `end_turn`

## Développement

Pour étendre ce jeu, vous pouvez modifier le fichier `game.proto` pour ajouter de nouvelles fonctionnalités, puis régénérer les fichiers gRPC.

## Licence

Ce projet est distribué sous licence MIT.
