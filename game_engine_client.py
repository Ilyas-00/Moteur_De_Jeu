import grpc
import game_engine_pb2
import game_engine_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = game_engine_pb2_grpc.GameEngineStub(channel)

# Démarrer le jeu
response = stub.StartGame(game_engine_pb2.StartGameRequest(max_players=4, max_turns=5))
print("Game Started:", response)

# Envoyer une action de joueur
response = stub.PlayerAction(game_engine_pb2.PlayerActionRequest(player_id="player1", action="move_right"))
print("Player Action:", response)

# Récupérer l'état du jeu
response = stub.GetGameState(game_engine_pb2.GameStateRequest())
print("Game State:", response)

# Réinitialiser le jeu
response = stub.ResetGame(game_engine_pb2.ResetGameRequest())
print("Game Reset:", response)
