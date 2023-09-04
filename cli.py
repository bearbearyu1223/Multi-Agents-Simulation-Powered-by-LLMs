from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.text import Text
from rich.color import ANSI_COLOR_NAMES
import random
from sim import Sim
from message import SYSTEM_NAME
import logging

logging.getLogger().setLevel(logging.ERROR)

ASCII_ART = r"""
   ____                                    _   _               ____  _           
  / ___|___  _ ____   _____ _ __ ___  __ _| |_(_) ___  _ __   / ___|(_)_ __ ___  
 | |   / _ \| '_ \ \ / / _ \ '__/ __|/ _` | __| |/ _ \| '_ \  \___ \| | '_ ` _ \ 
 | |__| (_) | | | \ V /  __/ |  \__ \ (_| | |_| | (_) | | | |  ___) | | | | | | |
  \____\___/|_| |_|\_/ \___|_|  |___/\__,_|\__|_|\___/|_| |_| |____/|_|_| |_| |_|
                                                                                 
"""

visible_colors = [color for color in ANSI_COLOR_NAMES.keys() if color not in ["black", "white", "red", "green"] and "grey" not in color]

MAX_STEPS = 5

class SimCLI:
    """
    The CLI user interface for Simulation
    """ 
    def __init__(self, sim: Sim):
        self.sim = sim
    
    def launch(self, max_steps: int = None, interactive: bool = True):
        if not interactive and max_steps is None: 
            max_steps = MAX_STEPS
        
        console = Console()
        console.print(ASCII_ART, style="bold blue")
        timestep = self.sim.reset()
        console.print("Conversation Simulation Initiated!", style="bold green")

        env = self.sim.environment
        players = self.sim.players

        env_desc = self.sim.global_prompt
        num_players = env.num_players
        player_colors = random.sample(visible_colors, num_players)
        name_to_color = dict(zip(env.player_names, player_colors))
        name_to_color[SYSTEM_NAME]= "red"

        console.print(f"[bold green underline]Environment Description:[/]\n{env_desc}")

        # Print the player name, role_desc and backend_type
        for _, player in enumerate(players):
            player_name = Text(f"[{player.name}  Role Description]:")
            player_name.stylize(f"bold {name_to_color[player.name]} underline")
            console.print(player_name)
            console.print(player.role_desc)

        console.print("\n========= Simulation Start! ==========\n", style="bold green")

        step = 0
        while not timestep.terminal:
            if interactive:
                command = prompt([('class:command', "command (n/r/q/s/h) > ")],
                                 style=Style.from_dict({'command': 'blue'}),
                                 completer=WordCompleter(
                                     ['next', 'n', 'reset', 'r', 'exit', 'quit', 'q', 'help', 'h', 'save', 's']))
                command = command.strip()

                if command == "help" or command == "h":
                    console.print("Available commands:")
                    console.print("    [bold]next or n or <Enter>[/]: next step")
                    console.print("    [bold]exit or quit or q[/]: exit the game")
                    console.print("    [bold]help or h[/]: print this message")
                    console.print("    [bold]reset or r[/]: reset the game")
                    console.print("    [bold]save or s[/]: save the history to file")
                    continue
                elif command == "exit" or command == "quit" or command == "q":
                    break
                elif command == "reset" or command == "r":
                    timestep = self.arena.reset()
                    console.print("\n========= Simulation Reset! ==========\n", style="bold green")
                    continue
                elif command == "next" or command == "n" or command == "":
                    pass
                elif command == "save" or command == "s":
                    # Prompt to get the file path
                    file_path = prompt([('class:command', "save file path > ")],
                                       style=Style.from_dict({'command': 'blue'}))
                    file_path = file_path.strip()
                    # Save the history to file
                    self.sim.save_history(file_path)
                    # Print the save success message
                    console.print(f"History saved to {file_path}", style="bold green")
                else:
                    console.print(f"Invalid command: {command}", style="bold red")
                    continue
            timestep = self.sim.step()
            messages = [msg for msg in env.get_observation() if not msg.logged]
            # Print the new messages
            for msg in messages:
                message_text = Text(f"[{msg.agent_name}]: {msg.content}")
                message_text.stylize(f"bold {name_to_color[msg.agent_name]}", 0,
                                     len(f"[{msg.agent_name}]:"))
                console.print(message_text)
                msg.logged = True

            step += 1
            if max_steps is not None and step >= max_steps:
                break

        console.print("\n========= Simulation Ended! ==========\n", style="bold green")


