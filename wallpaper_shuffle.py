#!/usr/bin/python3
from random import choice
from os import listdir, system
from os.path import isfile, join
_DIR = '/home/cloud/Pictures/wallpaper'
cmd = "gsettings set org.gnome.desktop.background picture-uri file://"
onlyfiles = [f for f in listdir(_DIR) if isfile(join(_DIR, f))]
full_dir = []
for item in onlyfiles:
    full_dir.append(f"{_DIR}/{item}")


paper = choice(full_dir)
execute = f"{cmd}{paper}"
system(execute)
