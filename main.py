"""Donkey Kong: DSA Edition - entry point."""
import asyncio
import sys
import traceback

import pygame

pygame.init()
_screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Donkey Kong: DSA Edition")


def _show(lines, color=(255, 255, 255)):
    """Draw plain text lines on the canvas (loading / error screen)."""
    _screen.fill((20, 20, 20))
    font = pygame.font.Font(None, 30)
    for i, line in enumerate(lines[:22]):
        _screen.blit(font.render(line[:110], True, color), (30, 30 + i * 30))
    pygame.display.flip()


async def main():
    # Show something immediately so the page never sits on a blank canvas.
    _show(["LOADING... please wait"], (255, 220, 120))
    await asyncio.sleep(0.1)

    try:
        # Heavy imports (images, sounds, sprites) happen here, after the first frame.
        from game.screens import main_menu, settings_menu, mode_select
        from game.gameplay import single_player_campaign, vs_ai_mode, run_2p_race_level
    except Exception:
        tb = traceback.format_exc()
        print(tb)
        _show(["STARTUP ERROR:"] + tb.splitlines()[-18:], (255, 80, 80))
        while True:
            await asyncio.sleep(1)

    curr = "menu"
    while True:
        if curr == "menu": curr = await main_menu()
        elif curr == "settings": curr = await settings_menu()
        elif curr == "mode_select": curr = await mode_select()
        elif curr == "singleplayer": curr = await single_player_campaign()
        elif curr == "vs_ai": curr = await vs_ai_mode()
        elif curr == "race_mode": curr = await run_2p_race_level(1)

asyncio.run(main())
