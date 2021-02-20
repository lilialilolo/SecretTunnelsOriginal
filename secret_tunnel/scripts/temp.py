import asyncio
from farm import farm


async def fight(name, *players):
    
    battle = players[0].get_battle(name)
    
    while await battle.loop():
        for p in players:
            temp = await p.find_spell('tempest')
            epic = await p.find_spell('epic')
            if temp and epic:
                e_temp = await epic.enchant(temp)
                await e_temp.cast()
            else:
                await p.pass_turn()
                


asyncio.run(farm(fight))