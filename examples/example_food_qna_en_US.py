import sys
sys.path.append( '.' )
from agent import Player
from backends.openai_backend import OpenAIBackend
from environments.conversation import Conversation
from sim import Sim

if __name__=="__main__": 
    environment_description = """
    Crystal is looking for quick and healthy school lunch preparation ideas for her 7 years old daughter; 
    she is trying to get some suggestions from an AI assistant called Nova. 
    """

    # Define the role of the User
    user = Player(name="Crystal", backend=OpenAIBackend(),
                 role_desc="""
                 You are exploring suggestions and ideas for quick and healthy school lunch ideas for your daughter by talking to
                 an AI assistant. You will provide your feedback to responses from the AI assistant; you can also ask follow up questions.
                 """,
                 global_prompt=environment_description)
    
    # Define the role of the AI Assistant 
    assistant = Player(name="Nova", backend=OpenAIBackend(), 
                       role_desc="""
                       You are Nova, the AI assistant. Your goal is to provide suggestions and ideas to Crystal in less than 200 words;  
                       if you cannot find an answer or not sure how to help, just politely end the conversations. 
                       """,
                       global_prompt=environment_description)
    
    # Define the role of the Moderator
    moderator = Player(name="Ella", backend=OpenAIBackend(), 
                       role_desc="""
                       You are Ella, the moderator. Your goal is to evaluate if the converstations betweend Crystal and Nove can end.
                       Use the following criterion to decide if the converstation can end:

                       1. If Nova has provided answers to all the asks from Crystal and Crystal is also satisfied with the answer from Nova, then converstation can end. 
                       2. If Nova cannot help answer the questions from Crystal, the converstation can end. 

                       If you consider the converstation can end, just say "<<<<<<END_OF_CONVERSATION>>>>>>", otherwise, say "converstation can continue"; do not say 
                       anything else. 
                       """,
                       global_prompt=environment_description)
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant, moderator]])
    sim = Sim(players=[user, assistant, moderator], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=10)


