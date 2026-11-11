"""Donkey Kong: DSA Edition - entry point."""
import asyncio

from game.screens import main_menu, settings_menu, mode_select
from game.gameplay import single_player_campaign, vs_ai_mode, run_2p_race_level


async def main():
    curr = "menu"
    while True:
        if curr == "menu": curr = await main_menu()
        elif curr == "settings": curr = await settings_menu()
        elif curr == "mode_select": curr = await mode_select()
        elif curr == "singleplayer": curr = await single_player_campaign()
        elif curr == "vs_ai": curr = await vs_ai_mode()
        elif curr == "race_mode": curr = await run_2p_race_level(1)

asyncio.run(main())
