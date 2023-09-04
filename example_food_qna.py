from agent import Player
from backends.openai_backend import OpenAIBackend
from environments.conversation import Conversation
from sim import Sim

if __name__=="__main__": 
    environment_description = """
    Crystal, a 35 years old mom, is looking for quick and healthy school lunch preparation 
    ideas for her 7 years old daughter; she is trying to get some suggestions from an AI assistant. 
    """

    # Define the role of the User
    user = Player(name="Crystal", backend=OpenAIBackend(),
                 role_desc="""
                 You are a 35 years old mom, is exploring suggestions and ideas for quick and healthy school lunch ideas for your 7 years 
                 old daughter; you will provide your feedback to suggestions and ideas provided from the AI assistant, 
                 or ask a follow up question.
                 """,
                 global_prompt=environment_description)
    
    # Define the role of the AI Assistant 
    assistant = Player(name="ChatGPT", backend=OpenAIBackend(), 
                       role_desc="""
                       You are AI assistant, you are providing suggestions and ideas to Crystal;  
                       if you cannot find an answer or not sure how to help, just politely end the conversations. 
                       """,
                       global_prompt=environment_description)
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant]])
    sim = Sim(players=[user, assistant], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=10)


