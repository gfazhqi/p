from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio

async def main():
    client = TelegramClient("@ldrose3.session.session")
    
    tdesk = await client.ToTDesktop(flag=UseCurrentSession)
    
    # Save the session to a folder named "tdata"
    tdesk.SaveTData("tdata")

asyncio.run(main())
