import asyncio
import yaml
import pyrogram
from yaml.loader import SafeLoader
from pyrogram import Client
from pyrogram import raw
from pyrogram.raw import functions

with open('../config/config.yaml' , 'r' , encoding='UTF-8') as file:
    data = yaml.load(file, Loader = SafeLoader)

async def get_status(client: pyrogram.Client) -> str:
    user = raw.types.InputUserSelf()
    user_obj = await client.invoke(query= functions.users.GetFullUser(id=user))
    return user_obj.full_user.about

async def modify_bio(client: pyrogram.Client , new_bio: str ) -> None:
    await client.invoke(query = functions.account.UpdateProfile(about= new_bio))


async def main(api_id: int, api_hash: str, username: str, phone_number: str) -> None:
    """Main function"""
    async with Client(username, api_id=api_id, api_hash=api_hash, phone_number=phone_number) as app:
        text = await get_status(app)
        await modify_bio(app, "test")
        print(text)

if __name__ == "__main__":
    asyncio.run(main(data['api_id'] , data['api_hash'] , data['username_account'], data['phone_number']))
