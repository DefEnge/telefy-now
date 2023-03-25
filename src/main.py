import asyncio
import yaml
import pyrogram
from yaml.loader import SafeLoader
from pyrogram import Client
from pyrogram import raw
from pyrogram.raw import functions
from spotify import api

with open('../config/config.yaml' , 'r' , encoding='UTF-8') as file:
    data = yaml.load(file, Loader = SafeLoader)
async def get_bio(client: pyrogram.Client) -> str:
    user = raw.types.InputUserSelf()
    user_obj = await client.invoke(query= functions.users.GetFullUser(id=user))
    return user_obj.full_user.about

async def modify_bio(client: pyrogram.Client , new_track: str, old_bio: str) -> None:
    new_bio = old_bio + ', Currently playing ' + new_track
    if len(new_bio) > 70:
        new_bio = 'Currently playing ' + new_track

    await client.invoke(query = functions.account.UpdateProfile(about= new_bio))

async def run_queue(seconds: float, app: pyrogram.Client , spotify_api: any, old_bio: str):
    while True:
        if spotify_api.now_playing() is None:
            await asyncio.sleep(seconds)
        else:
            current_track = spotify_api.now_playing().title
            print(current_track)
            await modify_bio(app, current_track, old_bio)
            await asyncio.sleep(seconds)


async def main(api_id: int, api_hash: str, username: str, phone_number: str) -> None:
    """Main function"""
    spotify_api = api.SpotifyAPI(data['client_id'] , data['client_secret'])
    async with Client(username, api_id=api_id, api_hash=api_hash, phone_number=phone_number) as app:
        current_bio = await get_bio(app)
        await run_queue(10.0, app, spotify_api, current_bio)

if __name__ == "__main__":
    asyncio.run(main(data['api_id'] , data['api_hash'] , data['username_account'], data['phone_number']))
