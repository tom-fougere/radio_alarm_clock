from datetime import datetime


class Notifications:
    def __init__(self):
        self.wifi = False
        self.alarm = False
        self.calendar_intervention = False

    def set_wifi(self, wifi):
        """
        Set wifi notification
        :param wifi: wifi value, boolean
        """
        self.wifi = wifi

    def set_alarm(self, alarm):
        """
        Set alarm notification
        :param alarm: alarm value, boolean
        """
        self.alarm = alarm

    def set_calendar_intervention(self, intervention):
        """
        Set calendar intervation notification
        :param intervention: intervention value, boolean
        """
        self.calendar_intervention = intervention

    def define_alarm_notif(self, current_datetime, event_today, event_tomorrow, limit_hour=14):
        """
        Define alarm notification
        Switch to the alarm notification of the next day following the current event and datetime
        :param current_datetime: the current datetime (to compare with the limit_hour
        :param event_today: Event of the current datetime (today)
        :param event_tomorrow: Event of the next datetime (tomorrow)
        :param limit_hour: Hour to switch between the alarm of the current day to the next day
        :return:
            - Flag for the bell displaying, boolean
        """

        if event_today.kind == 'Hour':
            if current_datetime <= event_today.end:
                self.alarm = event_today.is_alarm
            else:
                self.alarm = event_tomorrow.is_alarm
        else:
            if current_datetime < datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                           hour=limit_hour, minute=0, second=0):
                self.alarm = event_today.is_alarm
            else:
                self.alarm = event_tomorrow.is_alarm

    def define_calendar_intervention_notif(self, events):
        """
        Define manual intervention is possible
        :param events: Events
        """

        alarm_available = False
        for event in events:
            if event.kind != 'None' and event.is_alarm == True:
                alarm_available = True

        if events[0].is_alarm is False and alarm_available is True:
            self.calendar_intervention = True
        else:
            self.calendar_intervention = False


    def get_values(self):
        """
        Return all parameters/notifications values
        :return:
            - values: values of notifications, dict
        """
        values = dict()
        values['wifi'] = self.wifi
        values['alarm'] = self.alarm
        values['calendar_intervention'] = self.calendar_intervention

        return values

    def clear(self):
        """
        Clear the values (to default)
        """
        self.wifi = False
        self.alarm = False
        self.calendar_intervention = False
