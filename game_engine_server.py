import grpc
import time
from concurrent import futures
import game_engine_pb2
import game_engine_pb2_grpc

class GameEngineService(game_engine_pb2_grpc.GameEngineServicer):
    def __init__(self):
        self.state = {
            "status": "waiting",
            "current_turn": 0,
            "player_positions": {}
        }

    def StartGame(self, request, context):
        self.state["status"] = "running"
        self.state["current_turn"] = 1
        return game_engine_pb2.GameState(**self.state)

    def PlayerAction(self, request, context):
        self.state["player_positions"][request.player_id] = request.action
        return game_engine_pb2.GameState(**self.state)

    def GetGameState(self, request, context):
        return game_engine_pb2.GameState(**self.state)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_engine_pb2_grpc.add_GameEngineServicer_to_server(GameEngineService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Game Engine gRPC Server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
