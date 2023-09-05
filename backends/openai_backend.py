import openai
import os
from tenacity import retry, stop_after_attempt, wait_random_exponential
from message import Message, SYSTEM_NAME, MODERATOR_NAME
from typing import List
import re

# Default config follows the OpenAI playground
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 256 * 5
DEFAULT_MODEL = "gpt-3.5-turbo"

END_OF_MESSAGE = "<EOS>"  # End of message token specified by us not OpenAI
STOP = ("<|endoftext|>", END_OF_MESSAGE)  # End of sentence token
BASE_PROMPT = f"The messages always end with the token {END_OF_MESSAGE}."

def is_open_ai_key_available()->bool:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None: 
        return False
    else:
        return True


class OpenAIBackend: 
    """
    Interface to the ChatGPT style model with system, user, assistant roles. 
    """
    def __init__(self, temperature:float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS, model: str = DEFAULT_MODEL):
        assert is_open_ai_key_available(), "OpenAI API Key cannot be found on your system enviroment."
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        
    @retry(stop=stop_after_attempt(5), wait=wait_random_exponential(min=1, max=60))
    def _get_response(self, messages:List): 
        completion = openai.ChatCompletion.create(
            model = self.model, 
            messages = messages, 
            temperature = self.temperature,
            max_tokens = self.max_tokens, 
            stop = STOP 
        )
        response = completion.choices[0]['message']['content']
        response = response.strip()
        return response 
    
    def query(self, agent_name: str, role_desc: str, history_messages: List[Message], global_prompt: str = None, request_msg: Message = None, *args, **kwargs):
        """
        Parameters:
            agent_name: the name of the agent 
            role_desc: the description of the role of the agent 
            history_messages: the history of the converstation
            global_prompt (str): A global prompt that applies to all agents. (e.g., the simulaion scence description)
            request_msg: the request from the system to guide the agent's next response
        """
        
        if global_prompt:  # Prepend the global prompt if it exists
            system_prompt = f"\n{global_prompt.strip()}\n{BASE_PROMPT}\n\nYour name is {agent_name}.\n\nYour role:{role_desc}"
        else:
            system_prompt = f"You are a helpful assistant. Your name is {agent_name}.\n\nYour role:{role_desc}\n\n{BASE_PROMPT}"

        all_messages = [(SYSTEM_NAME, system_prompt)]
        for msg in history_messages: 
            if msg.agent_name == SYSTEM_NAME:
                all_messages.append((SYSTEM_NAME, msg.content))
            else: # non-system messages are suffixed with the end of message token
                all_messages.append((msg.agent_name, f"{msg.content}{END_OF_MESSAGE}"))
        
        if request_msg: 
            all_messages.append((SYSTEM_NAME, request_msg.content))
        else: # The default request message that reminds the agent its role and instruct it to speak
            all_messages.append((SYSTEM_NAME, f"Now you speak, {agent_name}.{END_OF_MESSAGE}"))
        
        messages = []
        for i, msg in enumerate(all_messages):
            if i == 0:
                assert msg[0] == SYSTEM_NAME  # The first message should be from the system
                messages.append({"role": "system", "content": msg[1]})
            elif "Now you speak".lower() in str(msg[1]).lower() and END_OF_MESSAGE.lower() in str(msg[1]).lower():
                messages.append({"role": "system", "content": msg[1]})
            else:
                if msg[0] == agent_name:
                    messages.append({"role": "assistant", "content": msg[1]})
                else:
                    if messages[-1]["role"] == "user":  # last message is from user
                        messages.append({"role": "user", "content": f"[{msg[0]}]: {msg[1]}"})
                    elif messages[-1]["role"] == "assistant":  # consecutive assistant messages
                        # Merge the assistant messages
                        messages[-1]["content"] = f"{messages[-1]['content']}\n{msg[1]}"
                    elif messages[-1]["role"] == "system":
                        messages.append({"role": "user", "content": f"[{msg[0]}]: {msg[1]}"})
                    else:
                        raise ValueError(f"Invalid role: {messages[-1]['role']}")

        response = self._get_response(messages, *args, **kwargs)

        # Remove the agent name if the response starts with it
        response = re.sub(rf"^\s*\[.*]:", "", response).strip()
        response = re.sub(rf"^\s*{re.escape(agent_name)}\s*:", "", response).strip()

        # Remove the tailing end of message token
        response = re.sub(rf"{END_OF_MESSAGE}$", "", response).strip()

        return response


            

    

