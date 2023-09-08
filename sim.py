from agent import Player
import uuid
from environments.conversation import Conversation, TimeStep
from typing import List, Dict
import logging
import json

class Sim: 
    """
    Class to manage the Simulation 
    """
    def __init__(self, players: List[Player], environment: Conversation, global_prompt: str=None) -> None:
        self.players = players
        self.environment = environment
        self.global_prompt = global_prompt
        self.current_timestep = environment.reset()
        self.uuid = uuid.uuid4()

    @property
    def num_players(self)->int: 
        return self.environment.num_players
    
    @property
    def name_to_player(self) -> Dict[str, Player]:
        return {player.name: player for player in self.players}

    def reset(self) -> TimeStep:
        # Reset the environment
        self.current_timestep = self.environment.reset()
        # Reset the uuid
        self.uuid = uuid.uuid4()
        return self.current_timestep
    
    def step(self) -> TimeStep:
        """
        Take a step in the sim: one player takes an action and the environment updates
        """
        player_name = self.environment.get_next_player()
        player = self.name_to_player[player_name]  # get the player object
        observation = self.environment.get_observation(player_name)  # get the observation for the player
        action = player(observation)
        timestep = self.environment.step(player_name, action)
        if timestep is None:  # if the player made invalid actions, terminate the game
            warning_msg = f"{player_name} has made invalid actions for {self.invalid_actions_retry} times. Terminating the game."
            logging.warning(warning_msg)
        return timestep

    def run(self, num_steps: int = 1):
        """
        run the game for num_turns
        """
        for i in range(num_steps):
            timestep = self.step()
            if timestep.terminal:
                break
    
    
    def launch_cli(self, max_steps: int = None, interactive: bool = True):
        """
        launch the command line interface
        """
        from cli import SimCLI
        cli = SimCLI(self)
        cli.launch(max_steps=max_steps, interactive=interactive)

    def save_history(self, path: str):
        """
        save the history of the converstation sim to a json file
        """
        messages = self.environment.get_observation()
        message_rows = []
        for message in messages:
                message_row = {
                    "agent_name": message.agent_name,
                    "content": message.content,
                    "turn": message.turn,
                    "timestamp": str(message.timestamp),
                    "visible_to": message.visible_to,
                    "msg_type": message.msg_type,
                }
                message_rows.append(message_row)

        with open(path, "w") as f:
            json.dump(message_rows, f, indent=4, ensure_ascii=False)



        
