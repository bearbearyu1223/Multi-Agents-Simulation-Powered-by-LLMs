import sys
sys.path.append( '.' )

from agent import Player
from backends.openai_backend import OpenAIBackend
from environments.conversation import Conversation
from sim import Sim

if __name__=="__main__": 
    environment_description = """
    Nancy is using an AI assistant called "Nova" on iPhone to help her complete some daily tasks and make her daily life more organized. 
    """

    # Define the role of the User
    user = Player(name="Nancy", backend=OpenAIBackend(),
                 role_desc="""
                 You want AI Assistant to help you create an alarm for your HIIT class at 8:00am this Sunday, and share this 
                 event with your friend Crystal by texting her on WhatsApp. 
                 """,
                 global_prompt=environment_description)
    
    # Define the role of the AI Assistant 
    assistant = Player(name="Nova", backend=OpenAIBackend(), 
                       role_desc="""
                       You are Nova to help Nancy complete some daily tasks. Based on the asks from Nancy, you 
                       will diretcly complete the tasks in a few converstations. 
                       """,
                       global_prompt=environment_description)

    # Define the role of the Moderator
    moderator = Player(name="Ella", backend=OpenAIBackend(), 
                       role_desc="""
                       You are Ella, the moderator. Your goal is to evaluate if the converstations betweend Nancy and Nove can end.
                       Use the following criterion to decide if the converstation can end:

                       1. If Nova has fulfill all the requests Crystal and Crystal is happy with what Nova has accomplished, then converstation can end. 
                       2. If Nova cannot help fulfill the requests from Crystal, the converstation can end. 

                       If you consider the converstation can end, just say "<<<<<<END_OF_CONVERSATION>>>>>>", otherwise, say "converstation can continue"; do not say 
                       anything else. 
                       """,
                       global_prompt=environment_description)
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant, moderator]])
    sim = Sim(players=[user, assistant, moderator], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=20)


