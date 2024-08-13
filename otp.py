import logging
import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PhoneNumberBanned, PhoneCodeInvalid, SessionPasswordNeeded

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

api_id = int(os.getenv('13875777'))
api_hash = os.getenv('28bac7e8ca985a86f48aadc28b1b3916')

async def start_client(phone_number):
    client = Client(f'session/{phone_number}', api_id, api_hash, phone_number=phone_number)
    await client.connect()
    return client

async def fetch_account_info(client, phone_number):
    try:
        me = await client.get_me()
        logger.info(f'TELECODE RECEIVER: Un: {me.username}, No: {phone_number} ▪︎ {me.first_name}')
        logger.info('Waiting to receive code...\n')
    except Exception as e:
        logger.error(f'Error fetching account info: {e}')

async def main():
    if len(sys.argv) < 2:
        print('Usage: python start.py phone_number')
        exit(1)
    phone_number = sys.argv[1]

    if not os.path.exists("session"):
        os.mkdir("session")

    try:
        client = await start_client(phone_number)
        await client.start()

        if not client.is_authorized:
            try:
                await client.send_code(phone_number)
                await client.sign_in(phone_number, input('Enter the code: '))
            except SessionPasswordNeeded:
                logger.error(f'{phone_number} Session Password Needed!')
                await client.stop()
            except PhoneCodeInvalid:
                logger.error(f'{phone_number} ▪︎ Code Invalid!')
                await client.stop()

        await fetch_account_info(client, phone_number)

        @client.on_message(filters.private & filters.user(777000))
        async def handler(client, message):
            if message.text:
                logger.info(message.text)

        logger.info('[!] Connected!')
        await client.idle()
    except PhoneNumberBanned:
        logger.error(f'{phone_number} ▪︎ Number Banned!')
        sys.exit()
    except FloodWait as e:
        logger.error(f'{phone_number} ▪︎ Flood Wait Error! {e.x} seconds')
        sys.exit()
    except PhoneCodeInvalid:
        logger.error(f'{phone_number} ▪︎ Code Invalid!')

if __name__ == '__main__':
    asyncio.run(main())
