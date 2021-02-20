# Native imports
import os
from os import path
import sys
import traceback
import atexit

# Third party imports
import asyncio
import wizsdk
from wizsdk import Client, register_clients, XYZYaw

############################################################

# CONSTANTS
__DIR__ = path.dirname(path.abspath(__file__))
L_FIGHT1 = XYZYaw(x=1085.361, y=-2914.182, z=0.195, yaw=5.417)
L_FIGHT2 = XYZYaw(x=5718.185, y=-4054.871, z=0.195, yaw=4.598)
L_EXIT = XYZYaw(x=174.189, y=1067.975, z=0.556, yaw=3.021)


# HELPER FUNCTIONS
async def teleport_party(players):
    for p in players:
        await p.teleport_to_friend(__DIR__ + "/green_gem.png")

    await players[-1].finish_loading()


async def join_fight(player, delay, run_duration=2):
    await asyncio.sleep(delay)
    await player.send_key("W", run_duration)


async def join_fight_in_order(players, delay_between=0.5, run_duration=1.5):
    await asyncio.gather(*[
      join_fight(player, i * delay_between, run_duration) 
      for i, player in enumerate(players)
    ])


async def go_through_dialogs(players):
    await asyncio.gather(*[
      player.go_through_dialog() 
      for player in players
    ])


async def mass_teleport_to(location, players):
    await asyncio.gather(*[
      player.teleport_to(location)
      for player in players
    ])
    
async def check_all_potions(players):
    for p in players:
        await p.use_potion_if_needed()


async def farm(fight):
    try:
        clients = register_clients(-1, ["Player1", "Player2", "Player3", "Player4"])
        # teammates is a subarray that leaves out Player1
        teammates = clients[1:]
        # Assign the clients to variables, assign None if no clients are left
        p1, p2, p3, p4 = [*clients, None, None, None][:4]
        # Activate hooks on all clients
        await asyncio.gather(*[p.activate_hooks() for p in clients])

        # LOOP INDEFINITELY
        while True:
            # GO IN
            await p1.press_x()
            await p1.wait(5)
            await p1.finish_loading()

            await p1.send_key("W", 1)
            await p1.go_through_dialog()
            
            # GO TO FIRST FIGHT
            await p1.teleport_to(L_FIGHT1)
            
            # EVERYONE JOINS THE DUNGEON
            await teleport_party(teammates)
            await check_all_potions(clients)

            # 1st FIGHT
            await join_fight_in_order(clients)
            await fight("Gannon", *clients)
            await go_through_dialogs(clients)

            # GO TO SECOND FIGHT
            await mass_teleport_to(L_FIGHT2, clients)
            await go_through_dialogs(clients)
            await p1.wait(4)
            
            # 2nd FIGHT
            await join_fight_in_order(clients)
            await fight("Madd'n", *clients)
            await p1.go_through_dialog()

            # Start over
            await p1.teleport_to(L_EXIT)
            await p1.click_confirm()
            await p1.finish_loading()
            # Back up
            await p1.send_key("S", 0.5)
            while not p1.is_press_x():
                await p1.wait(.2)
                await p1.send_key("S", 0.2)
    # Handle Errors
    except Exception:
        traceback.print_exc()
    finally:
        # ALWAYS UNREGISTER!
        await unregister_all()
  

# Only run this if the script is being called directly!
# if __name__ == "__main__":
#     if '--preset' in sys.argv:
#         index = sys.argv.index('--preset')
#         print(len(sys.argv))
#         if len(sys.argv) > index + 1:
#             selected_preset = sys.argv[index + 1]
#             # Check if the preset exists
#             # Load fight preset module
#             # Run
#         else:
#             # List presets
#             dirs = os.listdir('presets')
#             print('Choose from the following presets:')
#             print('\n'.join(['- ' + filename[:-3] for filename in dirs]))
        