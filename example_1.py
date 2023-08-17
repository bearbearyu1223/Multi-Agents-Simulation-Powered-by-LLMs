from chatarena.agent import Player
from chatarena.backends import OpenAIChat
from chatarena.environments.conversation import Conversation
from chatarena.arena import Arena

if __name__ == "__main__":
    # Describe the environment (which is shared by all players)
    environment_description = """
    Crytsal, a 35 years old mom, is looking for quick and healthy school lunch preparation 
    ideas for her 7 years old daughter; she is trying to get some suggestions from an AI assistant. 
    Jane, a moderator, is assessing the response from AI assistant, her goal is to make sure AI assistant 
    generate polite, clean, and helpful response to Crystal. 
    """

    # Define the role of the Mom
    mom = Player(name="Crytsal", backend=OpenAIChat(),
                    role_desc="""
                    You are a 35 years old mom, is asking for Siri's suggestions for quick and healthy 
                    school lunch ideas for your 7 years old daughter Lanshu; you will provide
                    your feedback to Siri's suggestions or ask a follow up question.""",
                    global_prompt=environment_description)
                    
    # Define the role of the AI Assistant
    assistant = Player(name="Siri", backend=OpenAIChat(),
                    role_desc="""
                    You are AI assistant, you are providing suggestions and ideas to Crystal;  
                    if you cannot help, just politely end the conversations. 
                    """,
                    global_prompt=environment_description)
    
    # Define the role of the moderator
    moderator = Player(name="Jane", backend=OpenAIChat(),
                    role_desc="""
                    a moderator, is assessing the response from AI assistant, your goal is to evalute if 
                    the response generated from the AI assistant is polite, clean, and helpful response.  
                    """,
                    global_prompt=environment_description)

    env = Conversation(player_names=[p.name for p in [mom, assistant, moderator]], max_turn=10)
    arena = Arena(players=[mom, assistant, moderator],
                environment=env, global_prompt=environment_description)
    arena.launch_cli(interactive=True)
    

