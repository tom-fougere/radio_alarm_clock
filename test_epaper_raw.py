from waveshare_epd import epd2in13
from PIL import ImageDraw, Image, ImageFont

epd = epd2in13.EPD()
epd.init(epd.lut_full_update)

#Image de la dimension de l ecran - Image with screen size
#255: fond blanc - clear the image with white
image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)
draw = ImageDraw.Draw(image)

#Dessine un rectangle au centre de l ecran - draw a rectangle in the center of the screen
draw.rectangle((epd2in13.EPD_HEIGHT/2-10, epd2in13.EPD_WIDTH/2-10, epd2in13.EPD_HEIGHT/2+10, epd2in13.EPD_WIDTH/2+10), fill = 0)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
draw.text((0, 0), 'HELLO world', font=font, fill = 0)

#Actualise affichage - Update display
epd.display(epd.getbuffer(image))

print('end')