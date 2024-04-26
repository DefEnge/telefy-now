from spotipy import Spotify, oauth2
from typing import Union
from . import track

class SpotifyAPI(Spotify):
    'Main class to interact with the Spotify Web API.'
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = 'http://localhost:1024/redirect'):
        Spotify.__init__(self, auth_manager = oauth2.SpotifyOAuth(
            client_id = client_id,
            client_secret = client_secret,
            redirect_uri = redirect_uri,
            scope = 'user-read-currently-playing user-read-playback-state',
        ))
    
    def now_playing(self) -> Union[track.Track, None]:
        result = self.current_user_playing_track()
        return None if result is None else track.Track(result['item'])
