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
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant]])
    sim = Sim(players=[user, assistant], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=10)


