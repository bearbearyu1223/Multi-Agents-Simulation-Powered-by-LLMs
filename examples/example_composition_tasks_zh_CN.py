import sys
sys.path.append( '.' )

from agent import Player
from backends.openai_backend import OpenAIBackend
from environments.conversation import Conversation
from sim import Sim

if __name__=="__main__": 
    environment_description = """
    Nancy正在使用iPhone上的名为 Nova 的人工智能助手，帮助她完成一些日常任务，使她的日常生活更有条理。 
    """

    # Define the role of the User
    user = Player(name="Nancy", backend=OpenAIBackend(),
                 role_desc="""
                 您希望您的AI助手Nova帮助您在本周日上午8:00为您的 Hot Yoga 课程创建一个闹钟，并通过WhatsApp将这个事件与你的朋友Crystal分享。你只说中文。 
                 """,
                 global_prompt=environment_description)
    
    # Define the role of the AI Assistant 
    assistant = Player(name="Nova", backend=OpenAIBackend(), 
                       role_desc="""
                       您是AI助手Nova，负责帮助Nancy完成一些日常任务。根据Nancy的要求，您将在几次对话中直接完成这些任务。你只说中文。
                       """,
                       global_prompt=environment_description)

    # Define the role of the Moderator
    moderator = Player(name="Ella", backend=OpenAIBackend(), 
                       role_desc="""
                       您是Ella。您的目标是评估 Nancy 和 Nova之间的对话是否可以结束。请使用以下标准来决定是否可以结束对话：

                       1. 如果Nova已经回答了Nancy提出的所有请求，并且Nancy对Nova的回答感到满意，那么对话可以结束。
                       2. 如果Nova无法回答Nancy的问题，对话可以结束。

                       如果您认为对话可以结束，只需说 "<<<<<<END_OF_CONVERSATION>>>>>>"，否则，请说"continue"。不要说其他内容。
                       """,
                       global_prompt=environment_description)
    
    
    # Instantiate the Conversation Simulation Environment 
    env = Conversation(player_names=[p.name for p in [user, assistant, moderator]])
    sim = Sim(players=[user, assistant, moderator], environment=env, global_prompt=environment_description)
    sim.launch_cli(interactive=True, max_steps=20)


