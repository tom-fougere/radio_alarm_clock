class Sound:
    def __init__(self):
        self.radioURL = 'http://cdn.nrjaudio.fm/audio1/fr/40011/aac_64.mp3'
        self.mp3Link = None
        self.is_playing = 0
        self.volume = None
        self.radioVSmp3 = 0
            # 0 : radio
            # 1 : mp3

    def play(self):
        self.is_playing = 1
        print("Sound::Play Sound")

    def stop(self):
        self.is_playing = 0
        print("Sound::Stop Sound")

    def isplay(self):
        return self.is_playing

    def setRadio(self, radio_URL):
        self.radioURL = radio_URL

    def setMP3(self, mp3_Link):
        self.mp3Link = mp3_Link

    def setVolume(self, volume):
        self.volume = volume

    def displayRadioURLs(self):
        print("Sound::Display Radio URLs")

    def displayMp3Links(self):
        print("Sound::Display MP3 links")

