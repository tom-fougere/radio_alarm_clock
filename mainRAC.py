from dateTime import OSDate, NTPDate
from alarms import Alarm
from soundLibrary import Sound
from InternetCheck import InternetChecker

print("Hello world")

currentDateOS = OSDate()
currentDateNTP = NTPDate()
currentAlarm = Alarm()
currentSound = Sound()

# Initialisation
list_alarms = []
for count in range(3):
    alarm = Alarm()
    alarm.set_alarm(currentDateOS.get_hour(), currentDateOS.get_minute()+count, currentSound)
    alarm.set_on()
    list_alarms.append(alarm)


IChecker = InternetChecker()
while True:
    if alarm_active >= 0:
        if IChecker.check_connection():
            for count in range(3):
                currentDateOS.update()
                list_alarms[count].check_activation(currentDateOS)
                print("Alarm %d active : %d" %(count, list_alarms[count].active))
                alarm_active += list_alarms[count].active
        else:
            for count in range(3):
                currentDateNTP.update()
                list_alarms[count].check_activation(currentDateNTP)




currentAlarm.check_activation(currentDateOS)
currentAlarm.deactivate()

IChecker = InternetChecker()
IChecker.check_connection()








