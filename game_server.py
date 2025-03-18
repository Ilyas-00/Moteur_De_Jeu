import grpc
import sqlite3
import random
import game_pb2
import game_pb2_grpc
from concurrent import futures

DATABASE = "game.db"

class GameService(game_pb2_grpc.GameServiceServicer):
    def __init__(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect(DATABASE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Création des tables nécessaires
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, state TEXT, map_size INTEGER, max_players INTEGER, max_turns INTEGER, current_turn INTEGER, current_player_id INTEGER)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, game_id INTEGER, name TEXT, type INTEGER, x INTEGER, y INTEGER, is_alive INTEGER)"
        )
        self.conn.commit()
    
    def CreateGame(self, request, context):
        # Création d'un nouveau jeu avec les paramètres spécifiés
        settings = request.settings
        self.cursor.execute(
            "INSERT INTO games (state, map_size, max_players, max_turns, current_turn, current_player_id) VALUES (?, ?, ?, ?, ?, ?)",
            ("waiting", settings.map_size, settings.max_players, settings.max_turns, 0, 0)
        )
        self.conn.commit()
        game_id = self.cursor.lastrowid
        return game_pb2.CreateGameResponse(game_id=game_id)
    
    def CreatePlayer(self, request, context):
        # Création d'un nouveau joueur
        name = request.name
        player_type = request.type
        
        # Insertion du joueur dans la base de données
        self.cursor.execute(
            "INSERT INTO players (name, type, x, y, is_alive) VALUES (?, ?, ?, ?, ?)",
            (name, player_type, 0, 0, 1)
        )
        self.conn.commit()
        player_id = self.cursor.lastrowid
        
        # Récupérer les infos du joueur
        player = game_pb2.Player(
            id=player_id,
            name=name,
            type=player_type,
            position=game_pb2.Position(x=0, y=0),
            is_alive=True
        )
        
        return player
    
    def JoinGame(self, request, context):
        # Faire rejoindre un joueur à un jeu
        game_id = request.game_id
        player_id = request.player_id
        
        # Vérifier que le jeu existe
        self.cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        game = self.cursor.fetchone()
        if not game:
            context.abort(grpc.StatusCode.NOT_FOUND, "Jeu non trouvé")
        
        # Attribuer une position aléatoire au joueur sur la carte
        map_size = game[2]  # map_size est à l'index 2 dans la table games
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        
        # Mettre à jour le joueur avec l'ID du jeu et sa position
        self.cursor.execute(
            "UPDATE players SET game_id = ?, x = ?, y = ? WHERE id = ?",
            (game_id, x, y, player_id)
        )
        self.conn.commit()
        
        # Retourner l'état du jeu
        return self.GetGameState(game_pb2.GameRequest(id=game_id), context)
    
    def GetGameState(self, request, context):
        game_id = request.id
        
        # Récupérer les informations du jeu
        self.cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        game = self.cursor.fetchone()
        if not game:
            context.abort(grpc.StatusCode.NOT_FOUND, "Jeu non trouvé")
        
        # Récupérer les joueurs du jeu
        self.cursor.execute("SELECT * FROM players WHERE game_id = ?", (game_id,))
        player_rows = self.cursor.fetchall()
        
        # Construire la liste des joueurs
        players = []
        for p in player_rows:
            player = game_pb2.Player(
                id=p[0],
                name=p[2],
                type=p[3],
                position=game_pb2.Position(x=p[4], y=p[5]),
                is_alive=(p[6] == 1)
            )
            players.append(player)
        
        # Construire l'état du jeu
        game_state = game_pb2.GameState(
            id=game[0],
            state=game[1],
            players=players,
            current_turn=game[5],
            map_size=game[2],
            current_player_id=game[6]
        )
        
        return game_state
    
    def MovePlayer(self, request, context):
        player_id = request.player_id
        distance = request.distance
        direction = request.direction
        
        # Vérifier que la distance est valide (1 ou 2)
        if distance not in [1, 2]:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "La distance doit être 1 ou 2")
        
        # Récupérer les informations du joueur
        self.cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
        player = self.cursor.fetchone()
        if not player:
            context.abort(grpc.StatusCode.NOT_FOUND, "Joueur non trouvé")
        
        game_id = player[1]
        current_x = player[4]
        current_y = player[5]
        
        # Récupérer la taille de la carte
        self.cursor.execute("SELECT map_size FROM games WHERE id = ?", (game_id,))
        map_size = self.cursor.fetchone()[0]
        
        # Calculer la nouvelle position
        new_x, new_y = current_x, current_y
        if direction == "up":
            new_y = max(0, current_y - distance)
        elif direction == "down":
            new_y = min(map_size - 1, current_y + distance)
        elif direction == "left":
            new_x = max(0, current_x - distance)
        elif direction == "right":
            new_x = min(map_size - 1, current_x + distance)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Direction invalide")
        
        # Mettre à jour la position du joueur
        self.cursor.execute(
            "UPDATE players SET x = ?, y = ? WHERE id = ?",
            (new_x, new_y, player_id)
        )
        self.conn.commit()
        
        # Retourner l'état du jeu
        return self.GetGameState(game_pb2.GameRequest(id=game_id), context)
    
    def StartGame(self, request, context):
        game_id = request.id
        
        # Mettre à jour l'état du jeu
        self.cursor.execute(
            "UPDATE games SET state = ?, current_turn = ? WHERE id = ?",
            ("running", 1, game_id)
        )
        self.conn.commit()
        
        # Sélectionner un joueur au hasard pour commencer
        self.cursor.execute("SELECT id FROM players WHERE game_id = ?", (game_id,))
        players = self.cursor.fetchall()
        if players:
            first_player = random.choice(players)[0]
            self.cursor.execute(
                "UPDATE games SET current_player_id = ? WHERE id = ?",
                (first_player, game_id)
            )
            self.conn.commit()
        
        # Retourner l'état du jeu
        return self.GetGameState(game_pb2.GameRequest(id=game_id), context)
    
    def EndTurn(self, request, context):
        game_id = request.id
        
        # Récupérer l'état actuel du jeu
        self.cursor.execute(
            "SELECT current_turn, max_turns, current_player_id FROM games WHERE id = ?",
            (game_id,)
        )
        game_info = self.cursor.fetchone()
        current_turn, max_turns, current_player_id = game_info
        
        # Récupérer tous les joueurs du jeu
        self.cursor.execute(
            "SELECT id FROM players WHERE game_id = ? ORDER BY id",
            (game_id,)
        )
        players = [p[0] for p in self.cursor.fetchall()]
        
        if not players:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Pas de joueurs dans le jeu")
        
        # Trouver le prochain joueur
        try:
            current_index = players.index(current_player_id)
            next_index = (current_index + 1) % len(players)
            next_player_id = players[next_index]
        except ValueError:
            next_player_id = players[0]
        
        # Si on revient au premier joueur, incrémenter le tour
        if next_index == 0:
            current_turn += 1
        
        # Vérifier si le jeu est terminé
        game_state = "running"
        if current_turn > max_turns:
            game_state = "ended"
        
        # Mettre à jour l'état du jeu
        self.cursor.execute(
            "UPDATE games SET state = ?, current_turn = ?, current_player_id = ? WHERE id = ?",
            (game_state, current_turn, next_player_id, game_id)
        )
        self.conn.commit()
        
        # Retourner l'état du jeu
        return self.GetGameState(game_pb2.GameRequest(id=game_id), context)
    
    def ResetGame(self, request, context):
        game_id = request.id
        
        # Réinitialiser le jeu
        self.cursor.execute(
            "UPDATE games SET state = ?, current_turn = ? WHERE id = ?",
            ("waiting", 0, game_id)
        )
        
        # Replacer aléatoirement les joueurs
        self.cursor.execute("SELECT map_size FROM games WHERE id = ?", (game_id,))
        map_size = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT id FROM players WHERE game_id = ?", (game_id,))
        for player_id in [p[0] for p in self.cursor.fetchall()]:
            x = random.randint(0, map_size - 1)
            y = random.randint(0, map_size - 1)
            self.cursor.execute(
                "UPDATE players SET x = ?, y = ?, is_alive = ? WHERE id = ?",
                (x, y, 1, player_id)
            )
        
        self.conn.commit()
        return game_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServiceServicer_to_server(GameService(), server)
    server.add_insecure_port("[::]:50051")
    print("Moteur de jeu gRPC en écoute sur le port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()