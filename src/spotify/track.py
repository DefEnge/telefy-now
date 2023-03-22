class Track(dict):
    'Represents a now-playing track.'
    def __init__(self, data: dict = None):
        dict.__init__(self, data)
        self.title = data['name']
        self.artist = data['artists'][0]['name']
        self.image = data['album']['images'][0]['url']