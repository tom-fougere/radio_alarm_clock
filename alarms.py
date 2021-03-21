import datetime


class Alarm:

    applied_delay = 0
    time_of_deactivation = 0

    def __init__(self):
        # Activation
        self.on_off = 0  # User set ON/OFF
        self.active = 0  # Alarm is ringing?

        # Date/Time of activation
        self.days = None  # Days of activation
        self.time = None  # Time of activation (hour & minute)

        # Sound
        self.sound = None  # Sound active if alarm is active

        # Options
        self.isEphemeral = None  # Does the alarm be deleted after ringing?
        self.delay_repetition = None  # Delay after alarm reactivation after snooze

    def set_alarm(self, hour, minute, sound):
        self.time = datetime.time(hour, minute)
        self.days = [1, 2, 3, 4, 5, 6, 7]
        self.isEphemeral = 0
        self.delay_repetition = 5
        self.sound = sound

    def set_off(self):
        self.on_off = 0

    def set_on(self):
        self.on_off = 1

    def check_activation(self, current_daytime):

        # Time of the alarm
        ring_time = add_minutes_to_time(self.time, Alarm.applied_delay)
        # Current measured time
        current_time = datetime.time(current_daytime.get_hour(), current_daytime.get_minute())

        if self.on_off == 1:
            # Check the current day is included in the days of alarm activation
            if current_daytime.get_weekday() in self.days:
                print("Alarm::Current Time %02d:%02d" % (current_daytime.get_hour(), current_daytime.get_minute()))
                print("Alarm::Alarm Time %02d:%02d" % (ring_time.hour, ring_time.minute))

                # Compare the current time and the alarm time (in case where sound is not playing)
                if ring_time == current_time and self.sound.isplay() == 0:
                    print("Alarm::Ring")
                    # Active alarm
                    self.active = 1
                    # Time of deactivation in case of long activation (1h)
                    Alarm.time_of_deactivation = add_minutes_to_time(current_time, 60)
                    # Play sound
                    self.sound.play()

        if self.active == 1:
            # If current time is higher than the time of deactivation, force deactivation
            if current_time > Alarm.time_of_deactivation:
                print("Alarm::Force deactivation of the alarm")
                self.deactivate()

    def snooze(self):
        print("Alarm::Snooze")
        # Stop sound
        self.sound.stop()
        # Add delay
        Alarm.applied_delay += self.delay_repetition

    def deactivate(self):
        print("Alarm::Deactivation")
        # Reset delay
        Alarm.applied_delay = 0

        if self.sound.isplay() == 1:
            # Stop Sound
            self.sound.stop()

        # Deactivate alarm
        self.active = 0

    def set_days(self, days):
        self.days = days

    def set_time(self, hour, minute):
        self.deactivate()
        self.time = datetime.time(hour, minute)


def add_minutes_to_time(time, added_minutes):
    full_date = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
    # full_date = full_date + datetime.timedelta(minutes = added_minutes)
    full_date = full_date + datetime.timedelta(added_minutes)
    return full_date.time()
