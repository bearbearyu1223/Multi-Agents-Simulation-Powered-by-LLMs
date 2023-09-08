import sys
sys.path.append( '.' )
from agent import Player
from backends.openai_backend import OpenAIBackend
from environments.conversation import Conversation
from sim import Sim

if __name__=="__main__": 
    environment_description = """
    Crystal正在寻找为她7岁的女儿迅速准备健康午餐的想法；她正试图从一个名为诺瓦（Nova）的人工智能助手那里获得一些建议。 
    """

    # Define the role of the User
    user = Player(name="Crystal", backend=OpenAIBackend(),
                 role_desc="""
                 您正在通过与一个人工智能助手Nova交谈来探讨为您的女儿提供快速且健康的学校午餐建议和想法。您将提供有关人工智能助手的回应的反馈，也可以提出后续问题。
                 你只说中文。
                 """,
                 global_prompt=environment_description)
    
    # Define the role of the AI Assistant 
    assistant = Player(name="Nova", backend=OpenAIBackend(), 
                       role_desc="""
                       您是Nova，人工智能助手。您的目标是在不超过200字的情况下为Crystal提供建议和想法；如果您找不到答案或不确定如何帮助，只需礼貌地结束对话。你只说中文。

                       """,
                       global_prompt=environment_description)
    
    # Define the role of the Moderator
    moderator = Player(name="Ella", backend=OpenAIBackend(), 
                       role_desc="""
                       您是Ella。您的目标是评估Crystal和 Nova之间的对话是否可以结束。请使用以下标准来决定是否可以结束对话：

                       1. 如果Nova已经回答了Crystal提出的所有请求，并且Crystal对Nova的回答感到满意，那么对话可以结束。
                       2. 如果Nova无法回答Crystal的问题，对话可以结束。

                       如果您认为对话可以结束，只需说 "<<<<<<END_OF_CONVERSATION>>>>>>"，否则，请说"continue". 不要说其他内容。
                       """,
                       global_prompt=environment_description)
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant, moderator]])
    sim = Sim(players=[user, assistant, moderator], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=10)


