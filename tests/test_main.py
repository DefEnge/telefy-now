import pytest
from unittest.mock import Mock
from pyrogram.raw import functions
from src.main import get_status, modify_bio, check_playing

class TestFullUser:
    about = 'Example about'

class TestUser():
    full_user = TestFullUser()

class CustomClient:
    def __init__(self):
        self.times_called = 0
        self.query = None

    async def invoke(self, query):
        self.query = query
        self.times_called += 1
        return TestUser()

async def test_get_status():
    # creating the fake client
    test_client = CustomClient()
    # calling the function
    status = await get_status(test_client)

    # making assertions
    assert type(test_client.query) == functions.users.GetFullUser
    assert test_client.times_called == 1
    assert status == 'Example about'

async def test_modify_bio():
    test_client = CustomClient()
    await modify_bio(test_client, 'New about test')

    assert type(test_client.query) == functions.account.UpdateProfile
    assert test_client.query.about == 'New about test'
    assert test_client.times_called == 1


class CustomSpotifyClient:
    def now_playing(self):
        return {
            'name': 'Demons',
            'artists': [{'name': 'Imagine Dragons'}],
            'album': {'images': [{'url': 'https://i.scdn.co/image/ab67616d0000b273407bd04707c463bbb3410737'}]}
        }

async def custom_modify_bio(app, new_bio):
    assert new_bio == 'Hello World! | Listening to Demons by Imagine Dragons on Spotify.'

async def test_check_playing(mocker):
    test_client = CustomClient()
    test_spotify = CustomSpotifyClient()
    mocker.patch('src.main.spotify_client', new = test_spotify)
    mocker.patch('src.main.modify_bio', new = custom_modify_bio)
    await check_playing(test_client, 'Hello World!')
