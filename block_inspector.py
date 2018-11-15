import logging
import time

import inject
from eth_rpc_api import ParityEthJsonRpc

from models.transaction import Transaction
from utils import hex_to_dec


class BlockInspector(object):
    rpc_client = inject.attr(ParityEthJsonRpc)
    current_block = 0

    def __init__(self):
        self.current_block = self.rpc_client.eth_blockNumber()

    def get_prev_block(self) -> Transaction:
        return self.__get_another_block(-1)

    def __get_another_block(self, step: int):
        logger = logging.getLogger()
        # logger.error(e, exc_info=True, extra={"txid": transaction['hash']})
        while True:
            print(self.current_block)
            block = self.rpc_client.eth_getBlockByNumber(self.current_block)

            if block is None:
                time.sleep(5)
                logger.info("Sleeping on ", extra={"number": self.current_block})
                continue

            self.current_block = hex_to_dec(block['number']) + step
            logger.info("Fetched new block", extra={"number": self.current_block - 1})

            return block

    def get_next_block(self) -> Transaction:
        return self.__get_another_block(1)
