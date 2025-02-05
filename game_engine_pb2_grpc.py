# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import game_engine_pb2 as game__engine__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in game_engine_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GameEngineStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartGame = channel.unary_unary(
                '/game.GameEngine/StartGame',
                request_serializer=game__engine__pb2.StartGameRequest.SerializeToString,
                response_deserializer=game__engine__pb2.GameState.FromString,
                _registered_method=True)
        self.PlayerAction = channel.unary_unary(
                '/game.GameEngine/PlayerAction',
                request_serializer=game__engine__pb2.PlayerActionRequest.SerializeToString,
                response_deserializer=game__engine__pb2.GameState.FromString,
                _registered_method=True)
        self.GetGameState = channel.unary_unary(
                '/game.GameEngine/GetGameState',
                request_serializer=game__engine__pb2.GameStateRequest.SerializeToString,
                response_deserializer=game__engine__pb2.GameState.FromString,
                _registered_method=True)
        self.ResetGame = channel.unary_unary(
                '/game.GameEngine/ResetGame',
                request_serializer=game__engine__pb2.ResetGameRequest.SerializeToString,
                response_deserializer=game__engine__pb2.GameState.FromString,
                _registered_method=True)


class GameEngineServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StartGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PlayerAction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGameState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResetGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GameEngineServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartGame': grpc.unary_unary_rpc_method_handler(
                    servicer.StartGame,
                    request_deserializer=game__engine__pb2.StartGameRequest.FromString,
                    response_serializer=game__engine__pb2.GameState.SerializeToString,
            ),
            'PlayerAction': grpc.unary_unary_rpc_method_handler(
                    servicer.PlayerAction,
                    request_deserializer=game__engine__pb2.PlayerActionRequest.FromString,
                    response_serializer=game__engine__pb2.GameState.SerializeToString,
            ),
            'GetGameState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGameState,
                    request_deserializer=game__engine__pb2.GameStateRequest.FromString,
                    response_serializer=game__engine__pb2.GameState.SerializeToString,
            ),
            'ResetGame': grpc.unary_unary_rpc_method_handler(
                    servicer.ResetGame,
                    request_deserializer=game__engine__pb2.ResetGameRequest.FromString,
                    response_serializer=game__engine__pb2.GameState.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'game.GameEngine', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('game.GameEngine', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class GameEngine(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StartGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/game.GameEngine/StartGame',
            game__engine__pb2.StartGameRequest.SerializeToString,
            game__engine__pb2.GameState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PlayerAction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/game.GameEngine/PlayerAction',
            game__engine__pb2.PlayerActionRequest.SerializeToString,
            game__engine__pb2.GameState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetGameState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/game.GameEngine/GetGameState',
            game__engine__pb2.GameStateRequest.SerializeToString,
            game__engine__pb2.GameState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ResetGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/game.GameEngine/ResetGame',
            game__engine__pb2.ResetGameRequest.SerializeToString,
            game__engine__pb2.GameState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
