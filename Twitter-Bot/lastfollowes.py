'''
Este script recopila a los últimos 5 seguidores, descarga sus fotos de perfil, crea un banner
personalizado lo sube y actualiza
'''
from app.twlogin import login
from PIL import Image, ImageDraw, ImageFont
import os

def banner(path):
   #creamos la imagen
   #banner de twitter sugiere estas medidas
   WIDTH = 1500
   HEIGHT = 500
   SIZE = (WIDTH, HEIGHT)
   fondo = (5,5,5)
   image = Image.new('RGB', SIZE, fondo)

   wpp  = Image.open(path+'bins/wpp.png')
   pos = (650,170)
   image.paste(wpp, pos)

   # Para el texto:

   #TITULO
   text_color = (250,250,250)
   TEXT_FONT_TYPE = (path+'bins/MonoLisaSimpson-Regular.ttf')
   TEXT_SIZE = 55
   TEXT_PADDING_HOR = 550
   TEXT_PADDING_VERT = 50
   IMG_TEXT = 'WELCOME!'
   draw = ImageDraw.Draw(image)
   font = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE)
   offset_text = (TEXT_PADDING_HOR, TEXT_PADDING_VERT)
   draw.text(offset_text, IMG_TEXT, text_color, font=font)

   TEXT_SIZE = 30
   TEXT_PADDING_HOR = 45
   TEXT_PADDING_VERT = 130
   IMG_TEXT = 'A special thanks for my\n\nlast 5 followers, u rocks!'

   draw = ImageDraw.Draw(image)
   font = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE)
   offset_text = (TEXT_PADDING_HOR, TEXT_PADDING_VERT)
   draw.text(offset_text, IMG_TEXT, text_color, font=font)

#Como vamos a añadir a los ultimos 5 usuarios
#Descargamos la imagen y nombre de los ultimos 5 followers para crear imagen
   api = login('/home/ghost/rpibots/')
   
   user = api.get_user(screen_name='nodobtcbot')
   i=1
   for follower in user.followers()[:5]:
      target  = follower._json['profile_image_url']
      commando = 'wget -O '+path+follower._json['screen_name'][:]+'.jpg'+' '+target
      os.system(commando);
      im  = Image.open(path+follower._json['screen_name'][:]+'.jpg')
      im_pos = (i+40+i*30,190+i*50)
      image.paste(im, im_pos)
      TEXT_SIZE = 25
      IMG_TEXT = follower._json['screen_name'][:]
      draw = ImageDraw.Draw(image)
      font = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE)
      offset_text = (i+100+i*30,200+i*50)
      i+=1
      draw.text(offset_text, IMG_TEXT, text_color, font=font)
      os.remove(path+follower._json['screen_name'][:]+'.jpg')


   image.save(path+'bins/out.png')
   api.update_profile_banner(path+'bins/out.png')
   os.remove(path+'bins/out.png')
   #tw_user = '⚡₿it₿ol🇧🇴 | in ⌚⛓️'+blockclock() 
   #api.update_profile(name=tw_user)


if __name__=='__main__':
   p1='/home/ghost/rpibots/BitcoinResearch/Twitter-Bot/'
   banner(path=p1)

