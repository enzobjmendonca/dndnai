from game import Game
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Replace with your actual API key
API_KEY = ''

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
game_map = {}

class PlayerAction(BaseModel):
    game_id: str
    player_name: str
    action: str

class NewPlayer(BaseModel):
    game_id: str
    player_name: str


class Player(BaseModel):
    game_id: str
    player_name: str
    player_state: dict

@app.post("/add_player/")
def add_player(new_player: NewPlayer):
    #player = PlayerAgent(new_player.player_name)
    #game.add_player(player)
    return {"message": f"Player {new_player.player_name} added successfully."}

@app.post("/player_action/")
def player_action(action: PlayerAction):
    try:
        if action.game_id not in game_map:
            game_map[action.game_id] = Game(action.game_id)
        response = game_map[action.game_id].update_game(action.action)
        return {"dm_response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/game_history/")
def get_game_history(game_id: str):
    if game_id not in game_map:
        game_map[game_id] = Game(game_id)
    return {"history": game_map[game_id].get_game_history()}

@app.get("/players_state/")
def get_players_state(game_id: str):
    if game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    return {"players_state": game_map[game_id].get_players_state()}

@app.get("/npcs_state/")
def get_npcs_state(game_id: str):
    if game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    return {"npcs_state": game_map[game_id].get_npcs_state()}

@app.get("/locations_state/")
def get_locations_state(game_id: str):
    if game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    return {"locations_state": game_map[game_id].get_locations_state()}

@app.get("/player_state/{player_name}")
def get_state_for_player(player_name: str, game_id: str):
    if game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    return game_map[game_id].get_state_for_player(player_name)

@app.post("/update_player/")
def update_player(player: Player):
    if player.game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    game_map[player.game_id].update_player(player.player_name, player.player_state)
    return {"message": "Player updated successfully"}

@app.get("/game_checksum/")
def get_game_checksum(game_id: str):
    if game_id not in game_map:
        raise HTTPException(status_code=400, detail="Game not found")
    return {"game_checksum": game_map[game_id].get_game_checksum()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)