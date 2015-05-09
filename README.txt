The bot runs on Bejeweled Blitz through facebook: https://apps.facebook.com/bejeweledblitz

The following Python libraries need to be installed: Numpy

x_pad,y_pad and game_x_pad, game_y_pad need to be set manually depending where the game is on the screen. 

For best simulation, run through the Python shell, running the method "startPlaying()"

TODO:

- Make easier to run? Maybe autodetect if Bejeweled is open and throw appropriate error if not

- Minor Bug when the only move is with a "combo" item, it might not be detected. In worst case maybe just try all possible options if no valid move is detected?