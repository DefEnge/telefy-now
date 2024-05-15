import asyncio
from yaml import load as load_yaml
from yaml.loader import SafeLoader
from pyrogram import Client
from pyrogram import raw
from pyrogram.raw import functions
try:
    from spotify.api import SpotifyAPI
    project_dir = '..'
except ImportError:
    from src.spotify.api import SpotifyAPI
    project_dir = '.'

# Loading data from the config file
with open(f'{project_dir}/config/config.yaml' , 'r' , encoding='UTF-8') as file:
    data = load_yaml(file, Loader = SafeLoader)

# Starting the Spotify client
spotify_client = SpotifyAPI(
    data['spotify_client_id'],
    data['spotify_client_secret'],
    data['spotify_redirect_uri']
)


async def get_status(client: Client) -> str:
    user = raw.types.InputUserSelf()
    user_obj = await client.invoke(query= functions.users.GetFullUser(id=user))
    return user_obj.full_user.about

async def modify_bio(client: Client , new_bio: str ) -> None:
    await client.invoke(query = functions.account.UpdateProfile(about= new_bio))

async def check_playing(app: Client, current_bio: str):
    track = spotify_client.now_playing()
    if track:
        title = track['name']
        artist = ', '.join([a['name'] for a in track['artists']])
        previous = current_bio + ' | ' if current_bio and not current_bio.startswith('Listening') else ''
        await modify_bio(app, previous + f'Listening to {title} by {artist} on Spotify.')
    await asyncio.sleep(30)

async def main(api_id: int, api_hash: str, username: str, phone_number: str) -> None:
    """Main function"""
    async with Client(username, api_id=api_id, api_hash=api_hash, phone_number=phone_number) as app:
        text = await get_status(app)
        try:
            while True:
                await check_playing(app, text)
        except KeyboardInterrupt:
            # Reset the original bio.
            await modify_bio(app, text)


if __name__ == "__main__":
    asyncio.run(main(
        data['api_id'],
        data['api_hash'],
        data['username_account'],
        data['phone_number']
    ))
