import requests
from lxml import html
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlsplit
from sys import exit
from io import open as iopen
import configparser

# setting up the config parser
config = configparser.ConfigParser()
config_file = "wp.conf"
config.read(config_file)

# grabbing the config items from the file and creating local variables
# these will be used in the functions to download wallpapers
DIR      = config.get('config', 'directory')
PAGES    = config.get('config', 'depth')
CATEGORY = config.get('config', 'category')
RESOLUTE = config.get('config', 'resolution')
PURITY   = config.get('config', 'nsfw')

# nsfw mapping to wallhaven purity code
# 100 = SFW
# 111 = NSFW
# 110 = Sketchy...?
if PURITY.lower() == 'no':
    PCODE = '100'
if PURITY.lower() == 'yes':
    PCODE = '111'


# First we need to grab a list of all the image sources
# this function uses the search term and grabs all the hrefs that match to the images
def grab_list_of_curated_urls(url):
    headers = {
      "User-Agent": "Mozilla/532.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
    }

    data = requests.get(url, headers=headers)
    if data.status_code == 200:
        webpage = html.fromstring(data.content)
        hrefs = webpage.xpath('//a/@href')

        curated_list = []
        for url in hrefs:
            if len(url) == 43:
                curated_list.append(url)

        direct_url = []
        for url in curated_list:
            grab_content = requests.get(url).content
            soup = bs4(grab_content, 'lxml')
            images = soup.findAll('img')

            for image in images:
                direct_url.append(image['src'])

        return direct_url
    else:
        print("Received and error code from the server. Please ensure all config is correct without quotes.")
        print(f"Error Code: {str(data.status_code)}")
        print(f"Error Response:\n {data.content}")
        
        return False
        
# this function will grab every url and download them to the directory in the config
def requests_image(file_url, DIR):
    suffix_list = ['jpg', 'png']
    file_name = urlsplit(file_url)[2].split('/')[-1]
    file_suffix = file_name.split('.')[1]
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(DIR+file_name, 'wb') as file:
            file.write(i.content)

        return True
    else:
        return False

# this is a nice little function that gets the total number of pages for the category
# we will use this to ask the user if they want extra wallapers or if they go over
# the number of total wallpapers
def total_pages_of_wallpapers(CATEGORY):
    url = f"https://alpha.wallhaven.cc/search?q={CATEGORY}"
    html = requests.get(url).content
    def match_class(target):                                                        
        def do_match(tag):                                                          
            classes = tag.get('class', [])                                          
            return all(c in classes for c in target)                                
        return do_match                                                             

    soup = bs4(html, 'html.parser')                                                    
    data = soup.find_all('div', class_ = 'thumbs-container thumb-listing infinite-scroll')
    pages = data[0].h2.text
    total_pages = pages.split(' / ')[1]

    return total_pages

# the main function which completes the program
def main(CATEGORY, RESOLUTE, PAGES, PCODE):
    print("\n\nCurrently downloading files this takes roughly 20-30 seconds per page")
    print("Details below...\n")
    print(f"Category:   {CATEGORY}")
    print(f"Depth:      {str(PAGES)}")
    print(f"Resolution: {RESOLUTE}")

    DOWNLOADS = []

    for page in range(1, int(PAGES)):
        url = f"https://alpha.wallhaven.cc/search?q={CATEGORY}&categories=111&purity={PCODE}&atleast={RESOLUTE}&sorting=relevance&order=desc&page={str(page)}"
        
       
        image_list = grab_list_of_curated_urls(url)
        
        for item in image_list:
            if 'full' in item:
                url = f'https:{item}'
                DOWNLOADS.append(item)
                requests_image(url, DIR)
    
        print(f"ERROR CODE FROM REQUESTS: {url.status_code}")
        print(f"ERROR RESPONSE: \n {url.text}")
    return DOWNLOADS

   
# I just do this cause you are supposed to,
# I'm pretty sure this means you can only call the scrip from the command line
# ie; not as a pythong module
if __name__ in '__main__':

    TOTAL_PAGES = int(total_pages_of_wallpapers(CATEGORY))
    TPN = int(TOTAL_PAGES)
    PN = int(PAGES)
    if PN > TPN:
        print(f"Looks like the page number in your config [{PAGES}] is greater than the available pages [{TOTAL_PAGES}]")
        print(f"Because the programmer is lazy, go put your depth to [{TOTAL_PAGES}] :D")
        exit()


    if PN < TPN:
        print("Just a little bit of info\n#######################################")
        print(f"Looks like you are searching {PAGES} out of {TOTAL_PAGES} total pages")
        print(f"If you want more wallpapers just update your config depth to: {TOTAL_PAGES}")

        main(CATEGORY, RESOLUTE, PAGES, PCODE)

    if PN == TPN:
        main(CATEGORY, RESOLUTE, PAGES, PCODE)



    
      