import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import { Textarea } from "./components/ui/textarea";
import { Pencil, X } from "lucide-react";
import { Switch } from "./components/ui/switch";
import * as api from './services/api';

export default function ChatUI() {
  const [userInput, setUserInput] = useState("");
  const [modelResponse, setModelResponse] = useState("");
  const [player, setPlayer] = useState({});
  const [editing, setEditing] = useState(false);
  const [showLocation, setShowLocation] = useState(false);
  const [selectedNpc, setSelectedNpc] = useState(null);
  const [playerName, setPlayerName] = useState("");
  const [gameId, setGameId] = useState("");
  const [isDm, setIsDm] = useState(false);
  const [showGameIdDialog, setShowGameIdDialog] = useState(true);
  const [isJoiningGame, setIsJoiningGame] = useState(false);
  const [isLoadingPlayer, setIsLoadingPlayer] = useState(false);
  const [playerNotFound, setPlayerNotFound] = useState(false);
  const [locationData, setLocationData] = useState(null);
  const [isLoadingLocation, setIsLoadingLocation] = useState(false);
  const [isSendingAction, setIsSendingAction] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isPolling, setIsPolling] = useState(false);
  const gameChecksumRef = useRef(0);
  const pollingIntervalRef = useRef(null);

  const pollGameUpdates = async () => {
    if (isPolling) return;
    setIsPolling(true);

    try {
      const response = await api.getGameChecksum(gameId);
      console.log('Polling response:', response);
      console.log('Current checksum:', gameChecksumRef.current);
      console.log('New checksum:', response.game_checksum);
      
      if (response.game_checksum && response.game_checksum !== gameChecksumRef.current) {
        console.log('Checksum changed, updating history...');
        gameChecksumRef.current = response.game_checksum;
        await updateHistory();
      }
    } catch (error) {
      console.error('Error polling game updates:', error);
    } finally {
      setIsPolling(false);
    }
  };

  const fetchInitialChecksum = async () => {
    try {
      const response = await api.getGameChecksum(gameId);
      console.log('Initial checksum response:', response);
      if (response.game_checksum) {
        gameChecksumRef.current = response.game_checksum;
      }
    } catch (error) {
      console.error('Error fetching initial checksum:', error);
    }
  };

  // Cleanup polling interval when component unmounts
  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  const handleGameIdSubmit = async () => {
    if (!gameId.trim() || !playerName.trim()) {
      setModelResponse('Please enter both game ID and player name');
      return;
    }
    setIsJoiningGame(true);
    setModelResponse('Wait while the DM prepares the game!');
    try {
      // Fetch game history
      const historyResponse = await api.getGameHistory(gameId);
      setModelResponse(historyResponse.history.join('\n') || 'No response from DM.');
      updatePlayerState();
      setShowGameIdDialog(false);
      
      // Start polling after joining game
      await fetchInitialChecksum();
      pollingIntervalRef.current = setInterval(pollGameUpdates, 10000);
    } catch (error) {
      console.error('Error joining game:', error);
      setModelResponse('Error joining the game. Please try again.');
    } finally {
      setIsJoiningGame(false);
    }
  };

  const updatePlayerState = async () => {
    if (!gameId || !playerName) return;
    
    setIsLoadingPlayer(true);
    try {
      // Fetch player state
      const playerResponse = await api.getPlayerState(playerName, gameId);
      if (playerResponse && playerResponse.player_state) {
        console.log(playerResponse);
        setPlayer(playerResponse.player_state);
        setPlayerNotFound(false);
        playerResponse.player_location.npcs = [];
        playerResponse.all_npcs_in_location.forEach(npc => {
          playerResponse.player_location.npcs.push(npc);
        });
        setLocationData(playerResponse.player_location);
        console.log(locationData);
      } else {
        setPlayerNotFound(true);
      }
    } catch (error) {
      console.error('Error updating player state:', error);
      setPlayerNotFound(true);
    } finally {
      setIsLoadingPlayer(false);
    }
  };


  const handleSend = async () => {
    if (isSendingAction) return;
    
    setIsSendingAction(true);
    try {
      await api.sendPlayerAction(gameId, playerName, userInput);
      setUserInput("");
      await updateHistory();
    } catch (error) {
      console.error(error);
      setModelResponse('Error sending action.');
    } finally {
      setIsSendingAction(false);
    }
  };
  
  const updateHistory = async () => {
    try {
      const response = await api.getGameHistory(gameId);
      setModelResponse(response.history.join('\n') || 'No response from DM.');
      updatePlayerState();
    } catch (error) {
      console.error(error);
      setModelResponse('Error fetching game history.');
    }
  }

  const handleChange = (key, value) => {
    setPlayer(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const handleInventoryChange = (index, key, value) => {
    const newInventory = [...player.inventory];
    newInventory[index][key] = value;
    setPlayer(prev => ({ ...prev, inventory: newInventory }));
    setHasChanges(true);
  };

  const handleAddInventoryItem = () => {
    const newItem = {
      name: '',
      description: '',
      weight: 0,
      value: 0,
      health: 0
    };
    setPlayer(prev => ({
      ...prev,
      inventory: [...(prev.inventory || []), newItem]
    }));
    setHasChanges(true);
  };

  const handleRemoveInventoryItem = (index) => {
    const newInventory = [...player.inventory];
    newInventory.splice(index, 1);
    setPlayer(prev => ({ ...prev, inventory: newInventory }));
    setHasChanges(true);
  };

  const handleSavePlayer = async () => {
    if (!hasChanges) return;
    
    setIsSaving(true);
    try {
      await api.updatePlayer(gameId, playerName, player);
      setHasChanges(false);
      setModelResponse(modelResponse + '\nPlayer data updated successfully!');
    } catch (error) {
      console.error('Error updating player:', error);
      setModelResponse('Error updating player data. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCloseLocation = () => {
    setShowLocation(false);
    setSelectedNpc(null);
  };

  const dmScrollRef = useRef(null);

  if (showGameIdDialog) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <Card className="w-full max-w-md p-6">
          <CardContent className="space-y-4">
            <h2 className="text-2xl font-bold text-center">Enter Game Details</h2>
            <Input
              value={gameId}
              onChange={(e) => setGameId(e.target.value)}
              placeholder="Enter game ID"
              className="w-full"
              disabled={isJoiningGame}
            />
            <Input
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              placeholder="Enter your player name"
              className="w-full"
              disabled={isJoiningGame}
            />
            <Button 
              onClick={handleGameIdSubmit}
              className="w-full"
              disabled={isJoiningGame}
            >
              {isJoiningGame ? 'Joining Game...' : 'Join Game'}
            </Button>
            {modelResponse && (
              <p className={`text-center ${isJoiningGame ? 'text-blue-500' : 'text-red-500'}`}>
                {modelResponse}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 text-black p-4">
      <div className="w-full max-w-2xl space-y-4">

        {/* Game Settings */}
        <Card className="shadow-md bg-white">
          <CardContent className="p-4 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center md:gap-4">
              <div className="flex-1">
                <p className="text-sm text-gray-500">Game ID</p>
                <p className="font-medium">{gameId}</p>
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-500">Player Name</p>
                <p className="font-medium">{playerName}</p>
              </div>
              <div className="flex items-center gap-2">
                <span>Player</span>
                <Switch checked={isDm} onCheckedChange={setIsDm} />
                <span>DM</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Player Info Card */}
        {playerName && (
          <Card className="shadow-md bg-white">
            <CardContent className="p-4 relative">
              {isLoadingPlayer ? (
                <div className="text-center py-4">Loading player state...</div>
              ) : playerNotFound ? (
                <div className="text-center py-4">
                  <p className="text-red-500">
                    Please ask the DM to add your player in the game, provide relevant info about you.
                  </p>
                </div>
              ) : (
                <>
                  <button onClick={() => setEditing(!editing)} className="absolute top-2 right-2 text-gray-600 hover:text-yellow-500">
                    <Pencil size={20} />
                  </button>
                  {editing && hasChanges && (
                    <button 
                      onClick={handleSavePlayer}
                      disabled={isSaving}
                      className="absolute top-2 right-8 text-gray-600 hover:text-green-500"
                    >
                      {isSaving ? 'Saving...' : 'Save Changes'}
                    </button>
                  )}
                  <h2 className="text-2xl font-bold mb-2">
                    {player.name || 'Unnamed Character'} (Level {player.level || 1} {player.race || 'Unknown'} {player.class_type || 'Unknown'})
                  </h2>
                  {editing ? (
                    <Textarea
                      value={player.description}
                      onChange={e => handleChange('description', e.target.value)}
                      className="mb-2"
                    />
                  ) : (
                    <p className="mb-2 italic">{player.description}</p>
                  )}
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <p><strong>❤️ HP:</strong> {editing ? <Input value={player.hp} onChange={e => handleChange('hp', Number(e.target.value))} /> : player.hp}</p>
                    <p><strong>⚔️ Attack:</strong> {editing ? <Input value={player.attack} onChange={e => handleChange('attack', Number(e.target.value))} /> : player.attack}</p>
                    <p><strong>🛡️ Defense:</strong> {editing ? <Input value={player.defense} onChange={e => handleChange('defense', Number(e.target.value))} /> : player.defense}</p>
                    <p><strong>💰 Money:</strong> {editing ? <Input value={player.money} onChange={e => handleChange('money', Number(e.target.value))} /> : `${player.money} gold`}</p>
                    <p><strong>📦 Max Carry:</strong> {editing ? <Input value={player.max_weight_to_carry} onChange={e => handleChange('max_weight_to_carry', Number(e.target.value))} /> : player.max_weight_to_carry}</p>
                    <p>
                      <strong>📍 Location:</strong> {editing ? (
                        <Input value={player.location || ''} onChange={e => handleChange('location', e.target.value)} />
                      ) : (
                        <button onClick={() => setShowLocation(!showLocation)} className="text-blue-600 underline">
                          {player.location || "Unknown"}
                        </button>
                      )}
                    </p>
                  </div>
                  <div className="mt-4">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-semibold">🎒 Inventory:</h3>
                      {editing && (
                        <Button onClick={handleAddInventoryItem} className="text-sm">
                          Add Item
                        </Button>
                      )}
                    </div>
                    <ul className="list-disc list-inside space-y-2">
                      {player.inventory && player.inventory.map((item, index) => (
                        <li key={index} className="group">
                          {editing ? (
                            <div className="grid grid-cols-2 gap-2 p-2 bg-gray-50 rounded">
                              <div className="col-span-2 flex justify-between items-center">
                                <span className="text-sm font-medium">Item #{index + 1}</span>
                                <Button 
                                  onClick={() => handleRemoveInventoryItem(index)}
                                  className="text-red-500 hover:text-red-700"
                                >
                                  Remove
                                </Button>
                              </div>
                              <Input 
                                value={item.name} 
                                onChange={e => handleInventoryChange(index, 'name', e.target.value)} 
                                placeholder="Name" 
                              />
                              <Input 
                                value={item.description} 
                                onChange={e => handleInventoryChange(index, 'description', e.target.value)} 
                                placeholder="Description" 
                              />
                              <Input 
                                type="number"
                                value={item.weight} 
                                onChange={e => handleInventoryChange(index, 'weight', Number(e.target.value))} 
                                placeholder="Weight" 
                              />
                              <Input 
                                type="number"
                                value={item.value} 
                                onChange={e => handleInventoryChange(index, 'value', Number(e.target.value))} 
                                placeholder="Value" 
                              />
                              <Input 
                                type="number"
                                value={item.health} 
                                onChange={e => handleInventoryChange(index, 'health', Number(e.target.value))} 
                                placeholder="Health" 
                              />
                            </div>
                          ) : (
                            `${item.name} - ${item.description} (Weight: ${item.weight}, Value: ${item.value}, Health: ${item.health})`
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        )}

        {/* Location and NPC cards */}
        {showLocation && locationData && (
          <Card className="shadow-md bg-white relative">
            <CardContent className="p-4">
              <button onClick={handleCloseLocation} className="absolute top-2 right-2 text-gray-600 hover:text-red-500">
                <X size={20} />
              </button>
              {isLoadingLocation ? (
                <div className="text-center py-4">Loading location data...</div>
              ) : (
                <>
                  <h3 className="text-lg font-bold mb-2">📍 Location: {locationData.name}</h3>
                  <p className="italic mb-2">{locationData.description}</p>
                  <div className="mb-2">
                    <strong>Items:</strong>
                    <ul className="list-disc list-inside">
                      {locationData.items.map((item, index) => (
                        <li key={index}>{item.name} - {item.description}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="mb-2">
                    <strong>NPCs:</strong>
                    <ul className="list-disc list-inside">
                      {locationData.npcs.map((npc, index) => (
                        <li key={index}>
                          <button onClick={() => setSelectedNpc(npc)} className="text-blue-600 underline">
                            {npc.name} - {npc.description} (HP: {npc.hp}, ATK: {npc.attack}, DEF: {npc.defense})
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <strong>Neighbouring Locations:</strong> {locationData.neighbours.join(', ')}
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        )}

        {selectedNpc && (
          <Card className="shadow-md bg-white relative">
            <CardContent className="p-4">
              <button onClick={() => setSelectedNpc(null)} className="absolute top-2 right-2 text-gray-600 hover:text-red-500">
                <X size={20} />
              </button>
              <h3 className="text-lg font-bold mb-2">{selectedNpc.name}</h3>
              <p className="italic mb-2">{selectedNpc.description}</p>
              <div className="grid grid-cols-2 gap-2 text-sm mb-2">
                <p><strong>Level:</strong> {selectedNpc.level}</p>
                <p><strong>Mood:</strong> {selectedNpc.mood}</p>
                <p><strong>HP:</strong> {selectedNpc.hp}</p>
                <p><strong>Attack:</strong> {selectedNpc.attack}</p>
                <p><strong>Defense:</strong> {selectedNpc.defense}</p>
                <p><strong>Money:</strong> {selectedNpc.money} gold</p>
                <p><strong>Location:</strong> {selectedNpc.location}</p>
                <p><strong>Max Carry:</strong> {selectedNpc.max_weight_to_carry}</p>
              </div>
              {selectedNpc.dialogue && selectedNpc.dialogue.length > 0 && (
                <div className="mt-2">
                  <h4 className="font-semibold mb-1">Dialogue History:</h4>
                  <div className="bg-gray-50 p-2 rounded max-h-40 overflow-y-auto">
                    {selectedNpc.dialogue.map((line, index) => (
                      <p key={index} className="text-sm mb-1">{line}</p>
                    ))}
                  </div>
                </div>
              )}
              {selectedNpc.inventory && selectedNpc.inventory.length > 0 && (
                <div className="mt-2">
                  <h4 className="font-semibold mb-1">Inventory:</h4>
                  <ul className="list-disc list-inside text-sm">
                    {selectedNpc.inventory.map((item, index) => (
                      <li key={index}>{item.name} - {item.description}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        <Card className="shadow-md bg-white">
          <CardContent ref={dmScrollRef} className="p-4 max-h-60 overflow-y-auto space-y-2">
            <h3 className="text-lg font-bold mb-2">Dungeon Master Responses:</h3>
            <div className="text-sm whitespace-pre-line">{modelResponse}</div>
          </CardContent>
        </Card>

        <Card className="shadow-lg bg-white">
          <CardContent className="space-y-4 p-4">
            <div className="flex gap-2">
              <Input
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Type your action..."
                className="flex-grow"
                disabled={isSendingAction}
              />
              <Button onClick={handleSend} disabled={isSendingAction}>
                {isSendingAction ? 'Sending...' : 'Send'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
