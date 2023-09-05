from agent import SIGNAL_END_OF_CONVERSATION
from dataclasses import dataclass
from typing import List, Dict
from message import MessagePool, Message
import time

@dataclass
class TimeStep: 
    """
    Represents a single step in time within the simulation. It includes the observation, and terminal state. 

    Attributes: 
        observation (List[Message]): A list of messages (observations) for the current timestep 
        terminal (bool): A boolean indicating whether the current state is terminal. 
    """
    observation: List[Message]
    terminal: bool

class Conversation: 
    """
    Turn-based fully obserable conversation enviroment. 
    Next speaker order is either parallel or round-robin. 
    """

    def __init__(self, player_names: List[str]) -> None:
        self.message_pool = MessagePool()
        self.player_names = player_names
        self._current_turn = 0 
        self._next_player_idx = 0
        self.num_players = len(player_names)
    
    def reset(self): 
        self._current_turn = 0 
        self._next_player_idx = 0 
        self.message_pool.reset()
        init_timestep = TimeStep(observation=[], terminal=False)
        return init_timestep
        

    def print(self):
        self.message_pool.print()
    
    def get_next_player(self) -> str: 
        """
        get the next player
        """
        return self.player_names[self._next_player_idx]
    
    def get_observation(self, player_name=None) -> List[Message]:
        """
        get observation for the player
        """
        if player_name is None:
            return self.message_pool.get_all_messages()
        else:
            return self.message_pool.get_all_visible_messages_until_turn_x(player_name, turn=self._current_turn)
    
    def is_terminal(self) -> bool:
        """
        check if the conversation is over
        """
        # If the last message is the signal, then the conversation is over
        if self.message_pool.last_message.content.startswith(SIGNAL_END_OF_CONVERSATION):
            return True

    def step(self, player_name: str, action: str)->TimeStep:
        """
        step function that is called by the conversation simulation
        Args:
            player_name: the name of the player that takes the action
            action: the action that the agents wants to take
        """
        message = Message(agent_name=player_name, content=action, timestamp=time.time_ns(), turn=self._current_turn)
        self.message_pool.append_message(message)

        # Update the counters of the player idx
        if self._next_player_idx != 0:
            self._current_turn += 1
        self._next_player_idx = (self._next_player_idx + 1) % self.num_players

        timestep = TimeStep(observation=self.get_observation(),
                            terminal=self.is_terminal())  # Return all the messages
        return timestep





    