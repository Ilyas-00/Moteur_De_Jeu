# Game Engine with gRPC

This project implements a simple game engine using gRPC. The game engine is designed to manage game states, process player actions, and allow players to interact with the game via gRPC requests.

## Project Overview

The Game Engine provides the following features:
- Start a new game with a specified number of players and turns.
- Allow players to perform actions (e.g., move, attack, etc.).
- Retrieve the current game state (status, current turn, player positions).

## Technologies Used

- **gRPC**: For communication between the server and the client.
- **Protobuf**: To define the service methods and message formats.
- **Python**: The programming language used for both the server and the client.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/game-engine-grpc.git
cd game-engine-grpc
