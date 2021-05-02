from PIL import ImageDraw, Image, ImageFont

MARGIN_Y = 5
MARGIN_X = 5
MARGIN_BETWEEN_CHAR = 5
TIME_Y = -10
DAY_Y = 65 + TIME_Y

MAX_X = 250
MAX_Y = 122

DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
MONTHS = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

FONT_BOLD = '/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf'
FONT_THIN = '/usr/share/fonts/truetype/piboto/Piboto-Thin.ttf'
FONT_LIGHT = '/usr/share/fonts/truetype/piboto/Piboto-Light.ttf'


class Screen2in13:
    def __init__(self, size):
        self.image = Image.new('1', size, 255)  # 255: clear the frame
        self.screen = ImageDraw.Draw(self.image)

        self.wifi = False
        self.hour = 'XX'
        self.minute = 'XX'
        self.week_day = 'XXX'
        self.day_number = 'XX'
        self.month = 'XXX'
        self.event_today = ''
        self.event_tomorrow = ''
        self.alarm = False

    def set_params(self, datetime, events, is_wifi_on=False, is_alarm_on=True):

        # Set parameters
        self.wifi = is_wifi_on
        self.alarm = is_alarm_on
        self.hour = str(datetime.hour)
        self.minute = str(datetime.minute).zfill(2)
        self.week_day = DAYS[datetime.isoweekday() - 1]
        self.day_number = str(datetime.day)
        self.month = MONTHS[datetime.month - 1]
        if events[0] is not None:
            self.event_today = events[0]['summary']
        if events[1] is not None:
            self.event_tomorrow = events[1]['summary']

        # Build screen with saved parameters
        self.build_screen()


    def build_screen(self):

        self.draw_hour()
        self.draw_date()
        self.draw_events()
        self.draw_icons()

    def draw_hour(self):

        hour_font = ImageFont.truetype(FONT_BOLD, 55)
        minute_font = ImageFont.truetype(FONT_LIGHT, 55)

        # Hours
        x_position = MAX_X - get_font_size(self.screen, self.hour, hour_font)[0] - MARGIN_BETWEEN_CHAR\
                           - get_font_size(self.screen, self.minute, minute_font)[0] - 3
        self.screen.text((x_position, TIME_Y), self.hour, font=hour_font, fill = 0)

        # Minutes
        x_position = MAX_X - get_font_size(self.screen, self.minute, minute_font)[0] - 3
        self.screen.text((x_position, TIME_Y), self.minute, font=minute_font, fill = 0)

    def draw_date(self):

        day_font = ImageFont.truetype(FONT_THIN, 14)
        day_font_bold = ImageFont.truetype(FONT_BOLD, 14)

        # Week day
        x_position = MAX_X - get_font_size(self.screen, self.month, day_font)[0] - MARGIN_X\
                           - get_font_size(self.screen, self.day_number, day_font_bold)[0] - MARGIN_BETWEEN_CHAR\
                           - get_font_size(self.screen, self.week_day, day_font)[0] - MARGIN_BETWEEN_CHAR
        self.screen.text((x_position, DAY_Y), self.week_day, font=day_font, fill = 0)

        # Day
        x_position = MAX_X - get_font_size(self.screen, self.month, day_font)[0] - MARGIN_X\
                           - get_font_size(self.screen, self.day_number, day_font_bold)[0] - MARGIN_BETWEEN_CHAR
        self.screen.text((x_position, DAY_Y), self.day_number, font=day_font_bold, fill = 0)

        # Month
        x_position = MAX_X - get_font_size(self.screen, self.month, day_font)[0] - MARGIN_X
        self.screen.text((x_position, DAY_Y), self.month, font=day_font, fill = 0)

    def draw_icons(self):

        # Wifi
        if self.wifi is True:
            bmp_wifi = Image.open('icons/wifi_on.png')
        else:
            bmp_wifi = Image.open('icons/wifi_off.png')
        # bmp_wifi = bmp_wifi_on.resize((24, 26))
        self.image.paste(bmp_wifi, (MARGIN_X, 0 + MARGIN_Y))

        # Alarm
        if self.alarm is True:
            bmp_alarm = Image.open('icons/alarm.png')
            # bmp_alarm = bmp_alarm.resize((24, 26))
            self.image.paste(bmp_alarm, (MARGIN_X, 30 + MARGIN_Y))

    def draw_events(self):

        nb_char = 25
        margin_calendar_icon = 3
        bmp_calendar_size = (24, 24)
        event_font = ImageFont.truetype(FONT_THIN, 13)

        # Today Event
        bmp_calendar_today = Image.open('icons/calendar_today.png')
        self.image.paste(bmp_calendar_today, (MAX_X - bmp_calendar_size[0] - margin_calendar_icon,  MAX_Y - 2 * bmp_calendar_size[1]))
        x_position = MAX_X - get_font_size(self.screen, self.event_today[:nb_char], event_font)[0]\
                           - bmp_calendar_size[0] - margin_calendar_icon
        y_position = MAX_Y - 2*bmp_calendar_size[1] + 3
        self.screen.text((x_position, y_position), self.event_today[:nb_char], font=event_font, fill = 0)

        # Tomorrow Event
        bmp_calendar_tomorrow = Image.open('icons/calendar_tomorrow.png')
        self.image.paste(bmp_calendar_tomorrow, (MAX_X - bmp_calendar_size[0] - margin_calendar_icon, MAX_Y - bmp_calendar_size[1]))
        x_position = MAX_X - get_font_size(self.screen, self.event_tomorrow[:nb_char], event_font)[0]\
                           - bmp_calendar_size[0] - margin_calendar_icon
        y_position = MAX_Y - bmp_calendar_size[1] + 3
        self.screen.text((x_position, y_position), self.event_tomorrow[:nb_char], font=event_font, fill = 0)

    def get_screen(self):
            return self.image


def get_font_size(screen, text, font):
    return screen.textsize(text, font=font)