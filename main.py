import os
import datetime


def alarms_modification(last_alarms):
    """
        Find the JSON file (where alarms are stored) and check there is no update

        input : datetime of the last update
        output : 0 - No update of the JSON file
                 1 - New updates of the JSON file (modification of alarms)

    """
    for filename in os.listdir("/var/www/html"):

        # Find the correct file
        if filename.startswith("Alarms_") and filename.endswith(".txt"):

            # Extract the date from the filename (remove the file starting and the extension
            filename_date = filename[7:len(filename) - 4]

            # Convert the string to datetime
            current_alarms_update = datetime.datetime.strptime(filename_date, '%Y-%m-%d %H-%M-%S')

            # Check if the file was updated
            if current_alarms_update > last_alarms:
                # Return 1 if the file has been modified
                return 1
            else:
                # Return 0 if the file is the same
                return 0

last_alarms_update = datetime.datetime.now()
print(alarms_modification(last_alarms_update))
