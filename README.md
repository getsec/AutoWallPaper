# Auto WallPaper

Automatically downloads wall papers from https://alpha.wallhaven.cc/
![](https://media.giphy.com/media/xVu6vxIZzjeJ1aMRhl/giphy.gif)
## Requirements
- Python3.7 
- Gnome Desktop Manager on Ubuntu 18.04

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.
- configparser
- bs4
- requests

```bash
pip install configparser bs4 requests --user
```

## Usage
1. Setup the config file

```bash
vim wp.conf

[config]
directory = /home/cloud/Pictures/wallpaper
depth = 5
category = vaporwave
resolution = 1920x1080
```

2. Invoke the script
```bash
python3 wallpaper_get.py
```

3. User the wallpaper_shuffle.py to automatically set wallpapers (I put it in my zshrc but you can cron it or do whatever...)
```bash
python3 wallpaper_shuffle.py
```

## Roadmap
Add the NSFW Tag to make sure you dont download any boobies... :heavy_check_mark:

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
