import grpc
import time
import random
from concurrent import futures
import game_engine_pb2
import game_engine_pb2_grpc

ROLES = ["loup-garou", "villageois", "voyante", "chasseur"]

class GameEngineService(game_engine_pb2_grpc.GameEngineServicer):
    def __init__(self):
        self.max_turns = 0
        self.max_players = 0
        self.state = {
            "status": "waiting",
            "current_turn": 0,
            "player_positions": {},
            "players": [],
            "roles": {}
        }

    def RegisterPlayer(self, request, context):
        if len(self.state["players"]) >= self.max_players:
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            context.set_details("Nombre maximal de joueurs atteint")
            return game_engine_pb2.GameState(**self.state)
        
        if request.player_id in self.state["players"]:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Le joueur est déjà inscrit")
            return game_engine_pb2.GameState(**self.state)

        self.state["players"].append(request.player_id)
        return game_engine_pb2.GameState(**self.state)

    def AssignRoles(self, request, context):
        if len(self.state["players"]) < 4:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Pas assez de joueurs pour commencer")
            return game_engine_pb2.GameState(**self.state)

        shuffled_roles = random.sample(ROLES * (len(self.state["players"]) // len(ROLES) + 1), len(self.state["players"]))
        self.state["roles"] = dict(zip(self.state["players"], shuffled_roles[:len(self.state["players"])]))

        return game_engine_pb2.GameState(**self.state)

    def StartGame(self, request, context):
        if len(self.state["players"]) < 4:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Pas assez de joueurs pour commencer")
            return game_engine_pb2.GameState(**self.state)

        self.state["status"] = "running"
        self.state["current_turn"] = 1
        self.max_turns = request.max_turns
        self.max_players = request.max_players
        return game_engine_pb2.GameState(**self.state)

    def PlayerAction(self, request, context):
        if request.player_id not in self.state["players"]:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Joueur inconnu")
            return game_engine_pb2.GameState(**self.state)

        self.state["player_positions"][request.player_id] = request.action
        
        if self.state["current_turn"] >= self.max_turns:
            self.state["status"] = "finished"
        else:
            self.state["current_turn"] += 1
        
        return game_engine_pb2.GameState(**self.state)

    def GetGameState(self, request, context):
        return game_engine_pb2.GameState(**self.state)
    
    def ResetGame(self, request, context):
        self.state = {
            "status": "waiting",
            "current_turn": 0,
            "player_positions": {},
            "players": [],
            "roles": {}
        }
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
