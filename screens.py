from PIL import ImageDraw, Image

class Screen2in13:
    def __init__(self, size):
        self.image = Image.new('1', size, 255)  # 255: clear the frame
        self.screen = ImageDraw.Draw(self.image)

    def set_params(self, datetime, events):

        # font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        # self.screen.text((120, 80), 'Hello World', font = font, fill = 0)
        self.screen.rectangle([(0, 0), (50, 50)], outline=0)
        self.screen.rectangle([(0, 0), (30, 70)], outline=0)

    def get_screen(self):
        return self.image


