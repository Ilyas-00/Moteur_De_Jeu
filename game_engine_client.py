import grpc
import game_engine_pb2
import game_engine_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = game_engine_pb2_grpc.GameEngineStub(channel)


response = stub.StartGame(game_engine_pb2.StartGameRequest(max_players=4, max_turns=10))
print("Game Started:", response)


response = stub.PlayerAction(game_engine_pb2.PlayerActionRequest(player_id="player1", action="move_right"))
print("Player Action:", response)


response = stub.GetGameState(game_engine_pb2.GameStateRequest())
print("Game State:", response)
