from screens import *

from waveshare_epd import epd2in13
from PIL import ImageDraw, Image, ImageFont
from string import ascii_lowercase, ascii_uppercase


FONT_BOLD = 'fonts/piboto/Piboto-Bold.ttf'
FONT_THIN = 'fonts/piboto/Piboto-Thin.ttf'
FONT_LIGHT = 'fonts/piboto/Piboto-Light.ttf'
FONT_SIZE = 55

image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 255: clear the frame
screen = ImageDraw.Draw(image)

def test_get_max_size_digit():
    max_size_bold = 0
    max_size_thin = 0
    max_size_light = 0

    for minutes in range(10):

        font_bold = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)
        font_thin = ImageFont.truetype(FONT_THIN, FONT_SIZE)
        font_light = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)

        size_bold = get_font_size(screen, str(minutes), font_bold)
        size_thin = get_font_size(screen, str(minutes), font_thin)
        size_light = get_font_size(screen, str(minutes), font_light)

        if size_bold[0] > max_size_bold:
            max_size_bold = size_bold[0]
        if size_thin[0] > max_size_thin:
            max_size_thin = size_thin[0]
        if size_light[0] > max_size_light:
            max_size_light = size_light[0]

    print('Max size of digit ( Bold,', FONT_SIZE, '):', max_size_bold)
    print('Max size of digit ( Thin,', FONT_SIZE, '):', max_size_thin)
    print('Max size of digit ( Light,', FONT_SIZE, '):', max_size_light)


def test_get_max_size_minutes():
    max_size_bold = 0
    max_size_thin = 0
    max_size_light = 0

    for minutes in range(60):

        font_bold = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)
        font_thin = ImageFont.truetype(FONT_THIN, FONT_SIZE)
        font_light = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)

        size_bold = get_font_size(screen, str(minutes).zfill(2), font_bold)
        size_thin = get_font_size(screen, str(minutes).zfill(2), font_thin)
        size_light = get_font_size(screen, str(minutes).zfill(2), font_light)

        if size_bold[0] > max_size_bold:
            max_size_bold = size_bold[0]
        if size_thin[0] > max_size_thin:
            max_size_thin = size_thin[0]
        if size_light[0] > max_size_light:
            max_size_light = size_light[0]

    print('Max size of minutes ( Bold,',  FONT_SIZE, '):', max_size_bold)
    print('Max size of minutes ( Thin,',  FONT_SIZE, '):', max_size_thin)
    print('Max size of minutes ( Light,',  FONT_SIZE, '):', max_size_light)

def test_get_max_size_letter_lower():
    max_size_bold = 0
    max_size_thin = 0
    max_size_light = 0

    for char in ascii_lowercase:

        font_bold = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)
        font_thin = ImageFont.truetype(FONT_THIN, FONT_SIZE)
        font_light = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)

        size_bold = get_font_size(screen, char, font_bold)
        size_thin = get_font_size(screen, char, font_thin)
        size_light = get_font_size(screen, char, font_light)

        if size_bold[0] > max_size_bold:
            max_size_bold = size_bold[0]
        if size_thin[0] > max_size_thin:
            max_size_thin = size_thin[0]
        if size_light[0] > max_size_light:
            max_size_light = size_light[0]

    print('Max size of a lowercase character ( Bold,',  FONT_SIZE, '):', max_size_bold)
    print('Max size of a lowercase character ( Thin,',  FONT_SIZE, '):', max_size_thin)
    print('Max size of a lowercase character ( Light,',  FONT_SIZE, '):', max_size_light)

def test_get_max_size_letter_upper():
    max_size_bold = 0
    max_size_thin = 0
    max_size_light = 0

    for char in ascii_uppercase:

        font_bold = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)
        font_thin = ImageFont.truetype(FONT_THIN, FONT_SIZE)
        font_light = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)

        size_bold = get_font_size(screen, char, font_bold)
        size_thin = get_font_size(screen, char, font_thin)
        size_light = get_font_size(screen, char, font_light)

        if size_bold[0] > max_size_bold:
            max_size_bold = size_bold[0]
        if size_thin[0] > max_size_thin:
            max_size_thin = size_thin[0]
        if size_light[0] > max_size_light:
            max_size_light = size_light[0]

    print('Max size of a uppercase character ( Bold,', FONT_SIZE, '):', max_size_bold)
    print('Max size of a uppercase character ( Thin,', FONT_SIZE, '):', max_size_thin)
    print('Max size of a uppercase character ( Light,', FONT_SIZE, '):', max_size_light)

def test_get_size_string():

    my_string = 'Vendredi 17 Mai'

    font_bold = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)
    font_thin = ImageFont.truetype(FONT_THIN, FONT_SIZE)
    font_light = ImageFont.truetype(FONT_LIGHT, FONT_SIZE)

    size_bold = get_font_size(screen, my_string, font_bold)
    size_thin = get_font_size(screen, my_string, font_thin)
    size_light = get_font_size(screen, my_string, font_light)

    print('Size of the string "', my_string, '" in Bold (', FONT_SIZE, ') is :', size_bold[0])
    print('Size of the string "', my_string, '" in Thin (', FONT_SIZE, ') is :', size_thin[0])
    print('Size of the string "', my_string, '" in Light (', FONT_SIZE, ') is :', size_light[0])

if __name__ == '__main__':
    test_get_max_size_minutes()

