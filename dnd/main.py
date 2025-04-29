import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from game import Game
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/dnd_server_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get API key from environment
API_KEY = os.getenv('API_KEY', '')
if not API_KEY:
    logger.warning("API_KEY not found in environment variables")

app = FastAPI()

# Configure CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    try:
        logger.info(f"Adding new player: {new_player.player_name} to game: {new_player.game_id}")
        #player = PlayerAgent(new_player.player_name)
        #game.add_player(player)
        logger.info(f"Player {new_player.player_name} added successfully")
        return {"message": f"Player {new_player.player_name} added successfully."}
    except Exception as e:
        logger.error(f"Error adding player {new_player.player_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/player_action/")
def player_action(action: PlayerAction):
    try:
        logger.info(f"Processing action for player {action.player_name} in game {action.game_id}")
        if action.game_id not in game_map:
            logger.info(f"Creating new game instance for game_id: {action.game_id}")
            game_map[action.game_id] = Game(action.game_id)
        response = game_map[action.game_id].update_game(action.action)
        logger.info(f"Action processed successfully for player {action.player_name}")
        return {"dm_response": response}
    except Exception as e:
        logger.error(f"Error processing action for player {action.player_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/game_history/")
def get_game_history(game_id: str):
    try:
        logger.info(f"Retrieving game history for game_id: {game_id}")
        if game_id not in game_map:
            logger.info(f"Creating new game instance for game_id: {game_id}")
            game_map[game_id] = Game(game_id)
        history = game_map[game_id].get_game_history()
        logger.info(f"Successfully retrieved game history for game_id: {game_id}")
        return {"history": history}
    except Exception as e:
        logger.error(f"Error retrieving game history for game_id {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/players_state/")
def get_players_state(game_id: str):
    try:
        logger.info(f"Retrieving players state for game_id: {game_id}")
        if game_id not in game_map:
            logger.error(f"Game not found: {game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        state = game_map[game_id].get_players_state()
        logger.info(f"Successfully retrieved players state for game_id: {game_id}")
        return {"players_state": state}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving players state for game_id {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/npcs_state/")
def get_npcs_state(game_id: str):
    try:
        logger.info(f"Retrieving NPCs state for game_id: {game_id}")
        if game_id not in game_map:
            logger.error(f"Game not found: {game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        state = game_map[game_id].get_npcs_state()
        logger.info(f"Successfully retrieved NPCs state for game_id: {game_id}")
        return {"npcs_state": state}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving NPCs state for game_id {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/locations_state/")
def get_locations_state(game_id: str):
    try:
        logger.info(f"Retrieving locations state for game_id: {game_id}")
        if game_id not in game_map:
            logger.error(f"Game not found: {game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        state = game_map[game_id].get_locations_state()
        logger.info(f"Successfully retrieved locations state for game_id: {game_id}")
        return {"locations_state": state}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving locations state for game_id {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player_state/{player_name}")
def get_state_for_player(player_name: str, game_id: str):
    try:
        logger.info(f"Retrieving state for player {player_name} in game {game_id}")
        if game_id not in game_map:
            logger.error(f"Game not found: {game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        state = game_map[game_id].get_state_for_player(player_name)
        logger.info(f"Successfully retrieved state for player {player_name}")
        return state
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving state for player {player_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_player/")
def update_player(player: Player):
    try:
        logger.info(f"Updating player {player.player_name} in game {player.game_id}")
        if player.game_id not in game_map:
            logger.error(f"Game not found: {player.game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        game_map[player.game_id].update_player(player.player_name, player.player_state)
        logger.info(f"Successfully updated player {player.player_name}")
        return {"message": "Player updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating player {player.player_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/game_checksum/")
def get_game_checksum(game_id: str):
    try:
        if game_id not in game_map:
            logger.error(f"Game not found: {game_id}")
            raise HTTPException(status_code=400, detail="Game not found")
        checksum = game_map[game_id].get_game_checksum()
        return {"game_checksum": checksum}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving game checksum for game_id {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    logger.info(f"Starting D&D server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)