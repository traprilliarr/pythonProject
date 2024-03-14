from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
import asyncio
from quart import Quart, jsonify

# Remember to use your own values from my.telegram.org!
api_id = 27934029
api_hash = 'f319509d4dfe73834d265799e0197a1f'
client = TelegramClient('anon', api_id, api_hash)


app = Quart(__name__)


async def get_user_ids(group_username):
    user_ids = []
    try:
        await client.connect()  # Ensure the client is connected
        channel = await client(ResolveUsernameRequest(group_username))
        async for _user in client.iter_participants(entity=channel):
            user_ids.append(_user.id)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()  # Always disconnect after use
    return user_ids

@app.route('/users/<group_username>', methods=['GET'])
async def serve_user_ids(group_username):
    user_ids = await get_user_ids(group_username)
    return jsonify({'user_ids': user_ids})

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # # loop.run_until_complete(get_user_ids())
    # app.run(debug=True)
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run_task(host='0.0.0.0'))