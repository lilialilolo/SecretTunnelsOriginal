import asyncio
from farm import farm


async def fight(name, p1, p2, p3, p4=None):
    battle = p1.get_battle(name)
    
    hitter_pos = 7 if p4 else 6
    
    while await battle.loop():
        ##############################################
        # Player1 mass feint
        m_feint = await p1.find_spell('mass-feint')
        if m_feint:
            await m_feint.cast()
        else:
            await p1.pass_turn()
        
        ##############################################
        # Player2 elemental blades
        blade = await p2.find_spell('elemental-blade')
        if blade:
            await blade.cast(target=hitter_pos) # cast at last player
        else:
            await p2.pass_turn()
            
        
        if p4:
            ##############################################
            # Player 3 enchanted elemental blade
            blade = await p3.find_spell('elemental-blade')
            sharpen = await p3.find_spell('sharpened-blade')
            # e_blade = await p3.find_spell('elemental-blade-enchanted')
            # if e_blade:
                # await e_blade.cast(target=hitter_pos) # cast at last player
            if blade and sharpen:
                e_blade = await sharpen.enchant(blade)
                await e_blade.cast(target=hitter_pos) # cast at last player
            else:
                await p3.pass_turn()
            
            ##############################################
            # Player 4 tempest
            tempest = await p4.find_spell('tempest')
            epic = await p4.find_spell('epic')
            # e_temp = await p4.find_spell('tempest-enchanted')
            # if e_temp:
            #     await e_temp.cast()
            if tempest and epic:
                e_temp = await epic.enchant(tempest)
                await e_temp.cast()
            else:
                await p4.pass_turn()
        else:
            ##############################################
            # Player 3 tempest
            tempest = await p3.find_spell('tempest')
            epic = await p3.find_spell('epic')
            # e_temp = await p3.find_spell('tempest-enchanted')
            # if e_temp:
            #     await e_temp.cast()
            if tempest and epic:
                e_temp = await epic.enchant(tempest)
                await e_temp.cast()
            else:
                await p3.pass_turn()
                


asyncio.run(farm(fight))