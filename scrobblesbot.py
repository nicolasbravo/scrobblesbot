from bs4 import BeautifulSoup
import urllib.request
import telebot
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def usertext(im, draw, text, font, **kwargs):
    text_size = draw.textsize(text, font)
    return draw.text(
        ((im.size[0] - text_size[0]) - 25, 25), text, font=font, **kwargs)

#telegram channel id
channel = ''

#change this per user
user = ''

#bot api
bot = telebot.TeleBot('')

topalbums = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=' + user + '&api_key=0bf495b3674404739d515e449ed6742e&period=7day&limit=5')
bsList = BeautifulSoup(topalbums.read(), "xml")
topalbum = bsList.find_all('image')
albumslist = bsList.find_all('name')
toplink = bsList.find_all('url')

topsongs = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=' + user + '&api_key=0bf495b3674404739d515e449ed6742e&period=7day&limit=5')
bsList = BeautifulSoup(topsongs.read(), "xml")
songslist = bsList.find_all('name')

topartist = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=' + user + '&api_key=0bf495b3674404739d515e449ed6742e&period=7day&limit=1')
bsList = BeautifulSoup(topartist.read(), "xml")
artistlinks = bsList.find_all('url')

img = Image.new('RGB', (800,800), 'white')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('/Library/Fonts/Ubuntu-L.ttf', 40)

draw.text((25, 25), "Top Albums", font=font, fill=(0,0,0))
draw.text((25, 410), "Top Artist", font=font, fill=(0,0,0))
draw.text((350, 410), "Top Songs", font=font, fill=(0,0,0))
usertext(img, draw, '@' + user, font, fill=(255,0,0))

font = ImageFont.truetype('/Library/Fonts/Ubuntu-L.ttf', 15)

w = 100
x = 0
y = 1
for z in range(1,6):
    draw.text((350, w), str(z) + ". " + str(albumslist[x].contents)[2:-2], font=font, fill=(0,0,0))
    w = w + 20
    draw.text((350, w), str(albumslist[y].contents)[2:-2], font=font, fill=(75,75,75))
    x = x + 2
    y = y + 2
    w = w + 40

w = 485
x = 0
y = 1
for z in range(1,6):
    draw.text((350, w), str(z) + ". " + str(songslist[x].contents)[2:-2], font=font, fill=(0,0,0))
    w = w + 20
    draw.text((350, w), str(songslist[y].contents)[2:-2], font=font, fill=(75,75,75))
    x = x + 2
    y = y + 2
    w = w + 40
    
imglink = str(topalbum[3].contents)[2:-2]
if imglink == '':
    imglink = str(topalbum[7].contents)[2:-2]
if imglink == '':
    imglink = str(topalbum[11].contents)[2:-2]
if imglink == '':
    imglink = str(topalbum[15].contents)[2:-2]
if imglink == '':
    imglink = str(topalbum[19].contents)[2:-2]
if imglink == '':
    imglink = 'https://cdn2.iconfinder.com/data/icons/capsocial-square-flat-3/500/lastfm-512.png'

albumdownload = requests.get(imglink)
bytes = BytesIO(albumdownload.content)
albumimg = Image.open(bytes)
width, height = albumimg.size
if width > height:
	albumimg = albumimg.crop((int((width-height)/2),0,int(width-(width-height)/2),height))
elif height > width:
	albumimg = albumimg.crop((0, int((height-width)/2),width,int(height-(height-width)/2)))
size = (300, 300)
albumimg = albumimg.resize(size, Image.BILINEAR)
img.paste(albumimg, (25,90))

file = requests.get(str(artistlinks[0])[5:-6] + '/+tracks')
file = str(file.text)[str(file.text).find('+images'):]
file = file[file.find('+images'):file.find('"')]
file = str(artistlinks[0])[5:-6] + '/' + file
file = requests.get(file)
file = str(file.text)[str(file.text).find('js-gallery-image'):]
file = file[file.find('src="') + 5:file.find('alt="')]
file = file[:file.rfind('"')]
artistlink = file

if artistlink == '':
    artistlink = 'https://cdn2.iconfinder.com/data/icons/capsocial-square-flat-3/500/lastfm-512.png'

artistdownload = requests.get(artistlink)
bytes = BytesIO(artistdownload.content)
artistimg = Image.open(bytes)
width, height = artistimg.size
if width > height:
	artistimg = artistimg.crop((int((width-height)/2),0,int(width-(width-height)/2),height))
elif height > width:
	artistimg = artistimg.crop((0, int((height-width)/2),width,int(height-(height-width)/2)))
size = (300, 300)
artistimg = artistimg.resize(size, Image.BILINEAR)
img.paste(artistimg, (25, 475))

img.save('scrobbles.png')
output = open('scrobbles.png', 'rb')
bot.send_photo(channel, output)