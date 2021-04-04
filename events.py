from datetime import datetime
import re


class Event:
    def __init__(self):
        self.raw = dict()

        self.id = ''
        self.is_alarm = False
        self.title = ''
        self.start_time = datetime.min
        self.end_time = datetime.min

    def set_event(self, is_alarm, event):

        self.id = event['id']
        self.is_alarm = is_alarm

        self.raw['start'] = event['start']['dateTime']
        self.raw['end'] = event['end']['dateTime']

        self.raw['summary'] = event['summary']
        self.raw['description'] = event['description']

        self.format_data()

    def format_data(self):

        # Set the title as the summary of the event removing the hashtag key
        hashtag_pattern = "^(#[a-zA-Z]+) ([a-zA-Z\w ]+)"
        hashtag_search = re.search(hashtag_pattern, self.raw['summary'])
        if hashtag_search:
            self.title = hashtag_search.group(2)
        else:
            self.title = self.raw['summary']

        # Set the start/end time as datetime
        self.start_time = datetime.strptime(self.raw['start'], '%Y-%m-%dT%H:%M:%S%z')
        self.end_time = datetime.strptime(self.raw['end'], '%Y-%m-%dT%H:%M:%S%z')

        # Set parameters
        self.radio = extract_information_with_hashtag(self.raw['description'] + '#', "#radio")
        self.repetition = extract_information_with_hashtag(self.raw['description'] + '#', "#repetition")


def extract_information_with_hashtag(full_text, hashtag):
    """
    Extract text after a defined hashtag
    :param full_text: Text with hashtag and needed information, string
    :param hashtag: Hashtag to search, string, example: #radio
    :return:
        - information: Information after a hashtag
    """

    # Search hashtag key
    index_defined_hashtag = full_text.find(hashtag)
    index_next_hashtag = full_text.find('#', index_defined_hashtag + 1)

    # Extract information and remove '\n' character
    information = full_text[index_defined_hashtag + len(hashtag) + 1: index_next_hashtag]
    information = information.rstrip()

    return information
