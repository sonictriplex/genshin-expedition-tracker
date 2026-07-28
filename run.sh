#!/bin/sh
cd "/home/jens/Projekte/GenshinImpact"
which python3 >/tmp/genshin_err.log 2>&1
python3 main.py >>/tmp/genshin_err.log 2>&1
