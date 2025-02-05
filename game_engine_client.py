import grpc
import game_engine_pb2
import game_engine_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = game_engine_pb2_grpc.GameEngineStub(channel)

# Démarrer le jeu avec un nombre max de joueurs et de tours
response = stub.StartGame(game_engine_pb2.StartGameRequest(max_players=4, max_turns=5))
print("Game Started:", response)

# Inscription des joueurs
players = ["Alice", "Bob", "Charlie", "Dave"]
for player in players:
    response = stub.RegisterPlayer(game_engine_pb2.RegisterPlayerRequest(player_id=player))
    print(f"Player {player} registered:", response)

# Assigner les rôles
response = stub.AssignRoles(game_engine_pb2.AssignRolesRequest())
print("Roles assigned:", response.roles)

# Envoyer une action de joueur
response = stub.PlayerAction(game_engine_pb2.PlayerActionRequest(player_id="Alice", action="vote Bob"))
print("Player Action:", response)

# Récupérer l'état du jeu
response = stub.GetGameState(game_engine_pb2.GameStateRequest())
print("Game State:", response)

# Réinitialiser le jeu
response = stub.ResetGame(game_engine_pb2.ResetGameRequest())
print("Game Reset:", response)
