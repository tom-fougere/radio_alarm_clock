import json

mandatory_calendars_file = "mandatory_calendars.txt"
mandatory_calendars = {}


def write_dict_file(dict_to_write, filename):
    with open(filename, 'w') as fid:
        json.dump(dict_to_write, fid)


def read_dict_file(filename):
    return json.load(open(filename))


if __name__ == '__main__':
    write_dict_file(mandatory_calendars, mandatory_calendars_file)