const API_URL = 'http://localhost:8000';

export async function addPlayer(gameId, playerName) {
  const response = await fetch(`${API_URL}/add_player/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: gameId, player_name: playerName }),
  });
  if (!response.ok) throw new Error('Failed to add player');
  return response.json();
}

export async function sendPlayerAction(gameId, playerName, action) {
  const response = await fetch(`${API_URL}/player_action/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: gameId, player_name: playerName, action }),
  });
  if (!response.ok) throw new Error('Failed to send action');
  return response.json();
}

export async function getGameHistory(gameId) {
  const response = await fetch(`${API_URL}/game_history/?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch game history');
  return response.json();
}

export async function getPlayersState(gameId) {
  const response = await fetch(`${API_URL}/players_state/?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch players state');
  return response.json();
}

export async function getNpcsState(gameId) {
  const response = await fetch(`${API_URL}/npcs_state/?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch NPCs state');
  return response.json();
}

export async function getLocationsState(gameId) {
  const response = await fetch(`${API_URL}/locations_state/?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch locations state');
  return response.json();
}

export async function getPlayerState(playerName, gameId) {
  const response = await fetch(`${API_URL}/player_state/${playerName}?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch player state');
  return response.json();
}

export async function getGameChecksum(gameId) {
  const response = await fetch(`${API_URL}/game_checksum/?game_id=${gameId}`);
  if (!response.ok) throw new Error('Failed to fetch game checksum');
  return response.json();
}

export async function updatePlayer(gameId, playerName, playerState) {
  const response = await fetch(`${API_URL}/update_player/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: gameId, player_name: playerName, player_state: playerState }),
  });
  if (!response.ok) throw new Error('Failed to update player');
  return response.json();
}
