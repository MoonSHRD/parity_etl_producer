import logging
import traceback
from time import sleep

import inject

from block_inspector import BlockInspector
from conf import base_config
from extractors.EtherTransferExtractor import EtherTransferExtractor
from extractors.TokenTransferExtractor import TokenTransferExtractor
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction

logger = logging.getLogger()


def import_block(block):
    txs = []
    for tx_dict in block['transactions']:
        try:
            tx = TransactionMapper.json_dict_to_transaction(tx_dict)
            logger.info("Importing ", extra=tx_dict)
            for transfer in get_tx_value_transfers(tx):
                tx.add_transfer(transfer)
                txs.append(tx)


        except BaseException as e:
            logger.error(e, exc_info=True, extra=tx_dict)

    return txs


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
        block = inspector.get_next_block()

        import_block(block)

        sleep(0.02)
