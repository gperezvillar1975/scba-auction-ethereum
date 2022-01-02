# import the following dependencies
import asyncio
from  event_processor import log_loop
from  socket_server import handler
import websockets
import global_defs
from contract_functions import load_auctions

global_defs.JOIN = {}
global_defs.AUCTIONS = {}
load_auctions()

def main():
    loop = asyncio.get_event_loop()
    print('Starting Event Loop')
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(2),
                websockets.serve(handler, "localhost", 8765)
                )
            )
    finally:
        loop.close()

if __name__ == "__main__":
    main()