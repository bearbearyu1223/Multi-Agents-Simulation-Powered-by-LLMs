from abc import abstractmethod
from typing import List
from message import Message
from backends.openai_backend import OpenAIBackend
from tenacity import RetryError
import logging
import uuid

SIGNAL_END_OF_CONVERSATION = "<<<<<<END_OF_CONVERSATION>>>>>>{}.format(uuid.uuid4())"

class Agent:
    def __init__(self, name:str, role_desc:str, global_prompt:str=None):
        """
        Constructor to initialize the agent. 
        Parameters: 
            name (str): The name of the agent. 
            role_desc (str): Description of the agent's role. 
            global_prompt (str): A global prompt that applies to all agents. (e.g., the simulaion scence description)
        """
        self.name = name 
        self.role_desc = role_desc
        self.global_prompt = global_prompt

class Player(Agent): 
    """
    The Player class represent a role player in the converstation simulation enviroment. A player
    has access to the converstation history and can generate a response based on the observation. 
    """
    def __init__(self, name: str, role_desc: str, backend: OpenAIBackend, global_prompt: str= None,  *args, **kwargs):
        super().__init__(name=name, role_desc=role_desc, global_prompt=global_prompt)
        """
        Constructor to initialize the player. 
        Parameters: 
            name (str): The name of the player. 
            role_desc (str): Description of the player's role. 
            backend (str): The name of the LLM backend. Default to OPEN_AI. 
            global_prompt (str): A global prompt that applies to all agents. (e.g., the simulaion scence description)
        """
        self.back_end = backend
    
    def act(self, observation: List[Message]): 
        """
        Take an action based on the observation. 
        Parameters: 
            observation (List[Message]): The messages that the player has observed from the enviroment. 
        Returns: 
            str: The action (response) of the player. 
        """
        try: 
            assert isinstance(self.back_end, OpenAIBackend)
            response = self.back_end.query(agent_name=self.name, role_desc=self.role_desc, global_prompt = self.global_prompt, history_messages=observation, request_msg=None)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg
        return response
    
    def __call__(self, observation: List[Message]) -> str:
        return self.act(observation)


