from pyrogram import Client
import asyncio

api_id = 13875777
api_hash = '28bac7e8ca985a86f48aadc28b1b3916'
sesi = 'nama_sesi'

app = Client(name=sesi, api_id=api_id, api_hash=api_hash, workdir="sessions/")

async def main():
    await app.start()
    me = await app.get_me()
    print(me)
    await app.stop()

async def get_otp(sesi):
    async with Client(name=sesi, api_id=api_id, api_hash=api_hash, workdir='sessions/') as app:
        await asyncio.sleep(3)
        async for message in app.get_chat_history(chat_id=777000, limit=5):
            pesan = message.text
            angka = ''.join([char for char in pesan if char.isdigit()])
            print(pesan)
            return angka

# Run the main function to test getting account information
asyncio.run(main())

# Run the get_otp function to test getting OTP messages
asyncio.run(get_otp(sesi))
