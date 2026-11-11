Donkey Kong: DSA Edition

Layout
  main.py              entry point (game loop switcher)
  game/settings.py     window, constants, paths, colors, fonts
  game/assets.py       sounds, sprite loading, animated menu background
  game/pathfinder.py   BFS pathfinder for the AI player
  game/sprites.py      Player, DonkeyKong, Barrel, Fire, Coin, Platform, Ladder, Pauline, Cage
  game/ui.py           RPGButton, HUD
  game/levels.py       random level generator
  game/screens.py      menus, settings, how-to-play, credits
  game/gameplay.py     level loops and game modes
  assets/              images, sprites, sounds, fonts

Run on desktop:   python main.py   (needs: pip install pygame-ce)

Web build (pygbag), run from the folder that CONTAINS donkey_kong_dsa:
  python -m pip install pygbag
  python -m pygbag donkey_kong_dsa            test at http://localhost:8000
  python -m pygbag --archive donkey_kong_dsa  makes build/web.zip for itch.io
Or from inside donkey_kong_dsa:  python -m pygbag .
