#!/bin/bash
export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export SDL_AUDIODRIVER=dummy
sleep 15
/usr/bin/python3 /home/katleight/Desktop/fortune_teller/game.py