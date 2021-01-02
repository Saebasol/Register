import discord
import aiohttp
import argparse
import os
from base64 import b64decode
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
import time

parser = argparse.ArgumentParser("register")

comment = parser.add_argument("--userid", type=int)

args = parser.parse_args()

user_id: str = args.userid

key = SigningKey(b64decode(os.environ["SIGN_KEY"]))

api_key = key.sign(f"{user_id}{round(time.time())}".encode(), encoder=Base64Encoder)


async def send_api_key():
    async with aiohttp.ClientSession() as cs:
        async with cs.post(
            "https://doujinshiman.ga/v3/api/register",
            json={"user_id": user_id, "api_key": api_key},
            headers={"Verification": os.environ["VERIFI"]},
        ) as r:
            res = await r.json()
            if r.status != 201:
                if r.status == 200:
                    print("Already register")
                    return
                else:
                    print(f"cant register: {res['message']}")
                    return

    client = discord.Client()
    await client.start(os.environ["BOT_TOKEN"])
    user = await client.fetch_user(int(user_id))
    try:
        user.send(
            f"Congratulations. \nApproved! Please request through key: ``{api_key}``.\nHere is an example:\n```py\nrequests.get('example.com', headers={'Authorization': {api_key}})"
        )
    except Exception as e:
        print(f"Can't send Message Because:{e}")
    else:
        print("Success send message")

    await client.close()


import asyncio

asyncio.run(send_api_key())