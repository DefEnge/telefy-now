from src.spotify import api


class TestSpotifyAPI():
    # Imitates the api.SpotifyAPI class
    # counts the number of times
    # current_user_playing_track is called
    times_called = 0

    def current_user_playing_track(self):
        # increment the counter
        self.times_called += 1
        # return a possible response from Spotify APIs
        return {'item': {
            'name': 'Demons',
            'artists': [{'name': 'Imagine Dragons'}],
            'album': {'images': [{'url': 'https://i.scdn.co/image/ab67616d0000b273407bd04707c463bbb3410737'}]}
        }}


def test_now_playing():
    # creating the fake api.SpotifyAPI
    test_spotify_api = TestSpotifyAPI()
    # calling the function with the fake self
    result = api.SpotifyAPI.now_playing(test_spotify_api)

    # making assertions
    assert test_spotify_api.times_called == 1
    assert result.title == 'Demons'
    assert result.artist == 'Imagine Dragons'
    assert result.image == 'https://i.scdn.co/image/ab67616d0000b273407bd04707c463bbb3410737'