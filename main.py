import logging
import traceback
from time import sleep

import inject

from block_inspector import BlockInspector
from conf import base_config
from extractors import TokenTransferExtractor, EtherTransferExtractor
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction

logger = logging.getLogger()


def import_block(block_cb):
    block = block_cb()
    for tx_dict in block['transactions']:
        try:
            tx = TransactionMapper.json_dict_to_transaction(tx_dict)
            logger.info("Importing ", extra=tx_dict)
            for transfer in get_tx_value_transfers(tx):
                tx.add_transfer(transfer)

        except BaseException as e:
            logger.error(e, exc_info=True, extra=tx_dict)


# @todo Нужен повторяемый тест  для CI
# @body в качестве источника данных можно использовать инфьюру
def get_tx_value_transfers(transaction: Transaction):
    transfers = []
    try:
        if transaction.block_number is None:
            return []

        for transfer in TokenTransferExtractor.extract(transaction):
            transfers.append(transfer)

        for transfer in EtherTransferExtractor.extract(transaction):
            transfers.append(transfer)

    except BaseException as e:
        logger.error(e, {"trace": traceback.format_exc(), "txid": transaction.hash})

    return transfers


if __name__ == '__main__':
    inject.configure(base_config)
    inspector = BlockInspector()
    while True:
        import_block(inspector.get_next_block)
        sleep(0.02)
