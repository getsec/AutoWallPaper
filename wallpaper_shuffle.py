#!/usr/bin/python3
from random import choice
from os import listdir, system
from os.path import isfile, join
import configparser


config = configparser.ConfigParser()
config_file = "/home/cloud/.personal/AutoWallPaper/wp.conf"
config.read(config_file)

DIR = config.get('config', 'directory')


cmd = "gsettings set org.gnome.desktop.background picture-uri file://"
onlyfiles = [f for f in listdir(DIR) if isfile(join(DIR, f))]
full_dir = []
for item in onlyfiles:
    full_dir.append(f"{DIR}/{item}")


paper = choice(full_dir)
execute = f"{cmd}{paper}"
system(execute)
