from typing import List, Union
from dataclasses import dataclass
import time 
from uuid import uuid1
import hashlib

# Preserved roles
MODERATOR_NAME = "Moderator"
SYSTEM_NAME = "System"

def _hash(input:str)->str:
    """
    Helper function that generates a SHA256 has of a given input string. 

    Parameters:
        input (str) : The input string to be hashed. 
    
    Returns:
        str: The SHA256 hash of the input string.  
    """
    hex_dig = hashlib.sha256(input.encode()).hexdigest()

@dataclass
class Message: 
    """
    Represents a message in the conversation simulation enviroment. 

    Attributes: 
        agent_name (str) : Name of the agent sending the message. 
        content (str) : Content of the message. 
        turn (int) : The turn at which the message was sent. 
        timestamp (int) : Wall time at which the message was sent. Defaults to current time in nanosecond. 
        visible_to (Union[str, List(str)]) : The receivers of the message. Can be a single agent, multiple agents, or "all". Default to "all". 
        msg_type (str) : Type of the message, e.g., "text". Defaults to "text". 
        logged (bool) : Whether the message is logged in the database. Defaults to False. 
    """
    agent_name : str
    content : str
    turn : int 
    timestamp : int = time.time_ns()
    visible_to : Union[str, List[str]] = 'all'
    msg_type : str = "text"
    logged: bool = False

    @property
    def msg_hash(self): 
        return _hash(f"agent: {self.agent_name}\ncontent: {self.content}\ntimestamp: {str(self.timestamp)}\nturn: {self.turn}\nmsg_type: {self.msg_type}")

class MessagePool():
    """
    A pool to manage the messages in the converstation simulation enviorment. 
    """
    def __init__(self) -> None:
        self.conversation_id = str(uuid1())
        self._messages : List[Message] = []
        self._last_message_idx = 0 
    
    def reset(self): 
        self._messages = [] 
    
    def append_message(self, message: Message):
        self._messages.append(message)
    
    def print(self): 
        for message in self._messages: 
            print("[{} -> {}]: {}".format(message.agent_name, message.visible_to, message.content))
    
    @property
    def last_turn(self): 
        if len(self._messages) == 0: 
            return 0
        else:
            return self._messages[-1].turn
    
    @property
    def last_message(self): 
        if len(self._messages) == 0: 
            return None
        else: 
            return self._messages[-1]
    
    def get_all_messages(self) -> List[Message]: 
        return self._messages
    
    def get_all_visible_messages_until_turn_x(self, agent_name:str, turn:int)->List[Message]: 
        prev_messages = [message for message in self._messages if message.turn <= turn]
        visible_messages = [] 
        for message in prev_messages: 
            if message.visible_to == "all" or agent_name in message.visible_to or agent_name == MODERATOR_NAME:
                visible_messages.append(message)
        return visible_messages

