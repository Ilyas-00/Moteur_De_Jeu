import grpc
import game_pb2
import game_pb2_grpc
import cmd
import sys

class GameClient(cmd.Cmd):
    intro = "Bienvenue dans le jeu Loups-Garous et Villageois. Tapez help ou ? pour la liste des commandes."
    prompt = "(jeu) "
    
    def __init__(self):
        super().__init__()
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = game_pb2_grpc.GameServiceStub(self.channel)
        self.game_id = None
        self.player_id = None
    
    def do_create_game(self, arg):
        """Créer un nouveau jeu: create_game [taille_carte] [max_joueurs] [max_tours]"""
        args = arg.split()
        map_size = int(args[0]) if len(args) > 0 else 8
        max_players = int(args[1]) if len(args) > 1 else 10
        max_turns = int(args[2]) if len(args) > 2 else 30
        
        settings = game_pb2.GameSettings(
            map_size=map_size,
            max_players=max_players,
            max_turns=max_turns
        )
        
        try:
            response = self.stub.CreateGame(game_pb2.CreateGameRequest(settings=settings))
            self.game_id = response.game_id
            print(f"Jeu créé avec l'ID: {self.game_id}")
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_create_player(self, arg):
        """Créer un nouveau joueur: create_player [nom] [type: 0=Villageois, 1=Loup-garou]"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: create_player [nom] [type: 0=Villageois, 1=Loup-garou]")
            return
        
        name = args[0]
        player_type = int(args[1])
        
        try:
            response = self.stub.CreatePlayer(
                game_pb2.CreatePlayerRequest(name=name, type=player_type)
            )
            self.player_id = response.id
            print(f"Joueur créé avec l'ID: {self.player_id}")
            print(f"Type: {'Villageois' if player_type == 0 else 'Loup-garou'}")
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_join_game(self, arg):
        """Rejoindre un jeu: join_game [game_id]"""
        if not self.player_id:
            print("Vous devez d'abord créer un joueur.")
            return
        
        args = arg.split()
        game_id = int(args[0]) if len(args) > 0 and args[0] else self.game_id
        
        if not game_id:
            print("Veuillez spécifier l'ID du jeu ou créer un jeu d'abord.")
            return
        
        try:
            response = self.stub.JoinGame(
                game_pb2.JoinGameRequest(game_id=game_id, player_id=self.player_id)
            )
            self.game_id = game_id
            print(f"Vous avez rejoint le jeu {game_id}")
            self.print_game_state(response)
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_start(self, arg):
        """Démarrer le jeu: start"""
        if not self.game_id:
            print("Vous devez d'abord rejoindre un jeu.")
            return
        
        try:
            response = self.stub.StartGame(game_pb2.GameRequest(id=self.game_id))
            print("Le jeu a commencé!")
            self.print_game_state(response)
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_status(self, arg):
        """Afficher l'état du jeu: status"""
        if not self.game_id:
            print("Vous devez d'abord rejoindre un jeu.")
            return
        
        try:
            response = self.stub.GetGameState(game_pb2.GameRequest(id=self.game_id))
            self.print_game_state(response)
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_move(self, arg):
        """Déplacer votre joueur: move [distance: 1-2] [direction: up/down/left/right]"""
        if not self.game_id or not self.player_id:
            print("Vous devez d'abord rejoindre un jeu.")
            return
        
        args = arg.split()
        if len(args) < 2:
            print("Usage: move [distance: 1-2] [direction: up/down/left/right]")
            return
        
        distance = int(args[0])
        direction = args[1].lower()
        
        if distance not in [1, 2]:
            print("La distance doit être 1 ou 2.")
            return
        
        if direction not in ["up", "down", "left", "right"]:
            print("Direction invalide. Utilisez: up, down, left, right")
            return
        
        try:
            response = self.stub.MovePlayer(
                game_pb2.MoveRequest(
                    player_id=self.player_id,
                    distance=distance,
                    direction=direction
                )
            )
            print(f"Déplacement de {distance} case(s) vers {direction}")
            self.print_game_state(response)
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_end_turn(self, arg):
        """Terminer votre tour: end_turn"""
        if not self.game_id:
            print("Vous devez d'abord rejoindre un jeu.")
            return
        
        try:
            response = self.stub.EndTurn(game_pb2.GameRequest(id=self.game_id))
            print("Tour terminé")
            self.print_game_state(response)
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_reset(self, arg):
        """Réinitialiser le jeu: reset"""
        if not self.game_id:
            print("Vous devez d'abord rejoindre un jeu.")
            return
        
        try:
            self.stub.ResetGame(game_pb2.GameRequest(id=self.game_id))
            print("Jeu réinitialisé")
            self.do_status("")
        except grpc.RpcError as e:
            print(f"Erreur: {e.details()}")
    
    def do_exit(self, arg):
        """Quitter le client: exit"""
        print("Au revoir!")
        self.channel.close()
        return True
    
    def do_quit(self, arg):
        """Quitter le client: quit"""
        return self.do_exit(arg)
    
    def print_game_state(self, state):
        print(f"\nÉtat du jeu #{state.id}: {state.state}")
        print(f"Tour actuel: {state.current_turn}")
        print(f"Taille de la carte: {state.map_size}x{state.map_size}")
        print(f"Joueur actuel: {state.current_player_id}")
        
        # Créer une représentation visuelle de la carte
        grid = [[' . ' for _ in range(state.map_size)] for _ in range(state.map_size)]
        
        # Placer les joueurs sur la carte
        for player in state.players:
            symbol = 'V' if player.type == 0 else 'L'
            
            # Ajouter une indication visuelle pour le joueur actuel
            if player.id == self.player_id:
                symbol = '*' + symbol + '*'
            else:
                symbol = ' ' + symbol + ' '
            
            x, y = player.position.x, player.position.y
            if 0 <= x < state.map_size and 0 <= y < state.map_size:
                grid[y][x] = symbol
        
        # Afficher la carte
        print("\nCarte:")
        for row in grid:
            print('|' + '|'.join(row) + '|')
        
        # Afficher la liste des joueurs
        print("\nJoueurs:")
        for player in state.players:
            player_type = "Villageois" if player.type == 0 else "Loup-garou"
            status = "Vivant" if player.is_alive else "Mort"
            position = f"({player.position.x}, {player.position.y})"
            
            # Indiquer le joueur actuel
            current = "(Vous)" if player.id == self.player_id else ""
            
            print(f"  {player.id}: {player.name} - {player_type} - {status} - {position} {current}")
        
        print("")

def run():
    client = GameClient()
    try:
        client.cmdloop()
    except KeyboardInterrupt:
        print("\nAu revoir!")
    except Exception as e:
        print(f"Erreur: {str(e)}")
    finally:
        try:
            client.channel.close()
        except:
            pass

if __name__ == "__main__":
    run()